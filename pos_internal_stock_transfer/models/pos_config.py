from odoo import models, api, fields, _
import pytz
from dateutil.relativedelta import relativedelta


class PosConfig(models.Model):
    _inherit = 'pos.config'

    allow_send_stock = fields.Boolean(string="Allow Send Stock",help="To enable the send stock button in the pos")


    # To create the internal transfers called in js
    def action_send_stock(self, picking_data, dest_warehouse_id):
        warehouse_id = self.picking_type_id.warehouse_id
        dest_warehouse_id = self.env['stock.warehouse'].sudo().browse(int(dest_warehouse_id))
        move_list = []
        for data in picking_data:
            pid = int(data['pid'])
            product = self.env['product.product'].sudo().browse(pid)
            move_list.append((0, 0, {
                'description_picking': 'POS Send Stock',
                'product_uom': product.uom_id.id,
                'product_id': pid,
                'product_uom_qty': int(data['qty']),
                'quantity':int(data['qty']),
                'company_id': self.env.company.id,
                'location_id': warehouse_id.lot_stock_id.id,
                'location_dest_id': dest_warehouse_id.lot_stock_id.id,
                'date': fields.Date.today(),
            }))
        res = self.env['stock.picking'].sudo().create({
            'partner_id': self.env.user.partner_id.id,
            'picking_type_id': warehouse_id.int_type_id.id,
            'location_id': warehouse_id.lot_stock_id.id,
            'location_dest_id': dest_warehouse_id.lot_stock_id.id,
            'scheduled_date': fields.Datetime.now(),
            'note': 'From POS Send Stock',
            'move_ids': move_list,

        })
        # trigger the transfer confirm button
        res.sudo().button_validate()
        return res.name