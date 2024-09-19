{
    'name': 'LinkedIn Integration',
    'summary': 'Application to integrate linking data to the Odoo recruitment application.',
    'version': '1.0',
    'category': 'Human Resources/Recruitment',
    'author': 'Paula Rodriguez - Nivelics',
    'depends': ['hr_recruitment'],
    'data': [
        'data/cron.xml'
        # 'security/hr_recruitment_security.xml',
        # 'data/digest_data.xml',
        # 'views/hr_recruitment_views.xml',
        # 'wizard/applicant_send_mail_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
     'assets': {
        # 'web.assets_backend': [
        #     'hr_recruitment/static/src/**/*.js',
        #     'hr_recruitment/static/src/**/*.scss',
        # ],
    },
}
