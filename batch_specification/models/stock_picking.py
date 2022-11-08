# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    x_aa_bb_lots_ids = fields.Many2many('stock.production.lot',
                                        compute='_compute_lot_ids',
                                        string='Lots')
    x_aa_bb__count = fields.Integer(string='Lots count',
                                    compute='_compute_lot_ids')

    def _action_generate_immediate_wizard(self, show_transfers=False):
        """
            Assign actual value of Product Fields
        """
        res = super(StockPicking, self)._action_generate_immediate_wizard \
            (show_transfers=False)
        if self.x_aa_bb_lots_ids:
            for operation in self.move_ids_without_package:
                for lot in self.x_aa_bb_lots_ids:
                    if operation.product_id == lot.product_id:
                        lot.x_aa_bb_operation_id = operation.id
                        product_field = lot.x_aa_bb_product_field_ids. \
                            filtered(lambda x: x.x_aa_bb_name ==
                                               'Regel 7 Land van Herkomst')
                        if product_field and product_field.x_aa_bb_actual_value \
                                != operation.origin_id.name:
                            product_field.x_aa_bb_actual_value = \
                                operation.origin.name if operation.origin_id \
                                    else False

        return res

    @api.depends('state')
    def _compute_lot_ids(self):
        """
            on basis of state assign lots and count lots
        """
        lot = []
        for pack_ids in self.move_ids_without_package:
            for pack_lot_id in pack_ids.lot_ids:
                lot.append(pack_lot_id.id)
        self.x_aa_bb__count = len(lot)
        self.x_aa_bb_lots_ids = lot

    def action_view_lot(self):
        """
            from this button we can view lot
        """
        action = self.env.ref('stock.action_production_lot_form')
        result = action.read()[0]
        result['context'] = {}
        lots_ids = sum([order.x_aa_bb_lots_ids.ids for order in self], [])
        if len(lots_ids) > 0:
            result['domain'] = "[('id','in',[" + ','.join(map(str, lots_ids)) + "])]"
        return result


class StockMove(models.Model):
    _inherit = "stock.move.line"
    _rec_name = "picking_id"
