from social_core.backends.oauth import BaseOAuth2


class IonOauth2(BaseOAuth2):  # pylint: disable=abstract-method
    name = "ion"
    AUTHORIZATION_URL = "https://ion.tjhsst.edu/oauth/authorize"
    ACCESS_TOKEN_URL = "https://ion.tjhsst.edu/oauth/token"
    ACCESS_TOKEN_METHOD = "POST"
    EXTRA_DATA = [("refresh_token", "refresh_token", True), ("expires_in", "expires")]

    def get_scope(self):
        return ["read"]

    def get_user_details(self, response):
        profile = self.get_json(
            "https://ion.tjhsst.edu/api/profile",
            params={"access_token": response["access_token"]},
        )
        # fields used to populate/update User model

        if not profile["graduation_year"]:
            profile["graduation_year"] = 0

        return {
            "id": profile["id"],
            "username": profile["ion_username"],
            "first_name": profile["first_name"],
            "last_name": profile["last_name"],
            "nickname": profile["nickname"] if profile["nickname"] else "",
            "full_name": profile["full_name"],
            "email": profile["tj_email"],
            "is_student": profile["is_student"],
            "graduation_year": profile["graduation_year"],
        }

    def get_user_id(self, details, response):
        return details["id"]
