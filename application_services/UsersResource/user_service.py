from application_services.BaseApplicationResource import BaseApplicationResource
import database_services.RDBService as d_service


class UserResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_by_template(cls, template):
        users = d_service.find_by_template("UserAddress", "Users", template, None)
        new_users = []
        for user in users:
            user['links'] = [
                {
                    "rel": "self",
                    "href": f"/users/{user['ID']}"
                }
            ]
            if user['addressID'] is not None:
                user['links'].append(
                    {
                        "rel": "address",
                        "href": f"/address/{user['addressID']}"
                    }
                )

            new_users.append(user)

        return new_users

    @classmethod
    def get_by_prefix(cls, prefix):
        res = d_service.get_by_prefix("UserAddress", "Users", "username", prefix)
        return res
