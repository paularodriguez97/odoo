from odoo import models, fields, api, http
from odoo.exceptions import UserError
import requests

class CronTrigger(models.Model):
    _name = 'cron.trigger'
    _description = 'Cron trigger'

    access_token = fields.Char(string='Access Token')


    def create_access_token(self, access_token):
        if access_token:
            record = self.create({'access_token': access_token})
            return record
        raise UserError('Access token no puede ser vacío.')

    # Ejecuta el controlador de autenticación.
    def get_access_token(self, mode="default", access_token=None ):
        if access_token:
            self.sudo().write({'access_token': access_token})

        # Si no se proporciona un nuevo token, busca el registro
        if not access_token:
            record = self.search([], limit=1)  # Busca el primer registro

            if record:
                current_access_token = record.access_token
            else:
                raise UserError('No hay registros disponibles.')

        # Si current_access_token sigue vacío
            if not current_access_token:
                raise UserError('You must first perform with linkedin before executing this action.')


        # Obtener el perfil del usuario autenticado
        token_to_use = access_token if access_token else current_access_token
        profile_url = 'https://api.linkedin.com/v2/userinfo'
        headers = {'Authorization': f'Bearer {token_to_use}'}
        profile_response = requests.get(profile_url, headers=headers)
        candidates_data = profile_response.json()

        if profile_response.status_code != 200:
            raise UserError(f'Error al obtener el perfil: {profile_response.text}')


        # Realizar una búsqueda en configuración.
        config = self.env['linkedin_integration.config.form'].search([], limit=1)

        if config:
            record = config
            offer_state = record.offer_state
            max_candidates = record.max_candidates
            location_filter = record.location_filter
        else:
            offer_state = 'active'
            max_candidates = 10

        candidates_data = [
            {
                "localizedFirstName": "esq123ww",
                "localizedLastName": "eqse123ww",
                "id": "3e4sq1123www",
                "profilePicture": {
                    "displayImage": "https://ia-exwwwsp1123.licdn.com/dms/image/Cq4E03AQElc_Jn7X5k/photo.jpg"
                },
                "headline": "a Engiwwesneerq123 at XYZ Corp",
                "emailAddress": "eswwweoes@examqpl123e.com",
                "integrationContext": "urn:li:organization:2414183",
                "companyApplyUrl": "http://linkedin.com",
                "resume": "We are looking for a passionate Software Engineer to design, develop and install software solutions. Software Engineer responsibilities include gathering user requirements, defining system functionality and writing code in various languages. Our ideal candidates are familiar with the software development life cycle (SDLC) from preliminary system analysis to tests and deployment.",
                "employmentStatus": "PART_TIME",
                "externalJobPostingId": "1234",
                "listedAt": 1440716666,
                "jobPostingOperationType": "CREATE",
                "title": "Software Engineer",
                "location": "San Francisco",
                "workplaceTypes": [
                    "hybrid"
                ],
                "linkedInApplyStatus": "ENABLED",
                "jobName": "Nivelics sas",
                "jobTitle": "Desarrollador Drupal",
                "description": "Este es un trabajo de prueba para validacion.",
                "requirements": "activo"
            },
            {
                "localizedFirstName": "esq123r",
                "localizedLastName": "eqse123r",
                "id": "3e4sq1123r",
                "profilePicture": {
                    "displayImage": "https://ia-exrsp1123.licdn.com/dms/image/Cq4E03AQElc_Jn7X5k/photo.jpg"
                },
                "headline": "a Engiesnererq123 at XYZ Corp",
                "emailAddress": "eseoers@examqpl123e.com",
                "integrationContext": "urn:li:organization:2414183",
                "companyApplyUrl": "http://linkedin.com",
                "resume": "We are looking for a passionate Senior Software Engineer to design, develop and install software solutions. Software Engineer responsibilities include gathering user requirements, defining system functionality and writing code in various languages. Our ideal candidates are familiar with the software development life cycle (SDLC) from preliminary system analysis to tests and deployment.",
                "employmentStatus": "PART_TIME",
                "externalJobPostingId": "789",
                "listedAt": 1440716666,
                "jobPostingOperationType": "CREATE",
                "title": "Senior Software Engineer",
                "location": "Colombia",
                "linkedInApplyStatus": "ENABLED",
                "jobName": "Emergya",
                "jobTitle": "Desarrollador Drupal",
                "description": "Este es un trabajo de prueba para validacion.",
                "requirements": "activo"
            }
        ]

        if location_filter == False:
            filtered_candidates = [candidate for candidate in candidates_data if candidate.get('linkedInApplyStatus', '').lower() == offer_state.lower()]
        else:
            filtered_candidates = [candidate for candidate in candidates_data if candidate.get('linkedInApplyStatus', '').lower() == offer_state.lower() and candidate.get('location', '').strip().lower() == location_filter.strip().lower()]

        limited_candidates = filtered_candidates[:max_candidates]
        candidates_data_transformed = []

        for candidate in limited_candidates:
            transformed_candidate = {
                'fullName': candidate.get('localizedFirstName', '') + ' ' + candidate.get('localizedLastName', ''),
                'linkedinProfile': 'https://linkedin.com/in/' + candidate.get('id', ''),
                'email': candidate.get('emailAddress', ''),
                'resume': candidate.get('resume', ''),
                'jobName': candidate.get('jobName', ''),
                'jobTitle': candidate.get('jobTitle', ''),
                'department': candidate.get('location', ''),
                'jobDesription': candidate.get('description', ''),
                'requirements': candidate.get('requirements', '')
            }
            candidates_data_transformed.append(transformed_candidate)

        linkedin_candidate_model = self.env['linkedin.candidate'].sudo()
        if mode == "default":
            linkedin_candidate_model.save_candidates(candidates_data_transformed)
        elif mode == "hr":
            linkedin_candidate_model.save_candidates_to_hr_recruitment(candidates_data_transformed)