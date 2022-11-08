# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class AccountMoveMerge(models.TransientModel):
    _name = "account.move.merge"
    _description = "Merge Partner Invoice"

    x_aa_bb_keep_references = fields.Boolean('Keep references from original invoices',
                                     default=True)
    x_aa_bb_date_invoice = fields.Date('Invoice Date')

    @api.model
    def _get_not_mergeable_invoices_message(self, invoices):
        """Overridable function to custom error message"""
        key_fields = invoices._get_invoice_key_cols()
        error_msg = {}
        if len(invoices) != len(invoices._get_draft_invoices()):
            error_msg['state'] = (
                _('Megeable State (ex : %s)') %
                (invoices and invoices[0].state or _('Draft')))
        for field in key_fields:
            if len(set(invoices.mapped(field))) > 1:
                error_msg[field] = invoices._fields[field].string
        return error_msg

    @api.model
    def _dirty_check(self):
        '''Method to check for the invoiced to be merged,
        error messages for the invoice which are unable to be merged'''
        if self.env.context.get('active_model', '') == 'account.move':
            ids = self.env.context['active_ids']
            if len(ids) < 2:
                raise UserError(
                    _('Please select multiple invoices to merge in the list '
                      'view.'))

            invs = self.env['account.move'].browse(ids)
            error_msg = self._get_not_mergeable_invoices_message(invs)
            if error_msg:
                all_msg = _("All invoices must have the same: \n")
                all_msg += '\n'.join([value for value in error_msg.values()])
                raise UserError(all_msg)
        return {}

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        """Changes the view dynamically
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param context: A standard dictionary
         @return: New arch of view.
        """
        res = super(AccountMoveMerge, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=False)
        self._dirty_check()
        return res

    def merge_invoices(self):
        """To merge similar type of account invoices.

             @param self: The object pointer.
             @param cr: A database cursor
             @param uid: ID of the user currently logged in
             @param ids: the ID or list of IDs
             @param context: A standard dictionary

             @return: account invoice action
        """
        inv_obj = self.env['account.move']
        aw_obj = self.env['ir.actions.act_window']
        ids = self.env.context.get('active_ids', [])
        invoices = inv_obj.browse(ids)
        allinvoices = invoices.do_merge(x_aa_bb_keep_references=self.x_aa_bb_keep_references,
                                        x_aa_bb_date_invoice=self.x_aa_bb_date_invoice)        
        xid = {
            'out_invoice': 'action_move_out_invoice_type',
            'out_refund': 'action_move_out_refund_type',
            'in_invoice': 'action_move_in_invoice_type',
            'in_refund': 'action_move_in_refund_type',
        }[invoices[0].move_type]
        action= 'account.'+xid
        action = aw_obj._for_xml_id(action)
        action.update({
            'domain': [('id', 'in', ids + list(allinvoices.keys()))],
        })
        return action


