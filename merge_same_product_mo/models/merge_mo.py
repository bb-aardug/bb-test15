# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################
from collections import defaultdict


from odoo import models, fields, api


class MrpOrderMerge(models.TransientModel):
    _name = 'mo.merge'
    _description = 'MRP Production Order Merge'

    def do_merge(self):
        '''method to merge mo of same product'''
        moObj = self.env['mrp.production']
        mo_of_same_product = self.env['mrp.production'].mapped('product_id')
        print(':::::::::::::::;;product>>>>>>>>>>>>>..............')
        moIds = moObj.search_read([
            ('state', '=', 'confirmed')],
            ['product_qty', 'state', 'product_id'])
        D = defaultdict(list)
        for mo in moIds:
            D[mo['product_id'][0]].append((mo['id'], mo['product_qty']))
        for key , value in D.items():
            unlinkIds = []
            totalQty = 0.0
            mainMo = moObj.search([
                ('state', '=', 'progress'), ('product_id', '=', key)])
            mainMo = mainMo[0] if mainMo else False
            if mainMo:
                for v in value:
                    unlinkIds.append(v[0])
                    totalQty += v[1]
                    moId = moObj.browse(v[0])
                    moId.action_cancel()
                pQty = totalQty + mainMo.product_qty
                if totalQty:
                    self.env['change.production.qty'].create({
                        'mo_id': mainMo.id,
                        'product_qty': pQty,
                    }).change_prod_qty()
                    for mr in mainMo.move_raw_ids:
                        for moi in mr.move_orig_ids:
                            if moi.state not in ('done', 'cancel'):
                                moi.product_uom_qty = mr.product_uom_qty
                            if moi.picking_id:
                                moi.picking_id.do_unreserve()
                                for mv in moi.picking_id.move_lines:
                                    if mv.state == 'cancel':
                                        mv.unlink()
                                moi.picking_id.action_assign()
                            break
            else:
                for v in value:
                    mainMo = v[0], v[1]
                    break
                for v in value:
                    if mainMo[0] != v[0]:
                        unlinkIds.append(v[0])
                        totalQty += v[1]
                        moObj.browse(v[0]).action_cancel()
                if totalQty:
                    self.env['change.production.qty'].create({
                        'mo_id': mainMo[0],
                        'product_qty': totalQty + mainMo[1],
                    }).change_prod_qty()
                    mainMoRec = moObj.browse(mainMo[0])
                    for mr in mainMoRec.move_raw_ids:
                        for moi in mr.move_orig_ids:
                            if moi.state not in ('done', 'cancel'):
                                moi.product_uom_qty = mr.product_uom_qty
                            if moi.picking_id:
                                moi.picking_id.do_unreserve()
                                for mv in moi.picking_id.move_lines:
                                    if mv.state == 'cancel':
                                        mv.unlink()
                                moi.picking_id.action_assign()
                            break

