from odoo import models, fields, api

class ConfigForm(models.TransientModel):
    _name = 'linkedin_integration.config.form'
    _description = 'Configuration Form'

    # Configuración del Cron
    execution_frequency = fields.Selection([
        ('15', 'Cada 15 minutos'),
        ('30', 'Cada 30 minutos'),
        ('hourly', 'Cada hora'),
        ('daily', 'Diariamente'),
        ('weekly', 'Semanalmente'),
        ('monthly', 'Mensualmente')
    ], string="Frecuencia de Ejecución", required=True, default='hourly')
    cron_state = fields.Selection([
        ('active', 'Activo'),
        ('inactive', 'Inactivo')
    ], string="Estado del Cron", default='active')

    # Filtros y Opciones de Migración
    offer_state = fields.Selection([
        ('active', 'Activas'),
        ('in_progress', 'En Proceso'),
        ('closed', 'Cerradas')
    ], string="Seleccionar Estado de las Ofertas", default='active')
    max_candidates = fields.Integer(string="Candidatos por Oferta", default=10)
    location_filter = fields.Char(string="Filtro de Ubicación")

    def action_save(self):
        # Lógica para guardar la configuración
        pass

    def action_cancel(self):
        # Lógica para cancelar la acción
        pass