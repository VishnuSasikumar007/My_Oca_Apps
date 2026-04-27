from odoo import models, api, fields, _
import pytz
from dateutil.relativedelta import relativedelta


class PosConfig(models.Model):
    _inherit = 'pos.config'

    pos_shop_image = fields.Binary(string="POS Shop Image", help="Upload an image to display in the POS dashboard kanban view.",attachment=True)


    