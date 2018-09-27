import urllib2
import json
import copy

username = kobitonServer['username']
apiKey = kobitonServer['apiKey']

remoteServer = kobitonServer['remoteServer']

defaultDeviceOrientation = kobitonServer['deviceOrientation']
defaultCaptureScreenshots = kobitonServer['captureScreenshots']

jobIds = {}

EXECUTE_TEST_URL = remoteServer + '/submit'

def merge_devices():
  result = []
  for udid in privateDevices:
    result.append({
        'udid': udid
    })

  for id in kobiDevices:
    params = kobiDevices[id].split(' | ')
    if params[3] == 'cloudDevices':
      result.append({
          'deviceName': params[0],
          'platformName': params[1],
          'platformVersion': params[2]
      })
    elif (id in privateDevices) == False:
          result.append({
              'udid': id
          })
    
  return result

def yaml_to_json(yamlString):
  yamlArray = yamlString.split('\n')
  yamlArray = [s for s in yamlArray if s.strip()]

  jsonConfig = {}

  i = 0
  while i < len(yamlArray):
    line = yamlArray[i].strip()
    if line[-1:] == ':':
        line = line[:-1]
        if jsonConfig.has_key(line) is False:
            jsonConfig[line] = []

        j = i+1
        while j < len(yamlArray):
            item = yamlArray[j].strip()
            if item[0] == '-':
                jsonConfig[line].append(item[1:])
            elif item[-1:] == ':':
                break                
            j = j + 1

        i = j
        continue
    i = i + 1

  return jsonConfig

def send_request(devicesList):
  if devicesList == []:
    print 'No device to execute tests.'
    return

  bodyTemplate = {
    'desiredCaps': {
        'deviceOrientation': deviceOrientation if overrideDesiredCaps else defaultDeviceOrientation,
        'captureScreenshots': captureScreenshots if overrideDesiredCaps else defaultCaptureScreenshots,
    },
    'testScript': {
        'git': gitUrl,
        'ssh': ssh,
        'config': yaml_to_json(config),
        'passphrase': passphrase
    }
  }

  if testType == 'App':
    bodyTemplate['desiredCaps']['app'] = appUrl
  elif testType == 'Browser' and browserName is not None:
    bodyTemplate['desiredCaps']['browserName'] = browserName.lower()
    bodyTemplate['desiredCaps']['browserVer'] = browserVer
  
  headers = {
    'Content-type': 'application/json',
    'Kobiton-Username': username,
    'Kobiton-ApiKey': apiKey
  }

  jobIdsKeys = 0

  for device in devicesList:
    try:
      jobIdsKeys = jobIdsKeys + 1
      body = copy.deepcopy(bodyTemplate)
      body['desiredCaps'] = dict(bodyTemplate['desiredCaps'].items() + device.items())

      url = EXECUTE_TEST_URL
      request = urllib2.Request(url, json.dumps(body), headers=headers)
      response = urllib2.urlopen(request)
      jobIds[str(jobIdsKeys)] = response['jobId']
    except Exception as ex:
      errorDevice = device['deviceName'] if 'udid' not in device else device['udid']
      print "Error while executing test on {} : {}".format(errorDevice, ex)

mergedList = merge_devices()
send_request(mergedList)
