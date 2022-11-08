# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo.tools.float_utils import float_compare
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    x_aa_bb_pack_type_id = fields.Many2one('product.packaging', string="Pack Type")
    x_aa_bb_pack_amount = fields.Float(string="Pack Amount")
    x_aa_bb_pack_weight = fields.Float(string="Pack Weight")
    x_aa_bb_origin_id = fields.Many2one('res.country', string="Origin")

    @api.onchange('x_aa_bb_pack_amount', 'x_aa_bb_pack_weight')
    def _onchange_pack_amount_weight(self):
        self.product_qty = self.x_aa_bb_pack_amount * self.x_aa_bb_pack_weight

    # @api.onchange('pack_type')
    # def _onchange_pack_type(self):
    #     if self.pack_type:
    #         return self._check_package()

    # @api.multi
    # def _check_package(self):
    #     default_uom = self.product_id.uom_id
    #     pack = self.pack_type
    #     qty = self.product_qty
    #     if self.product_uom:
    #         q = default_uom._compute_quantity(pack.qty, self.product_uom)
    #         if qty and q and (qty % q):
    #             newqty = qty - (qty % q) + q
    #             return {
    #                 'warning': {
    #                     'title': _('Warning'),
    #                     'message': _("This product is packaged by %.2f %s. You should purchase %.2f %s.") % (pack.qty, default_uom.name, newqty, self.product_uom.name),
    #                 },
    #             }
    #         return {}


    # if Confirm Purchase Order then prepare stock move vals.
    def _prepare_stock_move_vals(self, picking, price_unit, product_uom_qty, product_uom):
        self.ensure_one()
        self._check_orderpoint_picking_type()
        product = self.product_id.with_context(lang=self.order_id.dest_address_id.lang or self.env.user.lang)
        date_planned = self.date_planned or self.order_id.date_planned
        for line in self:
            return {
                # truncate to 2000 to avoid triggering index limit error
                # TODO: remove index in master?
                'name': line.name or '',
                'product_id': line.product_id.id,
                'date': line.order_id.date_order,
                'date_deadline': line.date_planned,
                'location_id': line.order_id.partner_id.property_stock_supplier.id,
                'location_dest_id': line.order_id._get_destination_location(),
                'picking_id': picking.id,
                'partner_id': line.order_id.dest_address_id.id,
                'move_dest_ids': [(4, x) for x in line.move_dest_ids.ids],
                'state': 'draft',
                'purchase_line_id': line.id,
                'company_id': line.order_id.company_id.id,
                'price_unit': price_unit,
                'picking_type_id': line.order_id.picking_type_id.id,
                'group_id': line.order_id.group_id.id,
                'origin': line.order_id.name,
                'description_picking': product.description_pickingin or line.name,
                'propagate_cancel': line.propagate_cancel,
                'warehouse_id': line.order_id.picking_type_id.warehouse_id.id,
                'product_uom_qty': product_uom_qty,
                'product_uom': product_uom.id,
                'product_packaging_id': line.product_packaging_id.id,
                'x_aa_bb_pack_type_id': line.x_aa_bb_pack_type_id.id,
                'x_aa_bb_pack_amount': line.x_aa_bb_pack_amount,
                'x_aa_bb_pack_weight': line.x_aa_bb_pack_weight
            }

    # def _create_stock_moves(self, picking):
    #     moves = self.env['stock.move']
    #     done = self.env['stock.move'].browse()
    #     for line in self:
    #         if line.product_id.type not in ['product', 'consu']:
    #             continue
    #         qty = 0.0
    #         price_unit = line._get_stock_move_price_unit()
    #         for move in line.move_ids.filtered(lambda x: x.state != 'cancel'):
    #             qty += move.product_qty
    #         template = {
                # 'name': line.name or '',
                # 'product_id': line.product_id.id,
                # 'product_uom': line.product_uom.id,
                # 'date': line.order_id.date_order,
                # 'date_deadline': line.date_planned,
                # 'location_id': line.order_id.partner_id.property_stock_supplier.id,
                # 'location_dest_id': line.order_id._get_destination_location(),
                # 'picking_id': picking.id,
                # 'partner_id': line.order_id.dest_address_id.id,
                # 'move_dest_ids': False,
                # 'state': 'draft',
                # 'purchase_line_id': line.id,
                # 'company_id': line.order_id.company_id.id,
                # 'price_unit': price_unit,
                # 'picking_type_id': line.order_id.picking_type_id.id,
                # 'group_id': line.order_id.group_id.id,
                # # 'procurement_id': False,
                # 'origin': line.order_id.name,
                # 'route_ids': line.order_id.picking_type_id.warehouse_id and [(6, 0, [x.id for x in line.order_id.picking_type_id.warehouse_id.route_ids])] or [],
                # 'warehouse_id':line.order_id.picking_type_id.warehouse_id.id,
                # 'x_aa_bb_pack_type_id': line.x_aa_bb_pack_type_id.id,
                # 'x_aa_bb_pack_amount': line.x_aa_bb_pack_amount,
                # 'x_aa_bb_pack_weight': line.x_aa_bb_pack_weight
    #         }
            # Fullfill all related procurements with this po line
            # diff_quantity = line.product_qty - qty
            # for procurement in line.procurement_ids:
            #     # If the procurement has some moves already, we should deduct their quantity
            #     sum_existing_moves = sum(x.product_qty for x in procurement.move_ids if x.state != 'cancel')
            #     existing_proc_qty = procurement.product_id.uom_id._compute_quantity(sum_existing_moves, procurement.product_uom)
            #     procurement_qty = procurement.product_uom._compute_quantity(procurement.product_qty, line.product_uom) - existing_proc_qty
            #     if float_compare(procurement_qty, 0.0, precision_rounding=procurement.product_uom.rounding) > 0:
            #         tmp = template.copy()
            #         tmp.update({
            #             'product_uom_qty': min(procurement_qty, diff_quantity),
            #             'move_dest_id': procurement.move_dest_id.id,  #move destination is same as procurement destination
            #             'procurement_id': procurement.id,
            #             'propagate': procurement.rule_id.propagate,
            #         })
            #         done += moves.create(tmp)
            #         diff_quantity -= min(procurement_qty, diff_quantity)
        #     if float_compare(diff_quantity, 0.0, precision_rounding=line.product_uom.rounding) > 0:
        #         template['product_uom_qty'] = diff_quantity
        #         done += moves.create(template)
        # return done


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # def _prepare_invoice_line_from_po_line(self, line):
    #     result = super(AccountInvoiceInherit, self)._prepare_invoice_line_from_po_line(line)
    #     data = {
    #         'x_aa_bb_pack_type_id': line.x_aa_bb_pack_type_id.id,
    #         'x_aa_bb_pack_amount': line.x_aa_bb_pack_amount,
    #         'x_aa_bb_pack_weight': line.x_aa_bb_pack_weight,
    #         'quantity': line.product_qty,
    #         }
    #     result.update(data)
    #     return result

    @api.model_create_multi
    def create(self, vals_list):
        moves = super(AccountMoveLine, self).create(vals_list)
        origin_id = self.env['purchase.order'].search([('name', '=', moves.move_id.invoice_origin)], limit=1)
        if origin_id and moves.move_id.invoice_origin == origin_id.name:
            for line in origin_id.order_line:
                moves.x_aa_bb_pack_type_id = line.x_aa_bb_pack_type_id.id
                moves.x_aa_bb_pack_amount = line.x_aa_bb_pack_amount
                moves.x_aa_bb_pack_weight = line.x_aa_bb_pack_amount
        return moves


