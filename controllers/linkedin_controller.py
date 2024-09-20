# from odoo import http

# class LinkedInController(http.Controller):
#     @http.route('/linkedin/test', auth='public', website=True)
#     def test(self):
#         return "Ruta de prueba funciona"


from odoo import http
import requests

class LinkedInController(http.Controller):
    @http.route('/linkedin/auth', auth='public', website=True)
    def linkedin_auth(self):
        client_id = '78xcvk64pn071n'
        redirect_uri = 'http://localhost:8069/linkedin/callback'
        linkedin_auth_url = f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope=r_liteprofile r_emailaddress"
        return http.redirect(linkedin_auth_url)

    @http.route('/linkedin/callback', auth='public', website=True)
    def linkedin_callback(self, **kw):
        code = kw.get('code')
        client_id = '78xcvk64pn071n'
        client_secret = 'B8QbIaXMRGN9kZL1'
        redirect_uri = 'http://localhost:8069/linkedin/callback'

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

        # Aquí puedes hacer más llamadas a LinkedIn API para obtener datos
        # Por ejemplo, obtener el perfil del usuario autenticado
        profile_url = 'https://api.linkedin.com/v2/me'
        headers = {'Authorization': f'Bearer {access_token}'}
        profile_response = requests.get(profile_url, headers=headers)
        profile_data = profile_response.json()

        # Crear un registro en el modelo linkedin.candidate
        request.env['linkedin.candidate'].sudo().create({
            'name': profile_data.get('localizedFirstName', '') + ' ' + profile_data.get('localizedLastName', ''),
            # Puedes añadir más campos según la estructura de profile_data
        })

        return f"Datos obtenidos: {profile_data}"
