__author__ = 'itamar'
from oauth2client import client, crypt
ANDROID_CLIENT_ID = "ba:94:98:ec:15:3c:10:4f:c2:86:a0:03:9f:e1:8f:ab:82:8c:97:8c"
Client_ID = "662669652872-1jmfptq96sbjgtjrkmunnobe0tiaontd.apps.googleusercontent.com"

class google_logic():

    def verify_user(self, token, user_id):
        try:
            idinfo = client.verify_id_token(token, user_id)
            # If multiple clients access the backend server:
            if idinfo['aud'] is not ANDROID_CLIENT_ID:
                raise crypt.AppIdentityError("Unrecognized client.")
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")
            if idinfo['hd'] != "com.attender":
                raise crypt.AppIdentityError("Wrong hosted domain.")
        except crypt.AppIdentityError:
            userid = idinfo['sub']
