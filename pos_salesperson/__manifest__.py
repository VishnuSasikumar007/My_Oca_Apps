{
    "name": "POS Salesperson",
    "summary": "Select Salesperson on the Payment Screen",
    "description": "This module allows selecting a salesperson in the POS Payment Screen and stores it in the POS Order based on the configuration.",
    "category": "Point of Sale",
    "version": "19.0.1.0",
    "author": "Vishnu Sasikumar",
    "license": "LGPL-3",
    "depends": ["point_of_sale", "pos_hr", "hr"],
    "data": [
        "views/pos_config_views.xml",
        "views/pos_order_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_salesperson/static/src/js/main.js",
            "pos_salesperson/static/src/js/PaymentScreenInherit.js",
            "pos_salesperson/static/src/js/PosModel.js",
            "pos_salesperson/static/src/xml/PaymentScreenSalesperson.xml",
        ],
    },
    "auto_install": False,
    "installable": True,
    "application": True,
}