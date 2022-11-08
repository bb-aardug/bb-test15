# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models, _


class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    x_aa_bb_product_field_ids = fields.Many2many('product.field',
                                                 string='Product Fields')
    x_aa_bb_operation_id = fields.Many2one('stock.move.line', string="Operation")

    @api.model
    def create(self, vals):
        """
            Assign value to Product fields on basis of product
        """
        product = self.env['product.product'].browse(vals.get('product_id'))
        vals.update({'x_aa_bb_product_field_ids': [
            (0, 0, {'x_aa_bb_name': line.x_aa_bb_name, 'x_aa_bb_maximum':
                line.x_aa_bb_maximum, 'x_aa_bb_minimum': line.x_aa_bb_minimum})
            for line in product.x_aa_bb_product_field_ids]})
        return super(ProductionLot, self).create(vals)

    def write(self, vals):
        """
            if product is changed then its update product fields acc to
            that product
        """
        res = super(ProductionLot, self).write(vals)
        product_field = self.x_aa_bb_product_field_ids.filtered(
            lambda x: x.x_aa_bb_name == 'Regel 7 Land van Herkomst') \
            if self.x_aa_bb_product_field_ids else False
        for record in self:
            if 'product_id' in vals.keys():
                product = self.env['product.product']. \
                    browse(vals.get('product_id'))
                record.write({'x_aa_bb_product_field_ids': [
                    (
                        0, 0,
                        {'x_aa_bb_name': line.name,
                         'x_aa_bb_maximum': line.maximum,
                         'x_aa_bb_minimum': line.minimum})
                    for line in
                    product.x_aa_bb_product_field_ids]})
        return res

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """
            Assign Empty List to Product Fields
        """
        self.x_aa_bb_product_field_ids = []
