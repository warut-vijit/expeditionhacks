from splinter.browser import Browser
from splinter.exceptions import ElementDoesNotExist

def get_events():
  events = []
  br = Browser('phantomjs')
  br.visit('http://do512.com')
  listings = br.find_by_css('.ds-listing')
  for listing in listings:
    try:
      name = listing.find_by_css('.ds-listing-event-title-text').first.value
      interest = int(listing.find_by_css('.ds-upvote-default').first.value)
    except ElementDoesNotExist: continue
    except ValueError: continue
    if(name==''): continue
    events.append( {
      'name': name, 
      'interest': interest
    }) 
  return events
