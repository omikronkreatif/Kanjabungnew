{
    'name': 'Liter Sapi',
    'version': '14.0.1.0',
    'license': 'LGPL-3',
    'category': 'Farm',
    "sequence": 1,
    'summary': 'Manage Liter Sapi',
    'complexity': "easy",
    'author': 'AFajarR',
    'website': '',
    'depends': ['base', 'mail', 'purchase', 'peternak_sapi', 'master_sapi', 'product'],
    'data': [
            'security/ir.model.access.csv',
            'views/liter_sapi_views.xml',
            'views/data_anggota_liter_views.xml',
            'views/tps_liter_views.xml',
            'views/menu_liter_sapi.xml',
            ],
    'demo': [

            ],
    'css': [

        ],
    'qweb': [

            ],
    'images': [

            ],
    'installable': True,
    'auto_install': False,
    'application': True,
}