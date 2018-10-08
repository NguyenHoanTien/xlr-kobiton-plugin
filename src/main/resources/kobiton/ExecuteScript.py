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

  # Kobiton only allows execute automation test
  # by udid on private devices.
  for udid in inputUdid:
    mergedList.append({
      'udid': udid,
      'deviceGroup' : 'any'
    })

  if kobiDevices:
    for id in kobiDevices:
      params = kobiDevices[id].split(' | ')
      if id not in inputUdid:
        temp = {
          'deviceName' : params[0],
          'platformName': params[1],
          'platformVersion': params[2]
        }

        if params[3] == 'privateDevices':
          temp['udid'] = id
          temp['deviceGroup'] = 'any'

        mergedList.append(temp)

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
      if device.has_key('udid'):
        jobIds[body] = device['udid']
      else:
        jobIds[body] = device['deviceName']

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
      bodyTemplate['desiredCaps']['browserName'] = browserName.lower()
      
  except Exception as ex:
    print "Error while executing test: " + ex 

  return bodyTemplate

mergedList = merge_devices()
jobIds = send_request(mergedList)