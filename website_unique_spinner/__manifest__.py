# -*- coding: utf-8 -*-

{
    'name': 'Website Unique Spinner',
    'version': '19.0.1.0.0',
    'summary': 'Unique animated loading spinner for the Odoo website',
    'description': """
Website Unique Spinner
======================

Replaces the default loading experience of your Odoo website with a
distinctive, fully CSS-animated orbit spinner.

Features
--------
- Full-screen preloader shown while the website page and assets load.
- Smooth fade-out once the page is ready.
- Optional page-transition spinner for internal website navigation.
- Automatic fallback timeout to prevent the spinner from getting stuck.
- Pure CSS animation with no GIF or PNG dependency.
- Fully themeable using CSS variables.
- Zero third-party JavaScript dependencies.
- Lightweight and optimized for frontend performance.

Works on all Odoo website/frontend pages and does not affect the backend.
""",
    'author': 'Vishnu Sasikumar',
    'license': 'LGPL-3',
    'category': 'Website',
    'depends': [
        'website',
    ],
    'data': [
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_unique_spinner/static/src/css/spinner.css',
            'website_unique_spinner/static/src/js/spinner.js',
        ],
    },
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}