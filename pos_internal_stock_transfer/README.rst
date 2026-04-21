.. image:: https://itpp.dev/images/infinity-readme.png
   :alt: Tested and maintained by Vishnu Sasikumar
   :target: https://apps.odoo.com


===============================
 POS Internal Stock Transfer
===============================

This module allows users to create **internal stock transfers directly from the Point of Sale (POS)** interface.

With a single click, products added in the POS cart can be transferred from the current warehouse to another selected warehouse without leaving the POS screen.

The system also includes validation checks to ensure accurate and controlled stock movements.


Features
========

* Create internal stock transfers directly from POS
* Transfer products from POS warehouse to another warehouse
* Controlled via POS configuration (**Allow Send Stock** option)
* Automatically captures products and quantities from order lines
* Instant creation of stock transfers (``stock.picking``)
* User-friendly popup for warehouse selection
* Validation warnings for missing inputs:
  
  - Prevents transfer without selecting products
  - Prevents transfer without selecting destination warehouse

* Seamless integration with POS workflow


Usage
=====

1. Go to **Point of Sale → Configuration → Point of Sale**
2. Open your POS configuration
3. Enable **Allow Send Stock**
4. Start a POS session
5. Add products to the cart
6. Click **Send Stock**
7. Select the destination warehouse in the popup
8. Confirm to create the internal transfer


Workflow
========

**Step 1 : Enable Feature in POS Configuration**

Activate the *Allow Send Stock* option in POS settings.

**Step 2 : Click "Send Stock" in POS**

Add products to the cart and click the *Send Stock* button.

**Step 3 : Select Destination Warehouse**

A popup appears allowing you to choose the destination warehouse.

**Step 4 : Stock Transfer Created**

The system creates an internal transfer based on selected products and quantities.

**Step 5 : Validation & Warning Handling**

The system ensures proper validation before creating transfers:

* Warning is shown if no products are selected
* Warning is shown if no destination warehouse is selected


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