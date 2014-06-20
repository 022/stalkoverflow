import time
import os
import feedparser
import sys
import logging
import getpass
import sleekxmpp
import signal
import secret
from optparse import OptionParser
from datetime import datetime

class SendMsgBot(sleekxmpp.ClientXMPP):
    def __init__(self, sender_id, password, recipient, message):
        sleekxmpp.ClientXMPP.__init__(self, sender_id, password)
        self.recipient = recipient
        self.msg = message
        self.add_event_handler("session_start", self.start)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')
        self.disconnect(wait=True)

def send_chat(message):
    xmpp = SendMsgBot(secret.sender_id, secret.password, secret.to, message)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0199') # XMPP Ping

    if xmpp.connect():
        xmpp.process(block=True)
    else:
        print("Unable to connect.")

def setup_logging():
    logging.basicConfig(filename='logs/stalkLog{0}.txt'.format(datetime.now().strftime('%Y%m%d_%H_%M_%S')), format="[%(asctime)s][%(levelname)s] %(message)s", datefmt="%Y%m%d %H:%M:%S", level=logging.INFO)

def signal_handling(signum, frame):
    send_chat("Bye!")
    sys.exit()
    
def stalk(tag):
    rss_url="http://stackoverflow.com/feeds/tag?tagnames="+tag+"&sort=newest"
    logging.info("rss url = {0}".format(rss_url))
    feed=feedparser.parse(rss_url)
    new_title=feed["entries"][0]["title"]
    new_link=feed["entries"][0]["link"]
    old_title=""

    while True:
        if new_title == old_title:
            feed = feedparser.parse(rss_url)
            new_title = feed["entries"][0]["title"]
            new_link = feed["entries"][0]["link"]
        else:
            old_title = new_title
            logging.info(new_title)
            logging.info(new_link)
            send_chat(new_title+"""
            """+new_link)
        time.sleep(1)
        
def main():
    signal.signal(signal.SIGINT, signal_handling)
    setup_logging()
    tag=raw_input("Enter a tag to stalk on: ")
    send_chat("Started stalking {0} on StalkOverflow B) ".format(tag))
    logging.info("Tag = ".format(tag))
    logging.info("Started stalking {0} on StalkOverflow".format(tag))
    stalk(tag)
    
if __name__ == "__main__":
    main()
