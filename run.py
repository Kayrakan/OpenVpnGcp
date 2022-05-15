import os

from openvpn import app


if __name__ == "__main__":

    # When running locally, disable OAuthlib's HTTPs verification.
    # ACTION ITEM for developers:
    #     When running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Specify a hostname and port that are set as a valid redirect URI
    # for your API project in the Google API Console.
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

    app.run()

