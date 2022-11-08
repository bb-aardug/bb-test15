# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Sales Order Line Reference Codes',
    'version': '15.0.1.0',
    'summary': 'Add customer reference codes to sales line items',
    'description': """
                Sales Order Line Reference Codes
                ================================
                * Sale Order Line
                * Order Date
                * Customer Reference Number
    """,
    'category': 'Sales',
    'author': "Aardug, Arjan Rosman",
    'website': "http://www.aardug.nl/",
    'depends': ['sale','account','stock','line_extraction'],
    'data': [
            'view/sale_line.xml',
            'report/sale_and_invoce_report.xml'
            ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}