{
    'name': "POS Shop Image in Kanban",

    'summary': "Display POS shop image in the dashboard kanban view.",

    'description': """
This module allows you to upload and display a shop image for each Point of Sale configuration in the dashboard kanban view.

FEATURES:

• Add a custom image field to POS configuration.
• Upload shop/store image from POS settings.
• Display the image in POS dashboard kanban cards.
• Enhances visual identification of POS shops.
• Clean integration with existing POS kanban UI.
• Lightweight and easy to configure.
• Fully compatible with Odoo v19.

WORKFLOW:

1. Navigate to Point of Sale configuration.
2. Upload a shop image in the provided field.
3. Save the configuration.
4. The image appears in the POS dashboard kanban view.

This module is useful for businesses managing multiple POS shops, enabling quick visual recognition directly from the dashboard.
""",

    'author': "Vishnu Sasikumar",
    'website': "",
    'category': 'Point of Sale',
    'version': '19.0.1.0',

    'depends': ['base', 'point_of_sale'],

    'data': [
        'views/pos_config_views.xml',
    ],

    'images': ['static/description/banner.png'],

    'license': "LGPL-3",
    'installable': True,
    'application': True,
    'auto_install': False,
}