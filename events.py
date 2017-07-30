from splinter.browser import Browser
from datetime import datetime
import re
import logging

def get_events():
  events = []
  try:
    f = open('event.cache', 'r')
    logging.error("cache found")
    for line in f:
      event = line.split(';;;')
      events.append( {
        'name': event[0],
        'interest': int(event[1]),
        'lat': float(event[2]),
        'long': float(event[3]),
        'time': event[4]
      })
    return events
  except IOError:
    pass
  br = Browser('phantomjs')
  br.visit('http://do512.com')
  listings = br.find_by_css('.ds-listing')
  f = open('event.cache', 'w')
  for listing in listings:
    try:
      name = listing.find_by_css('.ds-listing-event-title-text').first.value
      interest = int(listing.find_by_css('.ds-upvote-default').first.value)
      lat = float(listing.find_by_css('.latitude').find_by_tag('span')._element.get_attribute('title'))
      long = float(listing.find_by_css('.longitude').find_by_tag('span')._element.get_attribute('title'))
      tstr = listing.find_by_css('.ds-event-time').first.value
      tparse = re.search('\d{1,2}:\d{2}[AP]M', tstr).group(0) 
      time = datetime.strptime(tparse, '%I:%M%p')
      tiso = datetime.today().replace(hour=time.hour, minute=time.minute).isoformat()
    except: continue
    if(name==''): continue
    f.write(name+';;;'+str(interest)+';;;'+str(lat)+';;;'+str(long)+';;;'+tiso+'\n')
    events.append( {
      'name': name, 
      'interest': interest,
      'lat': lat,
      'long': long,
      'time': tiso
    })
    
  return events

