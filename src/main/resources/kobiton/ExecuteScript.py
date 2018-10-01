import urllib2
import json
import copy

username = kobitonServer['username']
apiKey = kobitonServer['apiKey']

remoteServer = kobitonServer['remoteServer']

defaultDeviceOrientation = kobitonServer['deviceOrientation']
defaultCaptureScreenshots = kobitonServer['captureScreenshots']


def merge_devices():
  mergedList = []

  # Since Kobiton just allow execute automation test
  # by udid on private devices.
  for udid in inputUdid:
    mergedList.append({
      'udid': udid
    })

  if not kobiDevices:
    for id in kobiDevices:
      params = kobiDevices[id].split(' | ')
      if id not in inputUdid:
        mergedList.append({
          'deviceName': params[0],
          'platformName': params[1],
          'platformVersion': params[2],
          'udid': id
        })

  return mergedList


def send_request(devicesList):
  jobIds = {}
  
  if devicesList == []:
    print 'No device to execute tests.'
    return

  headers = {
    'Content-type': 'application/json',
    'Username': username,
    'ApiKey': apiKey
  }

  bodyTemplate = customizeBodyTemplate()

  for device in devicesList:
    try:
      body = copy.deepcopy(bodyTemplate)
      body['desiredCaps'] = dict(bodyTemplate['desiredCaps'].items() + device.items())

      url = remoteServer + '/submit'
      request = urllib2.Request(url, json.dumps(body), headers=headers)
      response = urllib2.urlopen(request)
      body = response.read()

      # Display in output
      # Showing usid of devices if user using private
      jobIds[device['udid'] if not device['deviceName'] else device['deviceName']] = body

    except Exception as ex:
      errorDevice = device['deviceName'] if 'udid' not in device else device['udid']
      print "Error while executing test on {} : {}".format(errorDevice, ex)

  return jobIds

def customizeBodyTemplate():
  # Get customize input in field
  try:
    bodyTemplate = {
      'desiredCaps': {
          'deviceOrientation': deviceOrientation if overrideDesiredCaps else defaultDeviceOrientation,
          'captureScreenshots': captureScreenshots if overrideDesiredCaps else defaultCaptureScreenshots,
          'groupId': groupId
      },
      'testScript': {
          'git': gitUrl,
          'ssh': ssh,
          'config': config
      }
    }

    if testType == 'App':
      bodyTemplate['desiredCaps']['app'] = appUrl

    elif testType == 'Browser':
      if not browserVer or not browserName:
        raise ValueError('Missing browser name or browser version')

      bodyTemplate['desiredCaps']['browserName'] = browserName.lower()
      bodyTemplate['desiredCaps']['browserVer'] = browserVer

  except Exception as ex:
    print "Error while executing test: " + ex 

  return bodyTemplate


mergedList = merge_devices()
jobIds = send_request(mergedList)
