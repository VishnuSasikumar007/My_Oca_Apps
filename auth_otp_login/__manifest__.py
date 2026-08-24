{
    "name": "Login with OTP (Email)",
    "version": "19.0.1.0.0",
    "category": "Extra Tools",
    "summary": "Passwordless login option: emails a one-time code as an "
                "alternative to the password field on /web/login.",
    "description": """
        Login with OTP (Email)
        =======================
        Adds a "Log in with a code by email" option to the standard Odoo login page.

        Flow:
        1. User clicks "Log in with a code by email" on /web/login.
        2. User enters their login/email on /web/login_otp.
        3. A 6-digit code is emailed to the address on file and the user is
           sent to /web/login_otp/verify, where a 6-box code entry field with
           a live expiry countdown and a resend cooldown timer is shown.
        4. Entering the correct code within the validity window logs the user in,
           exactly as if they had typed their password.

        Applies to both backend (internal) and portal users. The regular
        password login is untouched and still available.

        Configurable from Settings > General Settings > Login with OTP:
        - Show/hide the OTP link on the login page
        - Code validity (minutes)
        - Max attempts
        - Resend cooldown (seconds)
    """,
    'author': 'Vishnu Sasikumar',
    "license": "LGPL-3",
    'price': 30,
    'currency': 'USD',
    "depends": ["web", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "data/mail_template.xml",
        "views/login_templates.xml",
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "auth_otp_login/static/src/scss/login_otp.scss",
        ],
    },
    'images': ['static/description/banner.png'],
    "installable": True,
    "application": False,
}
