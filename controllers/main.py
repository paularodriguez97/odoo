from odoo import http
from werkzeug.utils import redirect
import requests
import urllib.parse
import random

class LinkedInCandidate(http.Controller):
    @http.route('/linkedin/auth', auth='public', type='http', website=True)
    def linkedin_auth(self):
        base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        client_id = '78mzayek1quywb'
        redirect_uri = f'{base_url}/linkedin/callback'
        redirect_uri_codified = urllib.parse.quote(redirect_uri)
        state = str(random.randint(100000, 999999))
        http.request.session['linkedin_state'] = state
        linkedin_auth_url = f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&state={state}&client_id={client_id}&redirect_uri={redirect_uri_codified}&scope=openid profile email"
        return redirect(linkedin_auth_url)

    @http.route('/linkedin/callback', auth='public', website=True)
    def linkedin_callback(self, **kw):
        original_state = http.request.session.get('linkedin_state')
        received_state = kw.get('state')

        # Validar el estado para prevenir ataques de tipo CSRF
        if original_state != received_state:
            return "Error: El estado no coincide. Posible intento de ataque."

        code = kw.get('code')
        client_id = '78mzayek1quywb'
        client_secret = 'WPL_AP1.9WVE4Fkr7Jyie0aa.WX/tLw=='
        base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        redirect_uri = f'{base_url}/linkedin/callback'

        # Intercambiar el código por el token de acceso
        token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
        token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret,
        }
        response = requests.post(token_url, data=token_data)
        token_json = response.json()
        access_token = token_json.get('access_token')

        # Obtener el perfil del usuario autenticado
        profile_url = 'https://api.linkedin.com/v2/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        profile_response = requests.get(profile_url, headers=headers)
        candidates_data = profile_response.json()

        # candidates_data = {
        #     "localizedFirstName": "John",
        #     "localizedLastName": "Doe",
        #     "id": "abcd1234",
        #     "profilePicture": {
        #         "displayImage": "https://media-exp1.licdn.com/dms/image/C4E03AQElc_Jn7X5k/photo.jpg"
        #     },
        #     "headline": "Software Engineer at XYZ Corp",
        #     "emailAddress": "johndoe@example.com"
        # }

        # candidates_data = [{
        #     'fullName': candidates_data.get('name', '') + ' ' + candidates_data.get('localizedLastName', ''),
        #     'linkedinProfile': 'https://linkedin.com/in/' + candidates_data.get('id', ''),
        #     'email': candidates_data.get('emailAddress', ''),
        #     'resume': candidates_data.get('summary', '')
        # }]

        # http.request.env['linkedin.candidate'].sudo().save_candidates(candidates_data)



        return f"Datos obtenidos1: {candidates_data} "


