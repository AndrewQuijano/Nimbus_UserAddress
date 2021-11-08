
from Services.BaseResource import ResourceBase
from abc import abstractmethod

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