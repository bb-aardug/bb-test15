# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError


class ProductFieldConfig(models.Model):
    _name = 'product.field.config'
    _description = 'Product Field Config'
    _rec_name = "x_aa_bb_name"

    x_aa_bb_name = fields.Char(string='Name')
    x_aa_bb_maximum = fields.Char(string='Maximum')
    x_aa_bb_minimum = fields.Char(string="Minimum")
    x_aa_bb_check_required = fields.Boolean(string="Required")
    x_aa_bb_product_id = fields.Many2one('product.template')

    @api.model
    def create(self, vals):
        """
            Used for Raising User Error if fields are empty
        """
        if vals['x_aa_bb_check_required'] == True:
            if vals['x_aa_bb_maximum'] == False or \
                    vals['x_aa_bb_minimum'] == False:
                raise UserError(_('Please fill all fields.'))
            else:
                return super(ProductFieldConfig, self).create(vals)
        else:
            return super(ProductFieldConfig, self).create(vals)

    def write(self, vals):
        """
            Used for Raising User Error  if fields are empty  and set flag
        """
        flag = 0
        if vals.get('x_aa_bb_check_required'):
            if vals['x_aa_bb_check_required'] == True:
                if vals.get('x_aa_bb_maximum'):
                    if vals['x_aa_bb_maximum'] == False:
                        flag = 1
                elif self.x_aa_bb_maximum == False:
                    flag = 1
                if vals.get('x_aa_bb_minimum'):
                    if vals['x_aa_bb_minimum'] == False:
                        flag = 1
                elif self.x_aa_bb_minimum == False:
                    flag = 1
        elif self.x_aa_bb_check_required == True:
            if vals.get('x_aa_bb_maximum'):
                if vals['x_aa_bb_maximum'] == False:
                    flag = 1
            if vals.get('x_aa_bb_minimum'):
                if vals['x_aa_bb_minimum'] == False:
                    flag = 1
        if flag == 1:
            raise UserError(_('Please fill all fields'))
        else:
            return super(ProductFieldConfig, self).write(vals)






