from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    auth_otp_login_show_on_login = fields.Boolean(
        string="Show \"Log in with a code by email\" on the login page",
        help="When enabled, the login page (/web/login) shows a link "
             "letting users sign in with an emailed one-time code "
             "instead of their password.",
    )
    auth_otp_login_code_validity_minutes = fields.Integer(
        string="Code Validity (minutes)",
        config_parameter="auth_otp_login.code_validity_minutes",
        default=5,
        help="How long an emailed code stays valid before it expires.",
    )
    auth_otp_login_max_attempts = fields.Integer(
        string="Max Attempts",
        config_parameter="auth_otp_login.max_attempts",
        default=5,
        help="Number of incorrect attempts allowed before a code is "
             "invalidated and a new one must be requested.",
    )
    auth_otp_login_resend_cooldown_seconds = fields.Integer(
        string="Resend Cooldown (seconds)",
        config_parameter="auth_otp_login.resend_cooldown_seconds",
        default=60,
        help="Minimum time a user must wait before requesting another "
             "code to be sent.",
    )

    # ------------------------------------------------------------------
    # auth_otp_login_show_on_login is handled manually (instead of via
    # config_parameter=...) because Odoo's automatic config_parameter
    # boolean handling *deletes* the ir.config_parameter row when the
    # box is unchecked, instead of writing "False". That means
    # get_param(key, default="True") would keep falling back to "True"
    # forever and the box could never actually turn the link off.
    # ------------------------------------------------------------------
    @api.model
    def get_values(self):
        res = super().get_values()
        icp = self.env["ir.config_parameter"].sudo()
        res["auth_otp_login_show_on_login"] = (
            icp.get_param("auth_otp_login.show_on_login", "True") == "True"
        )
        return res

    def set_values(self):
        super().set_values()
        self.env["ir.config_parameter"].sudo().set_param(
            "auth_otp_login.show_on_login",
            "True" if self.auth_otp_login_show_on_login else "False",
        )

    @api.constrains(
        "auth_otp_login_code_validity_minutes",
        "auth_otp_login_max_attempts",
        "auth_otp_login_resend_cooldown_seconds",
    )
    def _check_auth_otp_login_positive(self):
        for rec in self:
            for field_name, label in (
                ("auth_otp_login_code_validity_minutes", "Code Validity"),
                ("auth_otp_login_max_attempts", "Max Attempts"),
                ("auth_otp_login_resend_cooldown_seconds", "Resend Cooldown"),
            ):
                if rec[field_name] <= 0:
                    raise ValidationError(
                        f"{label} must be greater than zero."
                    )

