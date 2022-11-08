# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Account Invoice Merge',
    'version': '15.0.1.0.0',
    'category': 'Finance',
    'summary': "Merge invoices in draft",
    'description': """
        Merge the invoice in condition of,
        * 'Draft' state
        * Having same partner, company and address
    """,
    'author': 'Aardug, Arjan Rosman',
    'website': 'arosman@aardug.nl',
    'license': 'AGPL-3',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/invoice_merge_view.xml',
    ],
    'installable': True,
}
