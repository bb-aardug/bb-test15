# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    "name": "MRP Add Work Type Field",
    "description": """
    This module aims to add selection field on Bill of materials form view.  
    """,
    "version": "15.0.0.1",
    "category": "Manufacturing",
    "website": "http://www.aardug.nl/",
    "author": "Aardug, Arjan Rosman",
    "images": [],
    "depends": ['mrp'],
    "data": [
        "security/ir.model.access.csv",
        "views/mrp_bom_views.xml"
    ],
    "demo": [],
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": 'LGPL-3',
    "qweb": [],
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
