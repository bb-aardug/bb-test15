# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    x_aa_bb_visible_price = fields.Boolean(string="View Price", help="Product Sale Price View in Picking Slip")


class StockMove(models.Model):
    _inherit = "stock.move"

    x_aa_bb_product_desc = fields.Char(string="Description")

    @api.model
    def create(self, vals):
        res = super(StockMove, self).create(vals)
        sale_line = res.sale_line_id
        for line in sale_line:
            if res['product_id'] == line.product_id:
                res.update({
                        'x_aa_bb_product_desc':line.name,
                    })
        return res


class StockMoveLinesInherit(models.Model):
    _inherit = "stock.move.line"


    x_aa_bb_product_desc = fields.Char(string="Description")

    @api.model
    def create(self, vals):
        res = super(StockMoveLinesInherit, self).create(vals)
        sale = res['picking_id'].sale_id
        if sale:
            sale_line = self.env['sale.order.line'].search([('order_id','=',sale.id)])
            for line in sale_line:
                if res['product_id'] == line.product_id:
                    res.update({
                            'x_aa_bb_product_desc':line.name,
                        })
        return res