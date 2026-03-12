from odoo import fields, models, api,_

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # To get the product qty based on the location
    def tmp_action_get_warehouse_quant(self, pos_config_id):
        self.ensure_one()
        if self.type != 'consu':
            return 100000
        pos_config = self.env['pos.config'].browse(pos_config_id)
        warehouse = pos_config.picking_type_id.warehouse_id

        if not warehouse:
            return 0

        location = warehouse.lot_stock_id
        product_id = self.env['product.product'].search([('product_tmpl_id','=',self.id)],limit=1)
        quant = self.env['stock.quant'].search([
            ('product_id', '=', product_id.id),
            ('location_id', '=', location.id),
        ])
        return sum(quant.mapped('available_quantity'))

