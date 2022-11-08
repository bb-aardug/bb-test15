# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models, _


class CompanyInherit(models.Model):
    _inherit = "res.company"

    xaa_aa_for_all_report = fields.Boolean("Use images for all report")

    @api.onchange('xaa_aa_for_all_report')
    def onchange_for_all_report(self):
        if self.xaa_aa_for_all_report:
            ir_model_data = self.env['ir.model.data']
            self.paperformat_id = self.env.ref(
                'custom_header_footer.paperformat_custom_header_footer').id
        else:
            paperformat_us = self.env.ref('base.paperformat_us', False)
            if paperformat_us and paperformat_us.id or False:
                self.paperformat_id = paperformat_us and paperformat_us.id or False
