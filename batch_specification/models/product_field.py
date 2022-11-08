# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models, _


class ProductField(models.Model):
    _name = 'product.field'
    _description = 'Product Field'

    x_aa_bb_name = fields.Char(string='Name', readonly=True)
    x_aa_bb_maximum = fields.Char(string='Maximum', readonly=True)
    x_aa_bb_minimum = fields.Char(string="Minimum", readonly=True)
    x_aa_bb_actual_value = fields.Char(string='Actual Value')

