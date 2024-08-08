from odoo import fields, models


class account_payment(models.Model):
    _inherit = "account.payment"
    sale_order_id = fields.Many2one(comodel_name='sale.order')

