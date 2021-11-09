from Services.AddressService.address_service import AddressService, AddressServiceDataTransferObject
import os

from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup as StreetLookup

class SmartyAddressService(AddressService):
    def __init__(self):
        pass #super().__init__(self, config_info)

    @classmethod
    def get_api_keys(cls):
        smarty_auth_id = os.environ.get("SMARTY_AUTH_ID")
        smarty_auth_token = os.environ.get("SMARTY_AUTH_TOKEN")

        return smarty_auth_id, smarty_auth_token

    @classmethod
    def get_credentials(cls):
        auth_id, auth_token = cls.get_api_keys()
        credentials = StaticCredentials(auth_id, auth_token)
        return credentials

    @classmethod
    def _set_dictionary(cls):
        if cls.candidates:
            cls.candidates_dictionary = {}
            for r in cls.candidates:
                cls.candidates_dictionary[r.delivery_point_barcode] = r

    @classmethod
    def create_lookup(cls, dto: AddressServiceDataTransferObject):
        lookup = StreetLookup()
        lookup.street = str(dto.streetNo) + ' ' + dto.street_name_1
        lookup.city = dto.city
        lookup.state = dto.state
        lookup.zipcode = dto.zipcode
        return lookup

    @classmethod
    def look_up(cls, address_dto):
        creds = cls.get_credentials()
        print(creds)
        client = ClientBuilder(creds).with_licenses(["us-core-cloud"]).build_us_street_api_client()
        lookup = cls.create_lookup(address_dto)
        
        client.send_lookup(lookup)
        print(lookup.result)

        try:
            client.send_lookup(lookup)
        except exceptions.SmartyException as err:
            print(err)
            cls.candidates = None
            return

        cls.candidates = lookup.result
        cls._set_dictionary()
        print(cls.candidates_dictionary)
        if cls.candidates:
            first_candidate = cls.candidates[0]
            print("Address is valid. (There is at least one candidate)\n")
            print("ZIP Code: " + first_candidate.components.zipcode)
            print("County: " + first_candidate.metadata.county_name)
            print("Latitude: {}".format(first_candidate.metadata.latitude))
            print("Longitude: {}".format(first_candidate.metadata.longitude))
            return True
        else:
            return False
