from flask import Blueprint, render_template, redirect

oauth = Blueprint('oauth', __name__, static_folder='static', template_folder='templates')

import os
from pprint import pprint
import flask
import requests
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
import googleapiclient.discovery

CLIENT_SECRETS_FILE = "./client_secret.json"


# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
SCOPES = ['profile', 'email', 'openid',
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/cloud-platform.read-only',
            'https://www.googleapis.com/auth/cloudplatformprojects',
            'https://www.googleapis.com/auth/cloudplatformprojects.readonly',
            'https://www.googleapis.com/auth/compute',
            'https://www.googleapis.com/auth/compute.readonly',
            'https://www.googleapis.com/auth/devstorage.full_control',
            'https://www.googleapis.com/auth/devstorage.read_only',
            'https://www.googleapis.com/auth/devstorage.read_write',
            'https://www.googleapis.com/auth/drive.metadata.readonly'
            ]

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
API_SERVICE_NAME = 'compute' #compute
API_VERSION = 'v1'          #v1


@oauth.route('/')
def index():
    # print(flask.session['credentials'])
    return print_index_table()


@oauth.route('/test')
def test_api_request():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
      **flask.session['credentials'])


    drive = googleapiclient.discovery.build(
      API_SERVICE_NAME, API_VERSION, credentials=credentials)

    files = drive.files().list().execute()

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.jsonify(**files)


@oauth.route('/test_compute')
def test_compute():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    print(flask.session['credentials'])

    credentials = google.oauth2.credentials.Credentials(
      **flask.session['credentials'])


    compute = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    result = compute.instances().list(project='white-script-342313', zone='us-west1-b').execute()
    print('test api');
    print(result);
    e = result['items'] if 'items' in result else None
    return flask.jsonify(result['items'] if 'items' in result else None)

@oauth.route('/test_resources')
def test_resources():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    print(flask.session['credentials'])

    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])


    # resourceManage = googleapiclient.discovery.build('cloudresourcemanager', 'v3', credentials=credentials)
    # print('list')
    # result = resourceManage.projects().create(
    #     body={
    #         'project_id': 'example-project1234',
    #     }
    # ).execute()
    print("TESTING RESOURCE")
    # resourceManage = googleapiclient.discovery.build('cloudresourcemanager', 'v3', credentials=credentials)

    # client = resourcemanager_v3.ProjectsClient()
    # print("TESTING REQUEST")
    #
    # request = resourcemanager_v3.ListProjectsRequest(
    #     parent= 'projects/750325132631'
    # )
    # print("TESTING PAGE")
    #
    # page_result = client.list_projects(request=request)
    #
    # print('RESOURCE LIST SS')
    # print(page_result)
    # for response in page_result:
    #     print(response)

    projectId = 'personal-340011'

    resourceManage = googleapiclient.discovery.build('cloudresourcemanager', 'v3', credentials=credentials)
    project = resourceManage.projects().get(name="projects/" + projectId).execute()

    # result = resourceManage.projects().list(parent='').execute()
    # print(result)
    # #
    print(project)
    for x in project:
        print(x)
    return project
    # return flask.jsonify(result['items'] if 'items' in result else None)


@oauth.route('/authorize')
def authorize():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES
    )

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = flask.url_for('oauth.oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
      # Enable offline access so that you can refresh an access token without
      # re-prompting the user for permission. Recommended for web server apps.
      access_type='offline',
      # Enable incremental authorization. Recommended as a best practice.
      include_granted_scopes='true'
    )

    # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state

    return flask.redirect(authorization_url)


@oauth.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = flask.session['state']

    flow = Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('oauth.oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url

    print('auth response')
    print(authorization_response)

    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)

    # return flask.redirect(flask.url_for('index'))

    # return flask.redirect(flask.url_for('test_api_request'))
    # return flask.redirect(flask.url_for('test_compute'))
    return flask.redirect(flask.url_for('index'))


@oauth.route('/revoke')
def revoke():
    if 'credentials' not in flask.session:
        return ('You need to <a href="/authorize">authorize</a> before ' +
            'testing the code to revoke credentials.')

    credentials = google.oauth2.credentials.Credentials(
    **flask.session['credentials'])

    revoke = requests.post('https://oauth2.googleapis.com/revoke',
      params={'token': credentials.token},
      headers = {'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        return('Credentials successfully revoked.' + print_index_table())
    else:
        return('An error occurred.' + print_index_table())

@oauth.route('/clear')
def clear_credentials():
  if 'credentials' in flask.session:
    del flask.session['credentials']
  return ('Credentials have been cleared.<br><br>' +
          print_index_table())


def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}



def print_index_table():
  return ('<table>' +
          '<tr><td><a href="/test">Test an API request</a></td>' +
          '<td>Submit an API request and see a formatted JSON response. ' +
          '    Go through the authorization flow if there are no stored ' +
          '    credentials for the user.</td></tr>' +
          '<tr><td><a href="/authorize">Test the auth flow directly</a></td>' +
          '<td>Go directly to the authorization flow. If there are stored ' +
          '    credentials, you still might not be prompted to reauthorize ' +
          '    the application.</td></tr>' +
          '<tr><td><a href="/revoke">Revoke current credentials</a></td>' +
          '<td>Revoke the access token associated with the current user ' +
          '    session. After revoking credentials, if you go to the test ' +
          '    page, you should see an <code>invalid_grant</code> error.' +
          '</td></tr>' +
          '<tr><td><a href="/clear">Clear Flask session credentials</a></td>' +
          '<td>Clear the access token currently stored in the user session. ' +
          '    After clearing the token, if you <a href="/test">test the ' +
          '    API request</a> again, you should go back to the auth flow.' +
          '</td></tr></table>')