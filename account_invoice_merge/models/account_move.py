# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, models
from odoo.tools import float_is_zero


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _get_invoice_key_cols(self):
        '''Method to get invoice invoice fields and proceeded further'''
        return [
            'partner_id', 'invoice_user_id', 'move_type', 'currency_id',
            'journal_id', 'company_id', 'partner_bank_id'
        ]

    @api.model
    def _get_invoice_line_key_cols(self):
        '''Method to get invoice invoice line fields and proceeded further'''
        fields = [
            'name', 'ref', 'discount', 'tax_ids', 'price_unit', 'quantity', 
            'product_id', 'account_id', 'analytic_account_id', 'product_uom_id'
        ]
        for field in [
                'sale_line_ids',
                'purchase_price',
        ]:
            if field in self.env['account.move.line']._fields:
                fields.append(field)
        return fields

    @api.model
    def _get_first_invoice_fields(self, invoice):
        '''Method to pass invoice values from parent invoice'''
        return {
            'invoice_origin': '%s' % (invoice.invoice_origin or '',),
            'partner_id': invoice.partner_id.id,
            'journal_id': invoice.journal_id.id,
            'invoice_user_id': invoice.invoice_user_id.id,
            'currency_id': invoice.currency_id.id,
            'company_id': invoice.company_id.id,
            'move_type': invoice.move_type,
            'state': 'draft',
            'payment_reference': '%s' % (invoice.payment_reference or '',),
            'name': '%s' % (invoice.name or '',),
            'fiscal_position_id': invoice.fiscal_position_id.id,
            'invoice_payment_term_id': invoice.invoice_payment_term_id.id,
            'line_ids': {},
            'partner_bank_id': invoice.partner_bank_id.id,
        }

    def _get_draft_invoices(self):
        """Overridable function to return draft invoices to merge"""
        return self.filtered(lambda x: x.state == 'draft')

    def do_merge(self, x_aa_bb_keep_references=True, x_aa_bb_date_invoice=False,
                 remove_empty_invoice_lines=True):
        """
        To merge similar type of account invoices.
        Invoices will only be merged if:
        * Account invoices are in draft
        * Account invoices belong to the same partner
        * Account invoices are have same company, partner, address, currency,
          journal, currency, salesman, account, type
        Lines will only be merged if:
        * Invoice lines are exactly the same except for the quantity and unit

         @param self: The object pointer.
         @param x_aa_bb_keep_references: If True, keep reference of original invoices

         @return: new account invoice id

        """

        def make_key(br, fields):
            '''Process to merged invoice to be created'''
            list_key = []
            for field in fields:
                field_val = getattr(br, field)
                if field in ('product_id', 'account_id'):
                    if not field_val:
                        field_val = False
                if (isinstance(field_val, models.BaseModel) and
                        field != 'tax_ids' and
                        field != 'sale_line_ids'):
                    field_val = field_val.id
                elif isinstance(field_val, models.BaseModel):
                    field_val = False
                elif (isinstance(field_val, list) or
                        field == 'tax_ids' or
                        field == 'sale_line_ids'):
                    field_val = ((6, 0, tuple([v.id for v in field_val])),)
                list_key.append((field, field_val))
            list_key.sort()
            return tuple(list_key)

        # compute what the new invoices should contain
        new_invoices = {}
        seen_origins = {}
        seen_client_refs = {}

        for account_invoice in self._get_draft_invoices():
            invoice_key = make_key(
                account_invoice, self._get_invoice_key_cols())
            new_invoice = new_invoices.setdefault(invoice_key, ({}, []))
            origins = seen_origins.setdefault(invoice_key, set())
            client_refs = seen_client_refs.setdefault(invoice_key, set())
            new_invoice[1].append(account_invoice.id)
            invoice_infos = new_invoice[0]
            if not invoice_infos:
                invoice_infos.update(
                    self._get_first_invoice_fields(account_invoice))
                origins.add(account_invoice.ref)
                client_refs.add(account_invoice.payment_reference)
                if not x_aa_bb_keep_references:
                    invoice_infos.pop('name')
            else:
                if account_invoice.name and x_aa_bb_keep_references:
                    invoice_infos['name'] = \
                        (invoice_infos['name'] or '') + ' ' + \
                        account_invoice.name
                if account_invoice.ref and \
                        account_invoice.ref not in origins:
                    invoice_infos['origin'] = \
                        (invoice_infos['ref'] or '') + ' ' + \
                        account_invoice.ref
                    origins.add(account_invoice.ref)
                if account_invoice.payment_reference \
                        and account_invoice.payment_reference not in client_refs:
                    invoice_infos['payment_reference'] = \
                        (invoice_infos['payment_reference'] or '') + ' ' + \
                        account_invoice.payment_reference
                    client_refs.add(account_invoice.payment_reference)

            for invoice_line in account_invoice.line_ids:
                line_key = make_key(
                    invoice_line, self._get_invoice_line_key_cols())

                o_line = invoice_infos['line_ids'].\
                    setdefault(line_key, {})

                if o_line:
                    # merge the line with an existing line
                    o_line['quantity'] += invoice_line.quantity
                else:
                    # append a new "standalone" line
                    o_line['quantity'] = invoice_line.quantity

        allinvoices = []
        allnewinvoices = []
        invoices_info = {}
        old_invoices = self.env['account.move']
        qty_prec = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        for invoice_key, (invoice_data, old_ids) in new_invoices.items():
            # skip merges with only one invoice
            if len(old_ids) < 2:
                allinvoices += (old_ids or [])
                continue
            # cleanup invoice line data
            for key, value in invoice_data['line_ids'].items():
                value.update(dict(key))

            if remove_empty_invoice_lines:
                invoice_data['line_ids'] = [
                    (0, 0, value) for value in
                    invoice_data['line_ids'].values() if
                    not float_is_zero(
                        value['quantity'], precision_digits=qty_prec)]
            else:
                invoice_data['line_ids'] = [
                    (0, 0, value) for value in
                    invoice_data['line_ids'].values()]

            if x_aa_bb_date_invoice:
                invoice_data['invoice_date'] = x_aa_bb_date_invoice

            # create the new invoice
            newinvoice = self.with_context(is_merge=True).create(invoice_data)
            invoices_info.update({newinvoice.id: old_ids})
            allinvoices.append(newinvoice.id)
            allnewinvoices.append(newinvoice)
            # cancel old invoices
            old_invoices = self.env['account.move'].browse(old_ids)
            old_invoices.with_context(is_merge=True).button_cancel()

        # Make link between original sale order
        # None if sale is not installed
        invoice_line_obj = self.env['account.move.line']
        for new_invoice_id in invoices_info:
            if 'sale.order' in self.env.registry:
                sale_todos = old_invoices.mapped(
                    'line_ids.sale_line_ids.order_id')
                for org_so in sale_todos:
                    for so_line in org_so.order_line:
                        invoice_line = invoice_line_obj.search(
                            [('id', 'in', so_line.invoice_lines.ids),
                             ('invoice_id', '=', new_invoice_id)])
                        if invoice_line:
                            so_line.write(
                                {'invoice_lines': [(6, 0, invoice_line.ids)]})

        # recreate link (if any) between original analytic account line
        # (invoice time sheet for example) and this new invoice
        anal_line_obj = self.env['account.analytic.line']
        if 'invoice_id' in anal_line_obj._fields:
            for new_invoice_id in invoices_info:
                anal_todos = anal_line_obj.search(
                    [('invoice_id', 'in', invoices_info[new_invoice_id])])
                anal_todos.write({'invoice_id': new_invoice_id})

        for new_invoice in allnewinvoices:
            # custom method call to update the attribute of the invoice line
            new_invoice._update_child_invoice_lines(allnewinvoices)

            new_invoice._compute_amount()
            new_invoice._compute_tax_totals_json()

        return invoices_info

    def _update_child_invoice_lines(self, allnewinvoices):
        '''Method to update attribute for exclude invoice line from invoice tab'''
        for new_invoice_id in allnewinvoices:
            move_lines = new_invoice_id.mapped(
                'invoice_line_ids').filtered(lambda move_line: not move_line.product_id)
            for move_line in move_lines:
                move_line.write({'exclude_from_invoice_tab': True})

