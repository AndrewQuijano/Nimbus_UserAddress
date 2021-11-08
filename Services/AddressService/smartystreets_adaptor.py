from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup as StreetLookup

import middleware.context as context

class SmartyStreetsAdaptor:

    candidate_fields = [
        'city_name', 'default_city_name', 'delivery_point', 'delivery_point_check_digit', 'extra_secondary_designator',
        'extra_secondary_number', 'plus4_code', 'pmb_designator', 'pmb_number', 'primary_number', 'secondary_designator',
        'secondary_number', 'state_abbreviation', 'street_name', 'street_postdirection', 'street_predirection',
        'street_suffix', 'urbanization', 'zipcode'
        ]
    base_fields = [
        'delivery_line_1', 'delivery_line_2', 'delivery_point_barcode', 'last_line'
    ]
    smarty_info = context.get_context("SMARTY")

    auth_id = smarty_info["auth_id"]
    auth_token = smarty_info["auth_token"]

    def __init__(self, candidates=None):
        self._credentials = None
        self.candidates = candidates
        self.candidates_dictionary = None

        if self.candidates:
            self._set_dictionary()

        self._set_credentials()

    def _set_credentials(self):
        self.credentials = StaticCredentials(SmartyStreetsAdaptor.auth_id,
                                             SmartyStreetsAdaptor.auth_token)

    def _set_dictionary(self):
        if self.candidates:
            self.candidates_dictionary = {}
            for r in self.candidates:
                self.candidates_dictionary[r.delivery_point_barcode] = r

    def do_lookup(self, lookup):
        client = ClientBuilder(self.credentials).with_licenses(["us-standard-cloud"]).build_us_street_api_client()
        client.send_lookup(lookup)

        try:
            client.send_lookup(lookup)
        except exceptions.SmartyException as err:
            print(err)
            self.candidates = None
            return

        self.candidates = lookup.result
        self._set_dictionary()

    def do_search(self, address_fields):
        lookup = StreetLookup()

        lookup.street = address_fields.get("street1", None)
        lookup.street2 = address_fields.get("street2", None)
        lookup.city = address_fields.get("city", None)
        lookup.state = address_fields.get("state", None)
        lookup.zipcode = address_fields.get("zipcode")

        self.do_lookup(lookup)

        if self.candidates:
            result = len(self.candidates)
        else:
            result = None

        return result

    def get_candidates(self):
        return self.candidates_dictionary

    def get_candidates_json(self):
        return self.to_json()

    def to_json(self):

        result_all = {}

        for k,c in self.candidates_dictionary.items():
            result = {}

            base_fields = dir(c)
            for f in base_fields:
                if f not in ['components', 'metadata'] and f[0] != "_":
                    result[f] = getattr(c, f, None)

            components_fields = dir(c.components)
            result["components"] = {}
            for f in components_fields:
                if f[0] != "_":
                    result["components"][f] = getattr(c.components, f, None)

            metadata_fields = dir(c.metadata)
            result["metadata"] = {}
            for f in metadata_fields:
                if f[0] != "_":
                    result["metadata"][f] = getattr(c.metadata, f, None)

            result_all[c.delivery_point_barcode] = result

        return result_all



