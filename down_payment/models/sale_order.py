from odoo import fields, models


class sale_order(models.Model):
    _inherit = 'sale.order'
    advance_payment_ids = fields.One2many(comodel_name='account.payment', inverse_name='sale_order_id', readonly=True)

