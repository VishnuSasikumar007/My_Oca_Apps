from werkzeug.urls import url_encode

from odoo import http
from odoo.exceptions import AccessDenied, UserError
from odoo.http import request


class AuthOTPLogin(http.Controller):

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _find_user(self, email):
        """Find active user by email only."""
        email = (email or "").strip().lower()
        if not email:
            return request.env["res.users"]

        return request.env["res.users"].sudo().search([
            ("email", "=", email),
            ("active", "=", True),
        ], limit=1)

    def _finish_login(self, user):
        """Log the user in after successful OTP verification."""

        request.session.uid = user.id
        request.session.login = user.login
        request.session.session_token = user._compute_session_token(
            request.session.sid
        )
        request.update_env(user=user.id)

    # ------------------------------------------------------------------
    # Step 1 - Request OTP
    # ------------------------------------------------------------------

    @http.route(
        "/web/login_otp",
        type="http",
        auth="public",
        website=True,
        sitemap=False,
        csrf=True,
    )
    def login_otp(self, **kw):

        redirect = kw.get("redirect") or "/web"
        error = None
        email = ""

        if request.httprequest.method == "POST":

            email = (kw.get("email") or "").strip().lower()
            user = self._find_user(email)

            if not user:
                error = "No account found with this email address."

            elif not user.email:
                error = "This account does not have an email address."

            else:
                try:
                    otp = request.env["login.otp"].sudo()

                    if otp._can_resend(user):
                        otp._create_for_user(user)

                    query = url_encode({
                        "email": email,
                        "redirect": redirect,
                    })

                    return request.redirect(
                        "/web/login_otp/verify?%s" % query
                    )

                except UserError as e:
                    error = str(e)

        return request.render(
            "auth_otp_login.login_otp_request",
            {
                "redirect": redirect,
                "error": error,
                "email": email,
            },
        )

    # ------------------------------------------------------------------
    # Step 2 - Verify OTP
    # ------------------------------------------------------------------

    @http.route(
        "/web/login_otp/verify",
        type="http",
        auth="public",
        website=True,
        sitemap=False,
        csrf=True,
    )
    def login_otp_verify(self, **kw):

        email = (kw.get("email") or "").strip().lower()
        redirect = kw.get("redirect") or "/web"

        error = None
        info = None

        user = self._find_user(email)
        otp = request.env["login.otp"].sudo()

        if request.httprequest.method == "POST":

            action = kw.get("action") or "verify"

            if action == "resend":

                if not user:
                    error = "No account found with this email address."

                elif not otp._can_resend(user):
                    error = "Please wait before requesting another OTP."

                else:
                    try:
                        otp._create_for_user(user)
                        info = "A new verification code has been sent to your email."

                    except UserError as e:
                        error = str(e)

            else:

                code = (kw.get("code") or "").strip()

                if not user:
                    error = "No account found with this email address."

                else:
                    try:
                        otp._verify(user, code)

                        self._finish_login(user)

                        return request.redirect(redirect)

                    except AccessDenied as e:
                        error = str(e)

        return request.render(
            "auth_otp_login.login_otp_verify",
            {
                "email": email,
                "redirect": redirect,
                "error": error,
                "info": info,
                "validity_seconds": otp._expiry_remaining_seconds(user),
                "resend_cooldown_seconds": otp._resend_remaining_seconds(user),
            },
        )