{
    'name': "POS Negative Stock Restriction",

    'summary': "Prevent negative stock in POS with location-based validation (Supports variants & barcode).",

    'description': """
This module prevents selling products when stock is insufficient in the configured warehouse/location in Point of Sale.

FEATURES:

• Blocks negative stock in POS.
• Location-based stock validation.
• Supports products WITH variants.
• Supports products WITHOUT variants.
• Validates stock in product variant popup.
• Validates stock during barcode scanning.
• Displays warning popup if stock is not available.
• Prevents order line creation when quantity exceeds available stock.
• Ensures real-time inventory accuracy.
• Fully compatible with Odoo v19.

WORKFLOW:

1. When clicking a product:
   - System checks stock before adding to order.
   - If stock is zero → Warning popup shown.

2. When selecting variant from popup:
   - Stock is validated per selected variant.
   - Prevents adding if unavailable.

3. When scanning barcode:
   - Real-time stock validation triggered.
   - Blocks addition if stock is insufficient.

This module overrides core POS methods safely using OWL patching and ensures clean integration without breaking standard POS flow.

Ideal for businesses that require strict stock control and want to avoid overselling in retail environments.

""",

    'author': "Vishnu Sasikumar",
    'website': "",
    'category': 'Point of Sale',
    'version': '1.0',
    'depends': ['base', 'point_of_sale', 'stock'],

    'data': [],

    'assets': {
        'point_of_sale._assets_pos': [
            'pos_negative_stock_restrict/static/src/js/product_screen.js',
        ],
    },

    'images': ['static/description/banner.png'],
    'license': "LGPL-3",
    'price': 10.0,
    'currency': 'USD',

    'installable': True,
    'application': True,
    'auto_install': False,
}
