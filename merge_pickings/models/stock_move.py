# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, fields, api
from itertools import groupby
from odoo.tools.float_utils import float_compare

class ProductProduct(models.Model):
    _inherit = 'product.product'

    x_aa_bb_procurment_group_id = fields.Many2one('procurement.group', string='Procurment Group')


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    x_aa_bb_merge_picking = fields.Boolean(string='Merge Picking',
        help='this is only for internal manufecturing pickig, please dont apply it for others')


class StockMove(models.Model):
    _inherit = 'stock.move'

    # Here add common procurement group name for products so always moves merges with existing picking.
    def _assign_picking(self):
        """ Try to assign the moves to an existing picking that has not been
        reserved yet and has the same procurement group, locations and picking
        type (moves should already have them identical). Otherwise, create a new
        picking to assign them to. """
        Picking = self.env['stock.picking']
        ProcurementGroup = self.env['procurement.group']
        pgroup_id = False
        grouped_moves = groupby(sorted(self, key=lambda m: [f.id for f in m._key_assign_picking()]), key=lambda m: [m._key_assign_picking()])
        for group, moves in grouped_moves:
            moves = self.env['stock.move'].concat(*list(moves))
            pgroup_id = moves[0].product_id.x_aa_bb_procurment_group_id.id
            if moves[0].picking_type_id.x_aa_bb_merge_picking:
                if moves[0].product_id and not pgroup_id:
                    pgroup_id = ProcurementGroup.create({
                        'name': moves[0].product_id.display_name
                        }).id
                    moves[0].product_id.x_aa_bb_procurment_group_id = pgroup_id
                moves.group_id = pgroup_id
                moves = self.env['stock.move'].concat(*list(moves))
                new_picking = False
                # Could pass the arguments contained in group but they are the same
                # for each move that why moves[0] is acceptable
                picking = moves[0]._search_picking_for_assignation()
                if picking:
                    if any(picking.partner_id.id != m.partner_id.id or
                            picking.origin != m.origin for m in moves):
                        # If a picking is found, we'll append `move` to its move list and thus its
                        # `partner_id` and `ref` field will refer to multiple records. In this
                        # case, we chose to  wipe them.
                        picking.write({
                            'partner_id': False,
                            'origin': False,
                        })
                else:
                    # Don't create picking for negative moves since they will be
                    # reverse and assign to another picking
                    moves = moves.filtered(lambda m: float_compare(m.product_uom_qty, 0.0, precision_rounding=m.product_uom.rounding) >= 0)
                    if not moves:
                        continue
                    new_picking = True
                    picking = Picking.create(moves._get_new_picking_values())

                moves.write({'picking_id': picking.id})
                moves._assign_picking_post_process(new=new_picking)
            else:
                return super(StockMove, self)._assign_picking()
        return True