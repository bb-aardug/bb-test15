# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################


from odoo import api, fields, models, _


class ProductTemplateInh(models.Model):
    _inherit = "product.template"

    x_aa_bb_text_block1 = fields.Text('Tekst Block 1', translate=True)
    x_aa_bb_text_block2 = fields.Text('Tekst Block 2', translate=True)
