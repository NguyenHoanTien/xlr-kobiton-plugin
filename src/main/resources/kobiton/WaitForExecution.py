import urllib2
import json
import time

results = {}
listJobs = jobIds.keys()

def main():
  if len(listJobs) < 1:
    print 'No Jobs for waiting.'
    return

  headers = {
    'Content-Type': 'application/json'
  }

  while len(listJobs) > 0:
    for id in listJobs:
      url = kobitonServer['remoteServer'] + '/' + id + '/status'
      request = urllib2.Request(url, headers=headers)
      response = urllib2.urlopen(request)
      data = json.loads(response.read())
      
      if data['status'] != 'IN-PROGRESS':
        results[id] = str(data['message'])

    for key in results.keys():
      if key in listJobs:
        index = listJobs.index(key)
        del listJobs[index]
    
    # Delay to avoid DDOS 
    time.sleep(60)

main()