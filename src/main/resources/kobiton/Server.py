import sys
import re
import urllib2
import base64

errorLog = []
def ping(params={}, headers={}):
    try:
        request = urllib2.Request(params['url'], None, headers)
        urllib2.urlopen(request)
    except Exception as ex:
        errorLog.append("Error while connecting to {}: {}".format(params['server'], ex))

ping({
    "url": re.sub(r'\/$|\\$','',configuration.url) + '/v1/devices',
    "server": "Kobiton"
}, {
    "Authorization": 'Basic %s' % base64.b64encode('%s:%s' % (configuration.username, configuration.apiKey))
})

ping({
    "url": re.sub(r'\/$|\\$','',configuration.remoteServer) + '/ping',
    "server": "Remote Server"
})

if errorLog != []:
    sys.exit(errorLog)
