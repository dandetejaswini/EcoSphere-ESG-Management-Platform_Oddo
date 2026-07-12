{
    'name': 'EcoSphere ESG',
    'version': '1.0',
    'category': 'Sustainability',
    'summary': 'Environmental, Social, and Governance Tracking',
    'depends': ['base', 'hr'],
   'data': [
        'security/ir.model.access.csv',
        'views/esg_views.xml',
        'data/esg_demo_data.xml',
    ],
    'installable': True,
    'application': True,
}
