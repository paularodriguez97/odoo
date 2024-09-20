{
    'name': 'LinkedIn Integration',
    'version': '1.0',
    'summary': 'Application to integrate linking data to the Odoo recruitment application.',
    'category': 'Human Resources/Recruitment',
    'author': 'Paula Rodriguez - Nivelics',
    'depends': ['hr_recruitment'],
    'data': [
        'data/cron.xml',
        'security/ir.model.access.csv',
        'views/linkedin_candidates.xml'
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    # 'assets': {
        # 'web.assets_backend': [
        #     'hr_recruitment/static/src/**/*.js',
        #     'hr_recruitment/static/src/**/*.scss',
        # ],
    # },
}
