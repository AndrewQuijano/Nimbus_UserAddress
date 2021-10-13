from application_services.BaseApplicationResource import BaseApplicationResource
import database_services.RDBService as d_service


class AddressResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_by_template(cls, template):
        res = d_service.find_by_template("UserAddress", "Addresses", template, None)
        return res

    # @classmethod
    # def get_by_prefix(cls, prefix):
    #     res = d_service.get_by_prefix("UserAddress", "Addresses", "", prefix)
    #     return res
