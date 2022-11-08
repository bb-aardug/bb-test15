# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    x_aa_bb_order_date = fields.Date(string="SO. Date")
    x_aa_bb_customer_ref_no = fields.Char(string='SO. Line Ref.')
    
    # @api.multi
    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        print("res==",res)
        res.update({
                    'x_aa_bb_order_date':self.x_aa_bb_order_date,
                    'x_aa_bb_customer_ref_no':self.x_aa_bb_customer_ref_no,
                    'x_aa_bb_sale_line_id':self.id
                })
        return res

class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    @api.model
    def _get_invoice_line_key_cols(self):
        fields = [
            'name','origin', 'discount', 'invoice_line_tax_ids', 'price_unit',
            'product_id', 'account_id', 'account_analytic_id',
            'uom_id','x_aa_bb_order_date','x_aa_bb_customer_ref_no','sale_line_id'
        ]
        for field in ['sale_line_ids']:
            if field in self.env['account.move.line']._fields:
                fields.append(field)
        return fields


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    _order = "x_aa_bb_sale_line_id"

    x_aa_bb_order_date = fields.Date(string="SO. Date")
    x_aa_bb_customer_ref_no = fields.Char(string='SO. Line Ref.')
    x_aa_bb_sale_line_id = fields.Integer()


class StockMove(models.Model):
    _inherit = "stock.move"

    x_aa_bb_order_date = fields.Date(string="SO. Date")
    x_aa_bb_customer_ref_no = fields.Char(string='SO. Line Ref.')


    @api.model
    def create(self, vals):
        res = super(StockMove, self).create(vals)
        sale_line = res.sale_line_id
        for line in sale_line:
            if res['product_id'] == line.product_id:
                res.update({
                        'x_aa_bb_order_date':line.x_aa_bb_order_date,
                        'x_aa_bb_customer_ref_no':line.x_aa_bb_customer_ref_no
                    })
        return res


class StockMoveLinesInh(models.Model):
    _inherit = "stock.move.line"

    x_aa_bb_order_date = fields.Date(string="SO. Date")
    x_aa_bb_customer_ref_no = fields.Char(string='SO. Line Ref.')

    @api.model
    def create(self, vals):
        res = super(StockMoveLinesInh, self).create(vals)
        sale = res['picking_id'].sale_id
        if sale:
            sale_line = self.env['sale.order.line'].search([('order_id','=',sale.id)])
            for line in sale_line:
                if res['product_id'] == line.product_id:
                    res.update({
                        'x_aa_bb_order_date':line.x_aa_bb_order_date,
                        'x_aa_bb_customer_ref_no':line.x_aa_bb_customer_ref_no
                    })
        return res