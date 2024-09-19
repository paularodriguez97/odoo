from odoo import models, fields

class LinkedInCandidate(models.Model):
    _name = 'linkedin.candidate'
    _description = 'LinkedIn Candidate'

    name = fields.Char(string='Name')
    profile_url = fields.Char(string='LinkedIn Profile URL')
    email = fields.Char(string='Email')
    resume = fields.Text(string='Resume')
    job_id = fields.Many2one('hr.job', string='Applied Job')

    def save_candidates_to_odoo(candidates_data):
        for candidate in candidates_data:
            self.env['linkedin.candidate'].create({
                'name': candidate['fullName'],
                'profile_url': candidate['linkedinProfile'],
                'email': candidate['email'],
                'resume': candidate['resume'],
                'job_id': job_id,  # Obtén el ID de la oferta de trabajo en Odoo
            })

