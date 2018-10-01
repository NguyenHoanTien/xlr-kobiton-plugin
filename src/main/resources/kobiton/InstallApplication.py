from org.apache.http.client.methods import HttpPut
from org.apache.http.entity import ByteArrayEntity
from org.apache.http.impl.client import HttpClients
import json
import urllib2
import ntpath

api_server = kobitonServer['url']
username = kobitonServer['username']
api_key = kobitonServer['apiKey']

options = {
    'filename': ntpath.basename(appPath),
    'app_id': '',
}

kobitonAppId = {}


def loader():
    try:
        options['app_id'] = get_id_from_package_name()

        url_data = get_url()

        option = {
            'file_path': str(appPath),
            'url': url_data['url']
        }
        upload_app_status = upload_s3(option)

        if upload_app_status.getStatusCode() != 200:
            raise Exception('S3 upload error' + str(upload_app_status))

        kobiton_app_info = upload_kobiton(url_data['appPath'])

        return {'appId': str().join(['kobiton-store', ':', str(kobiton_app_info['appId'])])}
    except Exception as error:
        print 'Unable to upload application. Error ' + str(error)


def create_basic_authentication_token():
    s = username + ":" + api_key
    return "Basic " + s.encode("base64").rstrip()


def get_id_from_package_name():
    if appPackageName is None or appPackageName == '' or appPackageName.isspace():
        return ''

    header = {
        'content-type': 'application/json',
        'authorization': create_basic_authentication_token()
    }

    request = urllib2.Request(url=api_server + '/v1/apps/', headers=header)

    response = urllib2.urlopen(request)
    data = response.read()
    applications = json.loads(data)

    for application in applications['apps']:
        for version in application['versions']:
            native_properties = version['nativeProperties']
            if native_properties['package'] == appPackageName:
                return str(application['id'])


def get_url():
    content = {
        'filename': options['filename']
    }

    header = {
        'content-type': 'application/json',
        'authorization': create_basic_authentication_token()
    }

    if options['app_id'] != '':
        content.update({'appId': options['app_id']})

    request = urllib2.Request(url=api_server + '/v1/apps/uploadUrl', data=json.dumps(content), headers=header)

    response = urllib2.urlopen(request)
    data = response.read()

    return json.loads(data)


def upload_s3(upload_options={}):
    binary = open(upload_options['file_path'], "rb")
    http_put = HttpPut(upload_options['url'])
    http_put.setHeader('content-type', 'application/octet-stream')
    http_put.setHeader('x-amz-tagging', 'unsaved=true')
    http_put.setEntity(ByteArrayEntity(binary.read()))
    http_client = HttpClients.createDefault()
    response = http_client.execute(http_put)
    return response.getStatusLine()


def upload_kobiton(app_path):
    content = {
        'appPath': app_path,
        'filename': options['filename']
    }

    header = {
        'content-type': 'application/json',
        'authorization': create_basic_authentication_token()
    }

    request = urllib2.Request(url=api_server + '/v1/apps', data=json.dumps(content), headers=header)

    response = urllib2.urlopen(request)
    data = response.read()

    return json.loads(data)


kobitonAppId = loader()
