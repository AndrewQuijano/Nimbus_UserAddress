import os, pymysql
from Services.AddressService.address_service import AddressService as AddressService
from Services.UserService.user_service import UserService as UserService

def get_db_info():
    db_host = os.environ.get("DBHOST", None)
    db_user = os.environ.get("DBUSER", None)
    db_password = os.environ.get("DBPASSWORD", None)

    if db_host is not None:
        db_info = {
            "host": db_host,
            "user": db_user,
            "password": db_password,
            "cursorclass": pymysql.cursors.DictCursor
        }
    else:
        db_info = {
            "host": "localhost",
            "user": "dbuser",
            "password": "dbuserdbuser",
            "cursorclass": pymysql.cursors.DictCursor
        }

    return db_info


def _get_service_by_name(service_name):
    if service_name == "user_service":
        db_info = get_db_info()
        del db_info['cursorclass']
        db_info['db'] = "UserAddress"

        return UserService({
            "db_name": "UserAddress",
            "table_name": "Users",
            "db_connect_info": db_info,
            "key_columns": ['ID']
        })

    elif service_name == "address_service":
        db_info = get_db_info()
        del db_info['cursorclass']
        db_info['db'] = "UserAddress"

        return AddressService({
            "db_name": "UserAddress",
            "table_name": "Addresses",
            "db_connect_info": db_info,
            "key_columns": ['ID']
        })

    else:
        return None



def _generate_user_links(res):
    new_res = []
    for user_dict in res:
        links = [{
            "rel": "self",
            "href": f"/users/{user_dict['ID']}"
        }]
        if 'addressID' in user_dict and user_dict['addressID']:
            links.append({
                "rel": "address",
                "href": f"/addresses/{user_dict['addressID']}"
            })
        user_dict['links'] = links
        new_res.append(user_dict)

    return new_res


def _generate_address_links(res, userID = None):
    new_res = []
    for address_dict in res:
        links = [{
            "rel": "self",
            "href": f"/addresses/{address_dict['ID']}"
        }]
        if 'userID' in address_dict and address_dict['userID']:
            links.append({
                "rel": "user",
                "href": f"/users/{address_dict['userID']}"
            })
        elif userID is not None:
            links.append({
                "rel": "user",
                "href": f"/users/{userID}"
            })
        address_dict['links'] = links
        new_res.append(address_dict)

    return new_res
