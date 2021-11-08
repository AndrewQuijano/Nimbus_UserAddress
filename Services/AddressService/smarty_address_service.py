from Services.AddressService.address_service import AddressService
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
    def look_up(cls, address_dto):
        creds = cls.get_credentials()
        print(creds)
        client = ClientBuilder(creds).with_licenses(["us-standard-cloud"]).build_us_street_api_client()
        lookup = StreetLookup()
        lookup.street = "520 W. 120th Street" #address_dto.street_name_1
        # lookup.street2 = "closet under the stairs"
        #lookup.secondary = "APT 2"
        #lookup.urbanization = ""  # Only applies to Puerto Rico addresses
        lookup.city = "New York" #address_dto.city
        lookup.state = "NY" #address_dto.state
        lookup.zipcode = "10027" #address_dto.zipcode
        #lookup.candidates = 3
        client.send_lookup(lookup)

        try:
            client.send_lookup(lookup)
        except exceptions.SmartyException as err:
            print(err)
            cls.candidates = None
            return

        cls.candidates = lookup.result
        cls._set_dictionary()
