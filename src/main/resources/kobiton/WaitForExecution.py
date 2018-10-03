import urllib2
import json
import time
import sys

results = {}
listJobs = jobIds.keys()

def main():
  if len(listJobs) < 1:
    print 'No Jobs for waiting.'
    return

  headers = {
    'Content-Type': 'application/json'
  }

  exit = False
  
  while len(listJobs) > 0:
    for id in listJobs:
      try:
        url = kobitonServer['remoteServer'] + '/' + id + '/status'
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        data = json.loads(response.read())
        
        if data['status'] != 'IN-PROGRESS':
          if data['status'] == 'ERROR' and exitWhenFail:
            exit = True
          results[id] = str(data['message'])
      except Exception as ex:
        print ex
        results[id] = str(ex)
        if exitWhenFail:
          exit = True

    for key in results.keys():
      if key in listJobs:
        index = listJobs.index(key)
        del listJobs[index]
    
    # Delay to avoid DDOS 
    time.sleep(30)

main()

if exit:
  sys.exit(1)