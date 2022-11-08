# -*- coding: utf-8 -*-
##############################################################################
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
##############################################################################

from odoo import api, fields, models, _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    x_aa_bb_lots_ids = fields.Many2many('stock.production.lot',
                                        compute='_compute_lots_ids',
                                        string='Lots')
    x_aa_bb__count_lots = fields.Integer(string='Lots count',
                                         compute='_compute_lots_ids')

    @api.depends('state')
    def _compute_lots_ids(self):
        """"
            Compute lot ids
        """
        for rec in self:
            lot = []
            for move_ids in rec.move_raw_ids:
                for move_lot_id in move_ids.lot_ids:
                    for lot_id in move_lot_id:
                        lot.append(lot_id.id)
            rec.x_aa_bb__count_lots = len(lot)
            rec.x_aa_bb_lots_ids = lot

    def action_view_lots(self):
        """
            View lots from this button
        """
        action = self.env.ref('stock.action_production_lot_form')
        result = action.read()[0]
        result['context'] = {}
        lot_ids = sum([order.x_aa_bb_lots_ids.ids for order in self], [])
        if len(lot_ids) > 0:
            result['domain'] = "[('id','in',[" + ','\
                .join(map(str, lot_ids)) + "])]"
        return result
