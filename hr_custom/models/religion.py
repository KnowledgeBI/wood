# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models


class Religion(models.Model):
    _name = "religion.religion"
    _description = "Religion"

    name = fields.Char('Religion Name', required=True, translate=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Religion name already exists !"),
    ]
