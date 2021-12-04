from Services.AddressService.smarty_address_service import SmartyAddressService

class ServiceFactory():

    @staticmethod
    def get_address_service():
        return SmartyAddressService()