class StockMoveLine(models.Model):
    _inherit = "stock.move"

    x_aa_bb_pack_type_id = fields.Many2one('product.packaging', string="Pack Type")
    x_aa_bb_pack_amount = fields.Float(string="Pack Amount")
    x_aa_bb_pack_weight = fields.Float(string="Pack Weight")

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    x_aa_bb_pack_type_id = fields.Many2one('product.packaging', string="Pack Type")
    x_aa_bb_pack_amount = fields.Float(string="Pack Amount")
    x_aa_bb_pack_weight = fields.Float(string="Pack Weight")
    x_aa_bb_lot_ids = fields.Many2many('stock.production.lot', string='Serial Numbers', compute = "_assign_packlots")
    x_aa_bb_origin_id = fields.Many2one('res.country', string="Origin")

    def _assign_packlots(self):
        for rec in self:
            rec.x_aa_bb_lot_ids = [[6, False, [lot.id for lot in rec.move_id.lot_ids]]]

    # for open Lot/serial Number view using button click
    def action_lots_form(self):
        action = self.env.ref('stock.action_production_lot_form').read()[0]
        if len(self.x_aa_bb_lot_ids.ids) == 1 :
            action['domain'] = [('id', 'in', self.x_aa_bb_lot_ids.id)]
            action['views'] = [(self.env.ref('stock.view_production_lot_form').id, 'form')]
            action['res_id'] = self.x_aa_bb_lot_ids.id
        else :
            action['domain'] = [('id', 'in', self.x_aa_bb_lot_ids.ids)]
            action['views'] = [(self.env.ref('stock.view_production_lot_tree').id, 'tree')]
            action['res_id'] = self.x_aa_bb_lot_ids.ids
        return action

    def print_lots_barcode(self):
        # self.write({'printed': True})
        # move_line = self.env['stock.move.line']
        return self.env.ref('lot_barcode.action_report_lot_barcode_big_extend').report_action(self)

    def create(self, vals):
        res = super(StockMoveLine, self).create(vals)
        purchase = res['picking_id']['purchase_id']
        purchase_line = self.env['purchase.order.line'].search([('order_id','=',purchase.id)])
        for line in purchase_line:
            if res['product_id'] == line.product_id:
                res.update({
                        'x_aa_bb_pack_type_id':line.x_aa_bb_pack_type_id.id,
                        'x_aa_bb_pack_amount':line.x_aa_bb_pack_amount,
                        'x_aa_bb_pack_weight':line.x_aa_bb_pack_weight,
                        'x_aa_bb_origin_id': line.x_aa_bb_origin_id.id,
                    })
        return res

    # @api.multi
    # def write(self, vals):
    #     res = super(StockPackOperationLine, self).write(vals)
    #     if len(self.pack_lot_ids.ids) > 1:
    #         raise UserError(_('You have Only One Lot Assign!!!'))       
    #     return res

class AccountInvoice(models.Model):
    _inherit = "account.move.line"

    x_aa_bb_pack_type_id = fields.Many2one('product.packaging', string="Pack Type")
    x_aa_bb_pack_amount = fields.Float(string="Pack Amount")
    x_aa_bb_pack_weight = fields.Float(string="Pack Weight")
