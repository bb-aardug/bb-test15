# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_aa_bb_product_field_ids = fields.Many2many('product.field.config',
                                                 string='Product Fields')

    @api.model
    def create(self, vals):
        """
            Assign Product Fields
        """
        res = super(ProductTemplate, self).create(vals)
        config_field_ids = self.env['product.field.config'].search\
            ([('x_aa_bb_check_required', '=', True)])
        res.x_aa_bb_product_field_ids = config_field_ids.ids
        return res
