import time
import dateutil.parser
import dateutil.tz
import logging
import feedparser
from django.conf import settings
from django.db import transaction
from django.utils.encoding import smart_unicode
from jellybaby.models import Item, Bookmark
from bookmarks.models import Bookmark as Bookmark2
from django.contrib.auth.models import User
from jellybaby.providers import utils
from BeautifulSoup import BeautifulStoneSoup

#
# Public API
#

log = logging.getLogger("jellybaby.providers.delicious")

def enabled():
    return True
    
def update():
    d = feedparser.parse("http://feeds.delicious.com/rss/bittered/%s" % \
     "ojax")

    # Check to see if we need an update
    last_update_date = Item.objects.get_last_update_of_model(Bookmark)
    try:
        last_post_date = utils.parsedate(d.entries[0].updated)
        if last_post_date <= last_update_date:
            log.info("Skipping update: last update date: %s; last post date: %s", \
             last_update_date, last_post_date)
            return
    except:
        pass

            
    for entry in d.entries:
        dt = utils.parsedate(entry.updated)
        if dt > last_update_date:
            _prepare_bookmark(entry, dt)
                
#
# Private API
#

@transaction.commit_on_success
def _prepare_bookmark(entry, dt):
    """docstring for _add_bookmark"""
    
    try: url = entry.links[0].href
    except: url = ""
    
    try: description = str(BeautifulStoneSoup(entry.title, \
    convertEntities=BeautifulStoneSoup.ALL_ENTITIES))
    except: description = ""
    
    try: extended = str(BeautifulStoneSoup(entry.summary_detail.value, \
    convertEntities=BeautifulStoneSoup.ALL_ENTITIES))
    except: extended = ""
    
    try: tags = entry.tags[0].term
    except: tags = ""
    
    try: username = entry.author
    except: username = ""
    
    # try:
    #      User.objects.get(delicioususer__delicious_username=username)
    # except User.DoesNotExist:
    #     log.info("Skipping bookmark: %s from %s. User does not exist", \
    #         url, username)
    #     return
    # except User.MultipleObjectsReturned:
    #     pass
    
    log.debug("Handling bookmark: %s from %s.", url, username)
    _handle_bookmark(url, description, extended, tags, username, dt)

def _handle_bookmark(url, description, extended, tags, username, dt):
    b, created = Bookmark.objects.get_or_create(
        url         = url,
        description = description,
        extended    = extended,
    )
    if not created:
        b.url           = url
        b.description   = description
        b.extended      = extended
        b.save()

    dave = User.objects.get(username="dave")
    Bookmark2(
        url=url,
        description=description,
        note=extended,
        has_favicon=False,
        adder=dave
    ).save()
    
    return Item.objects.create_or_update(
        instance    = b,
        timestamp   = dt,
        tags        = tags,
        username    = username,
        source      = __name__,
    )

