.. image:: https://itpp.dev/images/infinity-readme.png
   :alt: Tested and maintained by Vishnu Sasikumar
   :target: https://apps.odoo.com


=========================================
 POS Shop Image in Kanban Dashboard
=========================================

This module enhances the **Point of Sale (POS) dashboard** by allowing users to display a **custom shop image directly in the Kanban view**.

It improves visual identification of POS configurations, making the dashboard more intuitive and user-friendly—especially in multi-shop or multi-location environments.


Features
========

* Display custom image for each POS in Kanban dashboard
* Easily upload and manage POS shop images
* Clean and modern UI integration
* Improves visual recognition of POS configurations
* Supports multiple POS setups (multi-shop environments)
* Lightweight and seamless integration with existing POS view


Usage
=====

1. Go to **Point of Sale → Configuration → Point of Sale**
2. Open any POS configuration
3. Upload an image in **POS Shop Image** field
4. Save the configuration
5. Navigate to the POS dashboard (Kanban view)
6. The uploaded image will be displayed in the POS card


Workflow
========

**Step 1 : Upload POS Shop Image**

Add an image in the *POS Shop Image* field inside POS configuration.

**Step 2 : Save Configuration**

Ensure the configuration is saved properly.

**Step 3 : View in Kanban Dashboard**

The image will automatically appear in the POS Kanban card.

**Step 4 : Visual Enhancement**

Each POS card now shows its respective shop image for better usability.


Technical Notes
===============

* Field Type: ``Binary``
* Model Extended: ``pos.config``
* View Modified: POS Kanban View
* Compatible with: Odoo 19.0


Questions?
==========

For support or any queries, contact:

:arrow_right: vishnu.sit2015@gmail.com


Author
======

* Vishnu Sasikumar


Further Information
===================

Odoo Apps Store: https://apps.odoo.com

Tested on `Odoo 19.0 <https://www.odoo.com>`_