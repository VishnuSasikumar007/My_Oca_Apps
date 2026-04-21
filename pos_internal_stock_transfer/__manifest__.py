{
    'name': "POS Internal Stock Transfer",

    'summary': "Transfer stock from one warehouse to another directly from POS.",

    'description': """
This module allows users to create internal stock transfers directly from the Point of Sale interface.

FEATURES:

• Create internal stock transfers from POS.
• Send stock from current POS warehouse to another warehouse.
• Transfer based on selected POS order lines.
• Seamless integration with POS workflow.
• Fully compatible with Odoo v19.

WORKFLOW:

1. User clicks "Send Stock" button in POS.
2. System collects selected order line products and quantities.
3. Popup appears to select destination warehouse.
4. User confirms transfer.
5. Internal stock transfer (stock.picking) is created.

This module extends POS using OWL and integrates with Inventory for smooth internal logistics operations.

Ideal for businesses managing multiple warehouses or store-to-store transfers directly from POS.

""",

    'author': "Vishnu Sasikumar",
    'website': "",
    'category': 'Point of Sale',
    'version': '19.0.1.0',

    'depends': ['base', 'point_of_sale', 'stock'],

    'data': [
        'views/pos_config_views.xml',
    ],

    'assets': {
        'point_of_sale._assets_pos': [
            'pos_internal_stock_transfer/static/src/js/pos_internal_stock_transfer_button.js',
            'pos_internal_stock_transfer/static/src/js/pos_internal_stock_transfer_popup.js',
            'pos_internal_stock_transfer/static/src/xml/pos_internal_stock_transfer_button.xml',
            'pos_internal_stock_transfer/static/src/xml/pos_internal_stock_transfer_popup.xml',
        ],
    },

    'images': ['static/description/banner.png'],

    'license': "LGPL-3",
    'installable': True,
    'application': True,
    'auto_install': False,
}