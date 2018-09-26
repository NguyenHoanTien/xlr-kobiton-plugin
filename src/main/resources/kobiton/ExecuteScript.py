import urllib2
import json
import copy

username = kobitonServer['username']
apiKey = kobitonServer['apiKey']

remoteServer = kobitonServer['remoteServer']

defaultDeviceOrientation = kobitonServer['deviceOrientation']
defaultCaptureScreenshots = kobitonServer['captureScreenshots']

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
            'config': config,
            'passphrase': passphrase
        }
    }

    if testType == 'App':
        bodyTemplate['desiredCaps']['app'] = appUrl
    elif testType == 'Browser':
        bodyTemplate['desiredCaps']['browserName'] = browserName
        bodyTemplate['desiredCaps']['browserVer'] = browserVer
    
    headers = {
        'Content-type': 'application/json',
        'Kobiton-Username': username,
        'Kobiton-ApiKey': apiKey
    }

    for device in devicesList:
        try:
            body = copy.deepcopy(bodyTemplate)
            body['desiredCaps'] = dict(bodyTemplate['desiredCaps'].items() + device.items())

            url = EXECUTE_TEST_URL
            request = urllib2.Request(url, json.dumps(body), headers=headers)
            urllib2.urlopen(request)
        except Exception as ex:
            errorDevice = device['deviceName'] if 'udid' not in device else device['udid']
            print "Error while executing test on {} : {}".format(errorDevice, ex)

mergedList = merge_devices()
send_request(mergedList)
