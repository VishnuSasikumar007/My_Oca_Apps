{
    'name': "POS Sales Dashboard",
    'summary': "Advanced POS dashboard with analytics, charts, and insights",

    'description': """
        This module provides a modern POS Sales Dashboard inside the Point of Sale interface.

        Features:
        - Sales analytics
        - Top products
        - Top customers
        - Top POS categories
        - Store performance
        - Active POS sessions
        - Interactive charts (bar & pie)
        - Session-based filtering
        - Today, Week, Month, Year filters
        - Notifications for new orders
        - Store sales comparison (month & year)
        - Top selling product history
        - Payment methods overview
        - Dark and light mode support

        Designed for better business decision-making directly from POS.
    """,
    'version': "19.0.3.0",
    'sequence': 10,
    'author': "Vishnu Sasikumar",
    'category': 'Point of Sale',
    'depends': ["point_of_sale"],
    'assets': {
        'web.assets_backend': [
            "https://cdn.jsdelivr.net/npm/chart.js",
            "pos_sales_dashboard/static/src/js/pos_dashboard.js",
            "pos_sales_dashboard/static/src/xml/pos_dashboard.xml",
            "pos_sales_dashboard/static/src/css/pos_dashboard.css",
        ],
    },
    'data': [
        "views/dashboard_view.xml",
    ],
    'images': ['static/description/banner.png'],
    'license': "LGPL-3",
    'installable': True,
    'application': True,
    'auto_install': False,
}