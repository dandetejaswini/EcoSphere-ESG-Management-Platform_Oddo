from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    esg_enable_notifications = fields.Boolean(
        string="Notification System", 
        config_parameter='ecosphere_esg.enable_notifications'
    )
    esg_enable_auto_emission = fields.Boolean(
        string="Auto Emission Calculation", 
        config_parameter='ecosphere_esg.enable_auto_emission'
    )
    esg_enable_evidence_req = fields.Boolean(
        string="Evidence Requirement", 
        config_parameter='ecosphere_esg.enable_evidence_req'
    )
    esg_enable_badge_auto = fields.Boolean(
        string="Badge Auto-Award", 
        config_parameter='ecosphere_esg.enable_badge_auto'
    )