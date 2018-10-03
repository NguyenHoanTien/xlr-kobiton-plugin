import urllib2
import json
import time
import sys

remoteServer = kobitonServer['remoteServer']

results = {}
listJobs = jobIds.keys()
exitWhenCatchError = False

def main():
  if len(listJobs) < 1:
    print 'No Jobs for waiting.'
    return

  headers = {
    'Content-Type': 'application/json'
  }

  while len(listJobs) > 0:
    for id in listJobs:
      try:
        url = remoteServer + '/' + id + '/status'
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        data = json.loads(response.read())
        
        if data['status'] != 'IN-PROGRESS':
          if data['status'] == 'ERROR' and isExitWhenFail:
            exitWhenCatchError = True
          
          results[id] = str(data['message'])

      except Exception as ex:
        print ex
        results[id] = str(ex)
        if isExitWhenFail:
          exitWhenCatchError = True


    for key in results.keys():
      if key in listJobs:
        index = listJobs.index(key)
        del listJobs[index]
    
    # Delay to avoid DDOS 
    time.sleep(30)


main()

if exitWhenCatchError:
  sys.exit(1)