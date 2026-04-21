from odoo import models, api, fields, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def action_get_warehouses(self):
        rec = self.env['stock.warehouse'].sudo().search([])
        warehouses = [{'id': warehouse.id, 'name': warehouse.name} for warehouse in rec]
        return warehouses
