
from openvpn.googleapi import create_project


def initiate_vpn(credentials, desired_project_id):

    print('task is initiated')

    create_project(credentials, desired_project_id)

    print('create vpn is done.')

