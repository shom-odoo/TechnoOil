from odoo import fields, models, api
from odoo.exceptions import ValidationError

class sale_order_advance_payment_wizard(models.Model):
    _name = "sale.order.advance.payment.wizard"

    amount = fields.Float("Amount", default=0)
    date = fields.Datetime("Date")
    journal_id = fields.Many2one(comodel_name='account.journal')
    # sale_order_id = fields.Many2one(comodel_name='sale.order')

    def _get_sales_order(self):
        sales_order_id = self.env.context.get('active_id')
        sales_order = self.env['sale.order'].search(domain=[('id', '=', sales_order_id)], limit=1)
        return sales_order

    def _validate_down_payment(self, sales_order, down_payment_amount):
        total = down_payment_amount
        for prev_down_payment in sales_order.advance_payment_ids:
            total += prev_down_payment.amount

        if total > sales_order.amount_total:
            return False
        return True
    @api.model
    def create(self, vals):
        sales_order=self._get_sales_order()
        if not self._validate_down_payment(sales_order, vals['amount']):
            raise ValidationError("You have more outstanding payments for this customer than the receivables related to this sale order. Please create the payment manually if you require to link it to another sales order.")

        payment_vals = {
            'payment_type': 'inbound',  # 'inbound' for customer payment, 'outbound' for vendor payment
            'partner_type': 'customer',  # 'customer' for customer payment, 'supplier' for vendor payment
            'partner_id': sales_order.partner_id.id,  # ID of the customer or vendor
            'amount': vals['amount'],  # Payment amount
            'destination_journal_id': vals['journal_id'],  # ID of the journal where the payment will be registered
            'payment_date': vals['date'],  # Date of the payment
            'sale_order_id':sales_order.id
        }
        payment = self.env['account.payment'].create(payment_vals)
        payment.action_post()
        return super().create(vals)
