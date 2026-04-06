from odoo import models,fields

class PosConfig(models.Model):
    _inherit = 'pos.config'

    salesperson_ids = fields.Many2many('hr.employee','hr_employee_pos_config_salesperson_rel',string='Salespersons',help="Select employees to be available as salespersons in the POS popup.")
    salesperson_compulsory = fields.Boolean(string='Salesperson Mandatory',help="Enable this to make salesperson selection mandatory in the POS.")
    