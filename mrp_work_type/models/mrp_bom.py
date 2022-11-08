# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models, _

class MrpBomInh(models.Model):
    _inherit = 'mrp.bom'

    x_aa_bb_work_type_id = fields.Many2one('mrp.worktype', string='Work Type')


class MrpProductionInh(models.Model):
    _inherit = 'mrp.production'

    x_aa_bb_work_type_id = fields.Many2one('mrp.worktype', string='Work Type')

    @api.model
    def create(self, values):
        res = super(MrpProductionInh, self).create(values)
        if res.bom_id:
            res.x_aa_bb_work_type_id = res.bom_id.x_aa_bb_work_type_id.id
        return res

    @api.onchange('bom_id')
    def onchange_bom_id(self):
        self.x_aa_bb_work_type_id = self.bom_id.x_aa_bb_work_type_id.id

class MrpWorkType(models.Model):
    _name = 'mrp.worktype'
    _description = "Work Type"
    _rec_name = "x_aa_bb_name"

    x_aa_bb_name = fields.Char(string='Work Type')
