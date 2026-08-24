import hashlib
import hmac
import random
from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import AccessDenied, UserError


def _hash_code(code, salt):
    """One-way hash of the plaintext code; nothing readable is stored."""
    return hashlib.sha256(f"{salt}:{code}".encode()).hexdigest()


class LoginOTP(models.Model):
    _name = "login.otp"
    _description = "Login One-Time Password"
    _order = "create_date desc"
    _rec_name = "user_id"

    user_id = fields.Many2one("res.users", required=True, index=True, ondelete="cascade")
    email = fields.Char(required=True, help="Address the code was sent to.")
    code_hash = fields.Char(required=True)
    salt = fields.Char(required=True)
    state = fields.Selection(
        [("sent", "Sent"), ("used", "Used"), ("expired", "Expired")],
        default="sent",
        required=True,
        index=True,
    )
    attempts = fields.Integer(default=0)
    expires_at = fields.Datetime(required=True)

    # ------------------------------------------------------------------
    # Config helpers
    # ------------------------------------------------------------------
    @api.model
    def _get_param(self, key, default):
        icp = self.env["ir.config_parameter"].sudo()
        try:
            return int(icp.get_param(f"auth_otp_login.{key}", default))
        except (TypeError, ValueError):
            return default

    @api.model
    def _validity_minutes(self):
        return self._get_param("code_validity_minutes", 5)

    @api.model
    def _max_attempts(self):
        return self._get_param("max_attempts", 5)

    @api.model
    def _resend_cooldown_seconds(self):
        return self._get_param("resend_cooldown_seconds", 60)

    # ------------------------------------------------------------------
    # Issuing codes
    # ------------------------------------------------------------------
    @api.model
    def _can_resend(self, user):
        """Simple per-user rate limit: block re-sends inside the cooldown."""
        return self._resend_remaining_seconds(user) <= 0

    @api.model
    def _resend_remaining_seconds(self, user):
        """Seconds left before another code may be requested for this
        user. 0 if none is pending or the cooldown has already passed."""
        if not user:
            return 0
        last = self.sudo().search(
            [("user_id", "=", user.id)], order="create_date desc", limit=1
        )
        if not last:
            return 0
        elapsed = (fields.Datetime.now() - last.create_date).total_seconds()
        remaining = self._resend_cooldown_seconds() - elapsed
        return max(0, int(remaining))

    @api.model
    def _expiry_remaining_seconds(self, user):
        """Seconds left before the current pending code expires. Falls
        back to the nominal full validity window when there's no real
        pending code (unknown login, already used/expired) so the page
        can't be used to infer whether an account exists."""
        if user:
            pending = self.sudo().search(
                [("user_id", "=", user.id), ("state", "=", "sent")],
                order="create_date desc",
                limit=1,
            )
            if pending:
                remaining = (pending.expires_at - fields.Datetime.now()).total_seconds()
                return max(0, int(remaining))
        return self._validity_minutes() * 60

    @api.model
    def _create_for_user(self, user):
        """Invalidate any pending code and issue + email a fresh one."""
        if not user.email:
            raise UserError("This account has no email address on file.")

        # Invalidate any still-pending codes for this user first.
        self.sudo().search(
            [("user_id", "=", user.id), ("state", "=", "sent")]
        ).write({"state": "expired"})

        code = f"{random.SystemRandom().randint(0, 999999):06d}"
        salt = hashlib.sha256(str(random.SystemRandom().random()).encode()).hexdigest()[:16]

        otp = self.sudo().create({
            "user_id": user.id,
            "email": user.email,
            "code_hash": _hash_code(code, salt),
            "salt": salt,
            "state": "sent",
            "expires_at": fields.Datetime.now() + timedelta(minutes=self._validity_minutes()),
        })
        otp._send_email(code)
        return otp

    def _send_email(self, code):
        self.ensure_one()
        template = self.env.ref("auth_otp_login.email_template_login_otp", raise_if_not_found=False)

        if template:
            template.sudo().with_context(
                otp_code=code,
                otp_validity_minutes=self._validity_minutes(),
            ).send_mail(self.id, force_send=True)
            return

        # Defensive fallback only - shouldn't happen once the module's
        # data file has loaded, but avoids leaving the user stranded.
        mail_values = {
            "subject": "Your login code",
            "body_html": (
                "<div style='font-family:Arial,sans-serif;font-size:14px;color:#333'>"
                "<p>Your one-time login code is:</p>"
                f"<p style='font-size:28px;font-weight:bold;letter-spacing:4px'>{code}</p>"
                f"<p>This code expires in {self._validity_minutes()} minutes. "
                "If you didn't request this, you can ignore this email.</p>"
                "</div>"
            ),
            "email_to": self.email,
            "auto_delete": True,
        }
        self.env["mail.mail"].sudo().create(mail_values).send()

    # ------------------------------------------------------------------
    # Verifying codes
    # ------------------------------------------------------------------
    @api.model
    def _verify(self, user, code):
        """Raise AccessDenied on any failure; return True on success."""
        otp = self.sudo().search(
            [("user_id", "=", user.id), ("state", "=", "sent")],
            order="create_date desc",
            limit=1,
        )
        if not otp:
            raise AccessDenied("No pending code for this account. Request a new one.")

        if fields.Datetime.now() > otp.expires_at:
            otp.state = "expired"
            raise AccessDenied("This code has expired. Request a new one.")

        if otp.attempts >= otp._max_attempts():
            otp.state = "expired"
            raise AccessDenied("Too many incorrect attempts. Request a new one.")

        expected = _hash_code(code or "", otp.salt)
        if not hmac.compare_digest(expected, otp.code_hash):
            otp.attempts += 1
            raise AccessDenied("Incorrect code.")

        otp.state = "used"
        return True
