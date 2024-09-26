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
    def get_access_token(self, access_token=None):
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
                raise UserError('Access token no definido y no existe uno guardado en la base de datos.')


        # Obtener el perfil del usuario autenticado
        token_to_use = access_token if access_token else current_access_token
        profile_url = 'https://api.linkedin.com/v2/userinfo'
        headers = {'Authorization': f'Bearer {token_to_use}'}
        profile_response = requests.get(profile_url, headers=headers)
        candidates_data = profile_response.json()

        if profile_response.status_code != 200:
            raise UserError(f'Error al obtener el perfil: {profile_response.text}')

        candidates_data = {
            "localizedFirstName": "esq12",
            "localizedLastName": "eqse12",
            "id": "3e4sq112",
            "profilePicture": {
                "displayImage": "https://ia-exsp112.licdn.com/dms/image/Cq4E03AQElc_Jn7X5k/photo.jpg"
            },
            "headline": "a Engiesneerq12 at XYZ Corp",
            "emailAddress": "eseoes@examqpl12e.com"
        }

        candidates_data = [{
            'fullName': candidates_data.get('name', '') + ' ' + candidates_data.get('localizedLastName', ''),
            'linkedinProfile': 'https://linkedin.com/in/' + candidates_data.get('id', ''),
            'email': candidates_data.get('emailAddress', ''),
            'resume': candidates_data.get('summary', '')
        }]

        linkedin_candidate_model = self.env['linkedin.candidate'].sudo()
        linkedin_candidate_model.save_candidates(candidates_data)