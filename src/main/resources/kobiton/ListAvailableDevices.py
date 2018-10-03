import json
import re
import urllib2
import copy

# Since the global variable wizard has already checked status of the url, we don't need to perform url checking again.
api_server = kobitonServer['url']
username = kobitonServer['username']
api_key = kobitonServer['apiKey']

group_options = {
  'cloudDevices': isCloud,
  'privateDevices': isPrivate,
  'favoriteDevices': isFavorite
}

platform_options = {
  'Android': isAndroid,
  'iOS': isiOs
}

devices = {}


def get_devices_list():
  filtered_list = {}
  try:
    devices_list = get_all_devices()
    filtered_list = devices_filter(group_options, devices_list)
  except Exception as error:
    print 'Failed to get devices list ' + str(error)
  finally:
    return filtered_list


def get_all_devices():
  auth_token = create_basic_authentication_token()
  url = api_server + '/v1/devices'
  header = {
    "Content-Type": "application/json",
    "Authorization": auth_token
  }
  request = urllib2.Request(url, headers=header)
  response = urllib2.urlopen(request)
  body = response.read()
  return json.loads(body)


def create_basic_authentication_token():
  s = username + ":" + api_key
  return "Basic " + s.encode("base64").rstrip()


def devices_filter(group_options, devices_list=[]):
  classified_list = {}

  for option in group_options:
    if group_options[option]:
      for device in devices_list[option]:
        if device_matches_filter(device) and classified_list.get(device['udid']) is None:
          classified_list.update(serialize_device(device))

  return classified_list


def device_matches_filter(device):
  return device_is_available(device) and device_has_matching_platform(device) and device_contains_name(device)


def device_is_available(device):
  return device['isOnline'] and not device['isBooked']


def device_has_matching_platform(device):
  return platform_options[device['platformName']]


def device_contains_name(device):
  if not model:
    return True

  search_list = model.split(',')
  devices_name = filter(lambda x: x != '' and not x.isspace(), search_list)

  if len(devices_name) == 0:
    return True

  for name in devices_name:
    if re.search(name, device['deviceName'], re.IGNORECASE):
      return True

  return False


def serialize_device(device):
  if device['isCloud']:
    deviceGroup = 'cloudDevices'
  else:
    deviceGroup = 'privateDevices'

  device_data = str().join([device['deviceName'], ' | ', device['platformName'], ' | ', device['platformVersion'], ' | ', deviceGroup])
  serialized_device = {
    device['udid']: str(device_data)
  }

  return serialized_device

devices = get_devices_list()
