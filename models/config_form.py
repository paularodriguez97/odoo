from odoo import models, fields, api
from odoo.exceptions import UserError
class ConfigForm(models.Model):
    _name = 'linkedin_integration.config.form'
    _description = 'Configuration Form'

    # Filtros y Opciones de Migración
    offer_state = fields.Selection([
        ('enabled', 'Enabled'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed')
    ], string="Select Bid Status", default='enabled')
    max_candidates = fields.Integer(string="Candidates by Offer", default=10)
    location_filter = fields.Char(string="Location Filter", default='Colombia')

    @api.model
    def default_get(self, fields):
        res = super(ConfigForm, self).default_get(fields)
        # Buscar el último registro existente
        existing_record = self.search([], limit=1, order='id desc')
        if existing_record:
            # Cargar los valores del último registro
            res.update({
                'offer_state': existing_record.offer_state,
                'max_candidates': existing_record.max_candidates,
                'location_filter': existing_record.location_filter,
            })
        return res

    @api.model_create_multi
    def create(self, vals_list):
        vals_list = [vals.copy() for vals in vals_list]

        # Buscar si ya existe un registro
        existing_record = self.search([], limit=1)
        if existing_record:
            # Si existe, actualizarlo en lugar de crear uno nuevo
            existing_record.write(vals_list[0])
            return existing_record
        else:
            # Si no existe, procede a crear uno nuevo
            return super(ConfigForm, self).create(vals_list)

