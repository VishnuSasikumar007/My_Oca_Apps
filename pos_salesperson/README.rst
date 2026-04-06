.. image:: https://itpp.dev/images/infinity-readme.png
   :alt: Tested and maintained by Vishnu Sasikumar
   :target: https://apps.odoo.com

=====================
 POS Salesperson
=====================

This module enforces the selection of a salesperson in the Point of Sale Payment Screen based on POS configuration.

When the **Salesperson Mandatory** option is enabled in POS settings, the system prevents order validation until a salesperson is selected.

Users can choose a salesperson from the configured list directly in the Payment Screen.

Features
========

* Mandatory salesperson selection based on POS configuration
* Salesperson selection in Payment Screen
* Restricts order validation without salesperson
* Supports multiple allowed salespersons
* Seamless integration with POS and POS HR
* Automatically stores salesperson in POS Order

Usage
=====

1. Go to **Point of Sale → Configuration → Point of Sale**
2. Open your POS configuration
3. Enable **Salesperson Mandatory**
4. Select allowed salespersons
5. Start POS session
6. Select salesperson in Payment Screen before validating order

Questions?
==========

For support or any queries, contact:
:arrow_right: vishnu.sit2015@gmail.com

Author
======

* Vishnu Sasikumar

Further information
===================

Odoo Apps Store: https://apps.odoo.com

Tested on `Odoo 19.0 <https://www.odoo.com>`_