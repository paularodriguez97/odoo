from odoo import http
from werkzeug.utils import redirect
import requests
import urllib.parse
import random

class LinkedInController(http.Controller):
    @http.route('/linkedin/auth', auth='public', type='http', website=True)
    def linkedin_auth(self):
        base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        client_id = '78xcvk64pn071n'
        redirect_uri = f'{base_url}/linkedin/callback'
        redirect_uri_codified = urllib.parse.quote(redirect_uri)
        state = str(random.randint(100000, 999999))  # Para prevenir ataques de tipo CSRF
        http.request.session['linkedin_state'] = state
        linkedin_auth_url = f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&state={state}&client_id={client_id}&redirect_uri={redirect_uri_codified}&scope=r_liteprofile r_emailaddress"
        return redirect(linkedin_auth_url)

# https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=78xcvk64pn071n&redirect_uri=http%3A%2F%2Flocalhost%3A8069%2Flinkedin%2Fcallback&scope=r_liteprofile r_emailaddress

    @http.route('/linkedin/callback', auth='public', website=True)
    def linkedin_callback(self, **kw):
        original_state = http.request.session.get('linkedin_state')
        received_state = kw.get('state')

        # Validar el estado
        if original_state != received_state:
            return "Error: El estado no coincide. Posible intento de ataque."

        code = kw.get('code')
        client_id = '78xcvk64pn071n'
        client_secret = 'B8QbIaXMRGN9kZL1'
        base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        redirect_uri = f'{base_url}/linkedin/callback'
        redirect_uri_codified = urllib.parse.quote(redirect_uri)

        # Intercambiar el código por el token de acceso
        token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
        token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,   # Validar si es con la codificada o no
            'client_id': client_id,
            'client_secret': client_secret,
        }
        response = requests.post(token_url, data=token_data)
        token_json = response.json()
        access_token = token_json.get('access_token')

        # Aquí para más llamados a LinkedIn API para obtener datos
        # Por ejemplo, obtener el perfil del usuario autenticado
        profile_url = 'https://api.linkedin.com/v2/me'
        headers = {'Authorization': f'Bearer {access_token}'}
        profile_response = requests.get(profile_url, headers=headers)
        profile_data = profile_response.json()

        # Crear un registro en el modelo linkedin.candidate
        http.request.env['linkedin.candidate'].sudo().create({
            'name': profile_data.get('localizedFirstName', '') + ' ' + profile_data.get('localizedLastName', ''),
            # Puedes añadir más campos según la estructura de profile_data
        })

        return f"Datos obtenidos: {profile_data}"
