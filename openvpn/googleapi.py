import os
from pprint import pprint

import flask
import googleapiclient.discovery

def create_project(credentials,desired_project_id):

    resourceManage = googleapiclient.discovery.build('cloudresourcemanager', 'v3', credentials=credentials)
    print('list')
    result = resourceManage.projects().create(
        body={
            'project_id': desired_project_id,
        }
    ).execute()

    print('created.')


def get_project(credentials):
    resourceManage = googleapiclient.discovery.build('cloudresourcemanager', 'v3', credentials=credentials)
    print('get project')
    result = resourceManage.projects().get(name='projects/exp-project321').execute()
    print('project ready')

    for x in result:
        print(result[x])

# project='debian-cloud', family='debian-9')

def create_instance(credentials):

    compute = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)
    project = 'exp-project321'

    zone = 'us-west1-b'

    instance_name = 'newopenvpninstance1ubuntu'
    machine_type = "zones/%s/machineTypes/n1-standard-1" % zone

    image_response = compute.images().getFromFamily(
        project='ubuntu-os-cloud', family='ubuntu-2004-lts').execute()
    source_disk_image = image_response['selfLink']

    startup_script = open(
        os.path.join(
            os.path.dirname(__file__), 'startup-script.sh'), 'r').read()
    image_url = "http://storage.googleapis.com/gce-demo-input/photo.jpg"
    image_caption = "Ready for dessert?"

    sshKey = "cosmos:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC5CFp3ArWNe7npcpaH/cPVnnDUuzADkjtjY3fJDH01zegRAt/MH/oM9YMY4UL2YksCTRLe4Fs7y05tXe6GyR2TrcI/IynEIdvd4MTbhxz0UezzDIcsInRlLoxO5fvNmn9SDSQBSQv7nhbS+bvzSBMPIGcEW1cFsIimPQ152QVA9WsbvPvWJP49AtARmzxeuLxXT7uSshE6akWVayFynsuM0+zwPNFsWZA37qKjr6iuWSlmIPCxXyejipHp91jQICjvPq8yY5leL9b5qLuM0GuH7p0JYTxB9vYEQ72YMctQLZmsGV7H22BOxhAoQ8EhqgO84urnZ1B0MSqbBO6BhzA3 cosmos google-ssh {\"userName\":\"cosmos\",\"expireOn\":\"2023-12-04T20:12:00+0000\"}"


    #reserve and ip address for vm.
    reserve_static_ip(credentials)
    ip_adress= '34.127.42.62'

    instance_body = {

        "machineType": machine_type,
        "name": instance_name,

        # Specify the boot disk and the image to use as a source.
        'disks': [
                     {
                         'boot': True,
                         'autoDelete': True,
                         'initializeParams': {
                             'sourceImage': source_disk_image,
                         }
                     }
        ],
        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT', 'natIP': ip_adress}
            ]
        }],

        # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],
        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': {
            'items': [{
                # Startup script is automatically executed by the
                # instance upon startup.
                'key': 'startup-script',
                'value': startup_script
            }, {
                'key': 'url',
                'value': image_url
            }, {
                'key': 'ssh-keys',
                'value': sshKey
            }, {
                'key': 'text',
                'value': image_caption
            }]
        }
    }


    request = compute.instances().insert(project=project, zone=zone, body=instance_body)
    response = request.execute()

    pprint(response)


def set_firewall_rule(credentials):

    service = googleapiclient.build('compute', 'v1', credentials=credentials)

    # Project ID for this request.
    project = 'exp-project321'  # TODO: Update placeholder value.

    firewall_body = {
        # TODO: Add desired entries to the request body.

        "name": "openVpnRule"
        ""


    }

    request = service.firewalls().insert(project=project, body=firewall_body)
    response = request.execute()

    # TODO: Change code below to process the `response` dict:
    pprint(response)


def reserve_static_ip(credentials):

    service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

    # Project ID for this request.
    project = 'exp-project321'  # TODO: Update placeholder value.

    # Name of the region for this request.
    region = 'us-west1'  # TODO: Update placeholder value.

    address_body = {
        # TODO: Add desired entries to the request body.
        "name": "cosmosaddress",
        # "ipVersion": "IPV6"
    }

    request = service.addresses().insert(project=project, region=region, body=address_body)
    response = request.execute()

    # TODO: Change code below to process the `response` dict:
    pprint(response)


def get_reserved_ip(credentials):

    service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

    # Project ID for this request.
    project = 'exp-project321'  # TODO: Update placeholder value.

    # Name of the region for this request.
    region = 'us-west1'  # TODO: Update placeholder value.

    # Name of the address resource to return.
    address = 'my-address'  # TODO: Update placeholder value.
    id = '1780800848339165366'
    name='operation-1649794649402-5dc7ac007ab14-10f1fa14-f63152e7'


    request = service.addresses().get(project=project, region=region, address=address)
    response = request.execute()

    # TODO: Change code below to process the `response` dict:
    pprint(response)


def list_reserveds(credentials):

    service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

    # Project ID for this request.
    project = 'exp-project321'  # TODO: Update placeholder value.

    # Name of the region for this request.
    region = 'us-west1'  # TODO: Update placeholder value.

    request = service.addresses().list(project=project, region=region)
    while request is not None:
        response = request.execute()

        for address in response['items']:
            # TODO: Change code below to process each `address` resource:
            pprint(address)

        request = service.addresses().list_next(previous_request=request, previous_response=response)



def insert_firewall_rule(credentials):

    service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

    # Project ID for this request.
    project = 'exp-project321'  # TODO: Update placeholder value.

    firewall_body = {
        # TODO: Add desired entries to the request body.
        'name': 'openvpn',
        'sourceRanges': ['0.0.0.0/0'],
        'allowed': [
            {
                'IPProtocol': 'UDP',
                'ports': [
                    '1194'
                ]
            }
        ],

    }

    request = service.firewalls().insert(project=project, body=firewall_body)
    response = request.execute()

    # TODO: Change code below to process the `response` dict:
    pprint(response)