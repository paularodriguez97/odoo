from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LinkedInCandidate(models.Model):
    _name = 'linkedin.candidate'
    _description = 'LinkedIn Candidate'

    # Datos de oferta de trabajo
    job_name = fields.Char(string='Job Name')
    job_title = fields.Char(string="Job Title")
    department_id = fields.Many2one('hr.department', string="Department")
    job_description = fields.Html(string="Description")
    requirements = fields.Text(string="Requirements")

    # Datos de solicitante
    name = fields.Char("Subject / Application")
    partner_name = fields.Char("Applicant's Name")
    email_from = fields.Char("Email", size=128)
    partner_phone = fields.Char("Phone", size=32)
    partner_mobile = fields.Char("Mobile", size=32)
    linkedin_profile = fields.Char('LinkedIn Profile')
    salary_expected = fields.Float("Expected Salary")
    salary_proposed = fields.Float("Proposed Salary")
    description = fields.Html("Description")
    # type_id = fields.Many2one('hr.recruitment.degree', "Degree")   #revisar



    # Redirige al usuario a la URL de autenticación de LinkedIn.
    def action_linkedin_auth(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/linkedin/auth',
            'target': 'new',
        }

    # Guarda los datos de los candidatos de LinkedIn en el modelo linkedin.candidate.
    @api.constrains('candidates_data')
    def save_candidates(self, candidates_data):
        if not isinstance(candidates_data, list):
            raise ValidationError("Candidate data should be a list.")

        for candidate in candidates_data:
            # existing_candidate = self.env['linkedin.candidate'].search([
            #     '|',  # Condición OR
            #     ('email', '=', candidate['email']),
            #     ('profile_url', '=', candidate['linkedinProfile'])
            # ], limit=1)

            if not existing_candidate:
                self.env['linkedin.candidate'].create({
                    'partner_name': candidate['partner_name'],
                    'linkedin_profile': candidate['linkedin_profile'],
                    'email_from': candidate['email_from'],
                    'description': candidate['description'],
                    'job_title': candidate['jobTitle']
                })
            # else:
            #     raise ValidationError(f"The candidate {candidate['fullName']} already exists.")

    # Guarda los datos de los candidatos de LinkedIn en el modelo hr.applicant de Odoo.
    def save_candidates_to_hr_recruitment(self, candidates_data):

        for candidate in candidates_data:
            existing_job = self.env['hr.job'].search([
                ('name', '=', candidate['jobName'])
            ], limit=1)

            existing_applicant = self.env['hr.applicant'].search([
                ('partner_name', '=', candidate['partner_name'])
            ], limit=1)

            if not existing_job:
                self.env['hr.job'].create({
                    'name': candidate['jobName'],
                    'description': candidate['jobDesription'],
                    # 'requirements': candidate['requirements']   #revisar donde se llena este campo, si no eliminar
                })

            if not existing_applicant:
                job_id = self.env['hr.job'].search([('name', '=', candidate['jobName'])], limit=1)
                stage_id = self.env['hr.recruitment.stage'].search([], limit=1)
                self.env['hr.applicant'].create({
                    'name': candidate['jobName'],
                    'partner_name': candidate['partner_name'],
                    'email_from': candidate['email_from'],
                    'partner_phone': candidate['partner_phone'],
                    'partner_mobile': candidate['partner_mobile'],
                    'linkedin_profile': candidate['linkedin_profile'],
                    'salary_expected': candidate['salary_expected'],
                    'salary_proposed': candidate['salary_proposed'],
                    'description': candidate['description'],
                    'job_id': job_id.id,
                    'stage_id': stage_id.id,
                    'active': True
                })


