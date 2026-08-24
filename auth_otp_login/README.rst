.. image:: https://itpp.dev/images/infinity-readme.png
:alt: Tested and maintained by Vishnu Sasikumar
:target: https://apps.odoo.com

=========================================
Login with OTP (Email)
======================

This module provides a secure and convenient **Email OTP Login** option for
Odoo 19.0.

It adds a **"Log in with a code by email"** option to the standard Odoo login
page, allowing users to authenticate using a temporary 6-digit One-Time
Password (OTP) sent to their registered email address instead of entering
their password.

The regular Odoo password-based login remains completely unchanged and
continues to be available.

# Features

* Login using a 6-digit OTP sent by email
* "Log in with a code by email" option on the standard Odoo login page
* Supports both **Internal Users** and **Portal Users**
* Email-based OTP verification
* Secure temporary OTP codes
* OTP expiry with live countdown timer
* Resend OTP cooldown timer
* Maximum OTP verification attempt limit
* 6-box OTP input interface
* Automatic login after successful OTP verification
* Existing password login remains available
* Configurable OTP settings from General Settings
* Show/hide OTP login option
* Configurable OTP validity duration
* Configurable maximum verification attempts
* Configurable resend cooldown
* Clean and responsive login interface
* Works with the standard Odoo authentication flow

# Login Flow

The module provides the following authentication flow:

1. User opens the standard Odoo login page at **/web/login**.
2. User clicks **"Log in with a code by email"**.
3. User is redirected to **/web/login_otp**.
4. User enters their registered login/email address.
5. The system generates a secure 6-digit OTP.
6. The OTP is sent to the user's registered email address.
7. User is redirected to **/web/login_otp/verify**.
8. User enters the OTP using the 6-digit verification interface.
9. A live countdown displays the remaining OTP validity period.
10. After successful verification, the user is logged into Odoo.
11. If the OTP expires, the user can request a new OTP after the configured
    resend cooldown.

The regular password login remains available throughout the process.

# Configuration

The OTP login functionality can be configured from:

**Settings > General Settings > Login with OTP**

The following options are available:

## Show Login with OTP

Enable or disable the **"Log in with a code by email"** option on the
standard Odoo login page.

## Code Validity

Configure how long the generated OTP remains valid.

Example:

* 5 minutes
* 10 minutes
* 15 minutes

## Maximum Attempts

Configure the maximum number of incorrect OTP verification attempts allowed
for a generated OTP.

Once the maximum number of attempts is reached, the OTP can no longer be
used.

## Resend Cooldown

Configure the waiting time before the user can request another OTP.

This helps prevent excessive OTP generation and email requests.

# Usage

1. Open the Odoo login page.
2. Enter the OTP login option by clicking **"Log in with a code by email"**.
3. Enter the registered email/login.
4. Click the button to request the OTP.
5. Check the registered email inbox.
6. Enter the received 6-digit OTP.
7. Click **Verify & Login**.
8. The user will be authenticated and redirected into Odoo.

# OTP Verification

The verification screen provides a user-friendly OTP interface containing:

* Six individual OTP input boxes
* Automatic focus between OTP fields
* OTP expiry countdown
* Resend OTP countdown
* OTP verification status
* Maximum attempt handling
* Validation for incorrect or expired OTPs

# Security

The module is designed to provide an additional authentication method while
maintaining the existing Odoo login mechanism.

Security features include:

* Temporary 6-digit OTP codes
* Configurable OTP expiration
* Maximum verification attempt protection
* Resend cooldown protection
* OTP validation before authentication
* Expired OTPs cannot be used
* OTPs are associated with the requested user/login
* Existing password authentication is not modified
* Only valid OTP verification results in authentication

# User Support

The OTP login method supports:

* Internal Odoo users
* Portal users

The OTP is sent to the email address associated with the user's account.

# Technical Details

* Designed for **Odoo 19.0**
* Integrates with the standard Odoo `/web/login` flow
* Provides dedicated OTP request and verification routes
* Uses Odoo's email infrastructure for OTP delivery
* Uses temporary OTP validation
* Supports configurable security parameters
* Responsive frontend interface
* Compatible with the standard Odoo authentication process
* Password login remains untouched

# Routes

The module introduces the following OTP-related routes:

**/web/login_otp**
OTP login request page where the user enters their login/email.

**/web/login_otp/verify**
OTP verification page where the user enters the received 6-digit code.

The standard Odoo login route remains available:

**/web/login**
Standard Odoo username/password login.

# Requirements

* Odoo 19.0
* Users must have a valid email address configured on their Odoo account.
* Outgoing email must be properly configured in Odoo.
* Users must have permission to access the relevant Odoo application.

# Installation

1. Copy the module into your Odoo custom addons directory.

2. Restart the Odoo server.

3. Update the Apps list.

4. Search for **Login with OTP (Email)**.

5. Install the module.

6. Configure the OTP settings from:

   **Settings > General Settings > Login with OTP**

7. Make sure the Odoo outgoing mail server is configured correctly.

# Email Configuration

The OTP is delivered using Odoo's configured outgoing email server.

Before using the OTP login functionality, make sure:

* An outgoing mail server is configured.
* The user's account has a valid email address.
* Email delivery is working correctly.

If the outgoing mail server is not configured, users may not receive their
OTP emails.

# Compatibility

+----------------------+----------------------+
| Odoo Version         | Supported            |
+======================+======================+
| Odoo 19.0            | Yes                  |
+----------------------+----------------------+

The module is designed specifically for **Odoo 19.0**.

# Benefits

* Passwordless login option
* Faster authentication
* Improved user convenience
* Email-based authentication
* Additional login flexibility
* Configurable security controls
* Supports both backend and portal users
* No changes to the existing password login workflow

# Questions?

For support or any queries, contact:

:arrow_right: [vishnu.sit2015@gmail.com](mailto:vishnu.sit2015@gmail.com)

# Author

* Vishnu Sasikumar

# Further information

Odoo Apps Store: https://apps.odoo.com

Tested on `Odoo 19.0 <https://www.odoo.com>`_
