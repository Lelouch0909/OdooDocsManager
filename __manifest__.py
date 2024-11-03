{
    'name': 'Enspd Dms',
    'version': '1.0',
    'summary': 'Module de gestion des documents personnalisé basé sur DMS pour l Enspd',
    'description': 'Ce module personnalise la gestion des documents en utilisant certaines fonctionnalités de DMS',
    'author': 'Lontsi Hermann',
    'depends': ['base', 'web_digital_sign', 'web'],
    'data': [
        'security/model_administration.xml',
        'security/ir.model.access.csv',
        'views/document_property_views.xml',
        'views/document_menu.xml',

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'category': 'Administration',
    'auto_install': True,

}
