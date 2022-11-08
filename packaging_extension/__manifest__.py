# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Packaging Extension',
    'category': 'Hidden',
    'summary': """Add custom fields like Pack Type, Pack Amount, Pack Weight and Origin
     on PO Line , Invoice Line , Stock Move and Stock Move Line""",
    'version': '15.0.0.1',
    'description': """
     * Add custom fields like Pack Type, Pack Amount, Pack Weight and Origin
       on PO Line , Invoice Line , Stock Move and Stock Move Line.
     * On PO line quantity is calculated as "Quantity = Pack Amount * Pack Weight".
     * On Stock Move Line you can showing lots and printing barcode reports using click by button
         * Show lots
         * Print reports
    """,
    'depends':['line_extraction','purchase','stock', 'lot_barcode', 'base'],
    'website': "http://www.aardug.nl/",
    'author': "Aardug, Arjan Rosman",
    'data' : [
        'views/purchase_view.xml',
        'report/purchase_and_invoce_report.xml'
    ],
    'license': 'LGPL-3',
    'auto_install': False,
    'instalable': True,
}
