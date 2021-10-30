import os, pymysql
from Services.AddressService.address_service import AddressService as AddressService
from Services.UserService.user_service import UserService as UserService
from middleware import context as ctx

default_limit = ctx.get_context_value("MAX_TABLE_ROWS_TO_PRINT")

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


def _generate_pages(res, inputs, total_count):
    path = inputs.path
    prev_url = f"{path}?"
    next_url = f"{path}?"

    args = []
    for k,v in inputs.args.items():
        args.append(f"{k}={v}")
    args = '&'.join(args)

    if args:
        prev_url += f"{args}"
        next_url += f"{args}"

    if inputs.fields:
        prev_url += f"&fields={inputs.fields}"
        next_url += f"&fields={inputs.fields}"

    limit = int(inputs.limit) if inputs.limit else default_limit
    if limit:
        prev_url += f"&limit={limit}"
        next_url += f"&limit={limit}"

    print(inputs.offset, inputs.limit, total_count)

    if inputs.order_by:
        prev_url += f"&order_by={inputs.order_by}"
        next_url += f"&order_by={inputs.order_by}"

    offset = int(inputs.offset) if inputs.offset else 0
    if offset > 0 and offset + limit >= total_count: # no more results
        prev_url += f"&offset={offset-limit}"
        next_url = ""
    elif offset == 0:
        next_url += f"&offset={offset+limit}"
        prev_url = ""
    else:
        prev_url += f"&offset={offset - limit}"
        next_url += f"&offset={offset + limit}"

    print(res)
    new_dict = {
        "data": res,
        "links": [
            {
                "rel": "self",
                "href": inputs.url
            },
            {
                "rel": "next",
                "href": next_url
            },
            {
                "rel": "prev",
                "href": prev_url
            }
        ]
    }

    return new_dict