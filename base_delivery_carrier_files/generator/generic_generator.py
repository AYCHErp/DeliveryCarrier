# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright 2012 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import csv

from file_generator import CarrierFileGenerator
from base_line import BaseLine
from openerp.addons.base_delivery_carrier_files.csv_writer import UnicodeWriter


class GenericLine(BaseLine):
    fields = ('reference',
              'name',
              'contact',
              'street1',
              'street2',
              'zip',
              'city',
              'state',
              'country_code',
              'phone',
              'fax',
              'mail',
              'delivery_name',
              'weight')


class LaPosteFileGenerator(CarrierFileGenerator):

    @classmethod
    def carrier_for(cls, carrier_name):
        return carrier_name == 'generic'

    def _get_rows(self, picking, configuration):
        """
        Returns the rows to create in the file for a picking

        :param browse_record picking: the picking for which
                                      we generate a row in the file
        :param browse_record configuration: configuration of
                                            the file to generate
        :return: list of rows
        """
        line = GenericLine()
        line.reference = picking.name
        address = picking.address_id
        if address:
            line.name = address.partner_id and address.partner_id.name
            line.contact = address.name
            line.street1 = address.street
            line.street2 = address.street2
            line.zip = address.zip
            line.city = address.city
            line.state = (picking.address_id.state_id and
                         picking.address_id.state_id.name)
            line.country_code = address.country_id and address.country_id.code
            line.phone = address.phone or address.mobile
            line.mail = address.email
            line.fax = address.fax
        line.delivery_name = picking.carrier_id and picking.carrier_id.name
        line.weight = "%.2f" % (picking.weight,)
        return [line.get_fields()]

    def _write_rows(self, file_handle, rows, configuration):
        """
        Write the rows in the file (file_handle)

        :param StringIO file_handle: file to write in
        :param rows: rows to write in the file
        :param browse_record configuration: configuration of
                                            the file to generate
        :return: the file_handle as StringIO with the rows written in it
        """
        writer = UnicodeWriter(file_handle, delimiter=',', quotechar='"',
                               lineterminator='\n', quoting=csv.QUOTE_ALL)
        writer.writerows(rows)
        return file_handle
