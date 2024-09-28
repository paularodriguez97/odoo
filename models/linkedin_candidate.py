from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LinkedInCandidate(models.Model):
    _name = 'linkedin.candidate'
    _description = 'LinkedIn Candidate'

    job_name = fields.Char(string='Job Name')
    job_title = fields.Char(string="Job Title")
    department_id = fields.Many2one('hr.department', string="Department")
    job_description = fields.Html(string="Description")
    requirements = fields.Text(string="Requirements")

    name = fields.Char(string='Name')
    profile_url = fields.Char(string='LinkedIn Profile URL')
    email = fields.Char(string='Email')
    resume = fields.Text(string='Resume')

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

            # if not existing_candidate:
            self.env['linkedin.candidate'].create({
                'name': candidate['fullName'],
                'profile_url': candidate['linkedinProfile'],
                'email': candidate['email'],
                'resume': candidate['resume'],
                'job_title': candidate['jobTitle']
            })
            # else:
            #     raise ValidationError(f"The candidate {candidate['fullName']} already exists.")

    # Guarda los datos de los candidatos de LinkedIn en el modelo hr.applicant de Odoo.
    def save_candidates_to_hr_recruitment(self, candidates_data):

        for candidate in candidates_data:
            existing_applicant = self.env['hr.job'].search([
                ('name', '=', candidate['jobName'])
            ], limit=1)

            if not existing_applicant:
                self.env['hr.job'].create({
                    'name': candidate['jobName'],
                    'description': candidate['jobDesription'],
                    # 'requirements': candidate['requirements']
                })
            else:
                raise ValidationError(f"The job {candidate['jobName']} already exists in hr.recruitment.")

