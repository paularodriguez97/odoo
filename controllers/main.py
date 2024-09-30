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
            return "Error: El estado no coincide. Posible intento de ataque."   #ponerlo en ingles

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

         # Guardar los datos en el modelo cron.trigger
        http.request.env['cron.trigger'].sudo().create_access_token(access_token)
        http.request.env['cron.trigger'].sudo().get_access_token(mode="default", access_token=access_token)

        return redirect(f'{base_url}/web#action=266&model=linkedin.candidate&view_type=list&cids=1&menu_id=200')     #Validar urls correctas


    @http.route('/add/hr_recruitment', auth='public', website=True)
    def linkedin_add_recruitment(self, **kw):
        # Guardar los datos en el modelo cron.trigger
        http.request.env['cron.trigger'].sudo().get_access_token(mode="hr")
        base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')

        return redirect(f'{base_url}/web?debug=assets%2Ctests#action=216&model=hr.job&view_type=kanban&cids=1&menu_id=142')
