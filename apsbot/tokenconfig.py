import json
import os
from aps_toolkit import Token
from aps_toolkit import ClientType
from aps_toolkit import RevokeType
from aps_toolkit import Auth


class TokenConfig:
    config_path = 'token_config.json'

    @classmethod
    def save_config(cls, token):
        """Save token information to a JSON file."""
        token_data = {
            'APS_ACCESS_TOKEN': token.access_token,
            'APS_REFRESH_TOKEN': token.refresh_token,
            'APS_TOKEN_TYPE': token.token_type,
            'APS_EXPIRES_IN': token.expires_in,
        }
        with open(cls.config_path, 'w') as file:
            json.dump(token_data, file, indent=4)

    @classmethod
    def load_config(cls):
        """Load token information from a JSON file."""
        if not os.path.exists(cls.config_path):
            return None
        with open(cls.config_path, 'r') as file:
            token_data = json.load(file)
            access_token = token_data['APS_ACCESS_TOKEN']
            refresh_token = token_data['APS_REFRESH_TOKEN']
            token_type = token_data['APS_TOKEN_TYPE']
            expires_in = token_data['APS_EXPIRES_IN']
            token = Token(access_token, token_type, expires_in, refresh_token)
            if token.refresh_token is not None and token.access_token is not None and token.refresh_token != 'null':
                status = token.introspect(ClientType.PRIVATE)
                if status['active']:
                    return token
                else:
                    print("Token is expired.")
                    token.revoke(RevokeType.REFRESH_TOKEN_PRIVATE)
                    auth = Auth()
                    token = auth.refresh_new_token(token.refresh_token)
                    cls.save_config(token)
                    return token
            else:
                token = Auth().auth2leg()
                cls.save_config(token)
        return token
