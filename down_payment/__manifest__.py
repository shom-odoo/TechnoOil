{
'name': 'Down Payment Magic',
'depends' : ['base', 'sale_management', 'account'],
'data' : ['security/ir.model.access.csv','views/sale_order_views.xml', 'views/sale_order_advance_payment_views.xml', 'views/account_payment_views.xml'],
'application': False,
'license': 'LGPL-3',
}