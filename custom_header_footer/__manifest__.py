# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Custom Header Footer',
    'version': '15.0',
    'license': 'LGPL-3',
    'category': 'Reports',
    'author': "Aardug, Arjan Rosman",
    'website': "http://www.aardug.nl/",
    'support': 'arosman@aardug.nl',
    'description': """
        1) Add Company Logo in header and footer of reports.
    """,
    'depends': ['sale', 'account'],
    'data': [
            'views/ir_sequence_view.xml',
            'data/paperformate_data.xml',
            'report/ec_layout.xml',
            'report/sale_invoice_reports.xml',
            'views/res_company_view.xml',
        ],
    'installable': True,
    'application': False,

}
