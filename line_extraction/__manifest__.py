# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Line Extraction',
    'version': '15.0.1',
    'description': """This module used to Sale Line Product Description Set In Delivery Lines.""",
    'summary': 'Product Description in Delivery Line',
    'category': 'Sale',
    'author': "Aardug, Arjan Rosman",
    'website': "http://www.aardug.nl/",
    'depends': ['base','sale','stock','sale_stock','mrp', 'product_expiry'],
    'data': [
            'data/report_paper_formate.xml',
            'view/view_picking.xml',
            'report/picking_report.xml'
            ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}
