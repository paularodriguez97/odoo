from odoo import models, fields

class ConfigForm(models.TransientModel):
    _name = 'linkedin_integration.config.form'
    _description = 'Configuration Form'

    field_one = fields.Char(string='Field One')
    field_two = fields.Integer(string='Field Two')


    def action_save(self):
        # Tu lógica aquí
        field_one = self.field_one
        field_two = self.field_two
        # Llamar a tu controlador con la información
        self.env['your_module.your_controller_model'].process_data(field_one, field_two)
