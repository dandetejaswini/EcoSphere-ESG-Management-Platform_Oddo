{
    'name': 'EcoSphere: ESG Management Platform',
    'version': '1.0',
    'category': 'Management',
    'summary': 'Full ESG Tracking and Gamification Platform',
    'depends': ['base', 'hr', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/esg_views.xml',
    ],
    'installable': True,
    'application': True,
}