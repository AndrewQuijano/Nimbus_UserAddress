from Services.AddressService.smarty_address_service import SmartyAddressService
from Services.AddressService.address_service import AddressServiceDataTransferObject

dto = AddressServiceDataTransferObject()
dto.streetNo = 520
dto.street_name_1 = "W. 120th Street"
dto.city = "New York"
dto.state = "NY"
dto.zipcode = 10027
dto.countryCode = "USA"
s = SmartyAddressService()
s.look_up(dto)
