# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################


from odoo import models, fields, api


class MrpProductionInh(models.Model):
    _inherit = 'mrp.production'

    def button_mark_done(self):
        res = super(MrpProductionInh, self).button_mark_done()
        moveObj = self.env['stock.move']
        moves_to_cancel = self.env['stock.move']
        for move in self.move_raw_ids:
            if move.state == 'done':
                return_mv = moveObj.search([('move_dest_ids', '=', move.id)])
                if return_mv.state not in ('done', 'cancel') and return_mv.picking_id:
                    moves_to_cancel += return_mv
        moves_to_cancel._action_cancel()
        return res