
from Services.BaseResource import ResourceBase
from abc import abstractmethod
from flask import Response

candidate_fields = [
        'city_name', 'default_city_name', 'delivery_point', 'delivery_point_check_digit', 'extra_secondary_designator',
        'extra_secondary_number', 'plus4_code', 'pmb_designator', 'pmb_number', 'primary_number', 'secondary_designator',
        'secondary_number', 'state_abbreviation', 'street_name', 'street_postdirection', 'street_predirection',
        'street_suffix', 'urbanization', 'zipcode'
        ]

class AddressServiceDataTransferObject():

    def __init__(self):
        self.city = None
        self.state = None
        self.streetNo = None
        self.street_name_1 = None
        self.street_name_2 = None
        self.zipcode = None
        self.countryCode = None

class AddressService(ResourceBase):

    def __init__(self, config_info):
        super().__init__(config_info)

    @classmethod
    def look_up(cls, address_dto):
        pass

    @classmethod
    def convert_to_dict(ID, streetNo, streetName1, streetName2, city, state, zipcode, countryCode):
        d = {}
        if ID is not None:
            d['ID'] = ID
        if streetNo is not None:
            d['streetNo'] = streetNo
        if streetName1 is not None:
            d['streetName1'] = streetName1
        if streetName2 is not None:
            d['streetName2'] = streetName2
        if city is not None:
            d['city'] = city
        if state is not None:
            d['state'] = state
        if zipcode is not None:
            d['zipcode'] = zipcode
        if countryCode is not None:
            d['countryCode'] = countryCode
        return d

    @classmethod
    def convert_to_dto(cls, addr_dict):
        addr = AddressServiceDataTransferObject()
        if addr_dict['streetNo'] != 'NULL':
            addr.streetNo = addr_dict['streetNo']
        if addr_dict['streetName1'] != 'NULL':
            addr.street_name_1 = addr_dict['streetName1']
        if addr_dict['streetName2'] != 'NULL':
            addr.street_name_2 = addr_dict['streetName2']
        if addr_dict['city'] != 'NULL':
            addr.city = addr_dict['city']
        if addr_dict['state'] != 'NULL':
            addr.state = addr_dict['state']
        if addr_dict['zipcode'] != 'NULL':
            addr.zipcode = addr_dict['zipcode']
        if addr_dict['countryCode'] != 'NULL':
            addr.countryCode = addr_dict['countryCode']
        return addr

