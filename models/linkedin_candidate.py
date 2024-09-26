from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LinkedInCandidate(models.Model):
    _name = 'linkedin.candidate'
    _description = 'LinkedIn Candidate'

    name = fields.Char(string='Name')
    profile_url = fields.Char(string='LinkedIn Profile URL')
    email = fields.Char(string='Email')
    resume = fields.Text(string='Resume')
    job_id = fields.Many2one('hr.job', string='Applied Job')

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
            existing_candidate = self.env['linkedin.candidate'].search([
                '|',  # Condición OR
                ('email', '=', candidate['email']),
                ('profile_url', '=', candidate['linkedinProfile'])
            ], limit=1)

            if not existing_candidate:
                self.env['linkedin.candidate'].create({
                    'name': candidate['fullName'],
                    'profile_url': candidate['linkedinProfile'],
                    'email': candidate['email'],
                    'resume': candidate['resume'],
                })
            else:
                raise ValidationError(f"The candidate {candidate['fullName']} already exists.")

    # Guarda los datos de los candidatos de LinkedIn en el modelo hr.applicant de Odoo.
    def save_candidates_to_hr_recruitment(self, candidates_data, job_id):
        for candidate in candidates_data:
            existing_applicant = self.env['hr.applicant'].search([
                ('email_from', '=', candidate['email'])
            ], limit=1)

            if not existing_applicant:
                self.env['hr.applicant'].create({
                    'name': candidate['fullName'],
                    'partner_name': candidate['fullName'],
                    'email_from': candidate['email'],
                    'description': candidate['resume'],
                    'job_id': job_id,  # ID de la oferta de trabajo en Odoo
                })
            else:
                raise ValidationError(f"The applicant {candidate['fullName']} already exists in hr.recruitment.")

