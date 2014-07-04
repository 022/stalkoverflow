import time
import os
import sys
import logging
import getpass
import sleekxmpp
import signal
import pickle
import tempfile
import getpass
import urllib2

from optparse import OptionParser
from datetime import datetime
from BeautifulSoup import BeautifulSoup

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

def send_chat(message, authority):
    xmpp = SendMsgBot(authority["sender_id"], authority["password"], authority["to"], message)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0199') # XMPP Ping

    if xmpp.connect():
        xmpp.process(block=True)
    else:
        print("Unable to connect.")

def setup_logging():
    if not os.path.exists('logs'):
        os.mkdir('logs')
    logging.basicConfig(filename='logs/stalkLog{0}.txt'.format(datetime.now().strftime('%Y%m%d_%H_%M_%S')), format="[%(asctime)s][%(levelname)s] %(message)s", datefmt="%Y%m%d %H:%M:%S", level=logging.INFO)

def signal_handling(signum, frame):
    logging.info("Exiting")
    sys.exit()
    
def get_option_parser():
    options = OptionParser(description=__doc__)
    options.add_option('--auth', action="store_true", dest='reauth', default=False, help="Re run authenticative process")
    options.add_option('--logs', action="store_true", dest='logs_on', default=False, help="Log output to disk")
    return options.parse_args()
                    
def authenticate(reauth):
    temp_file = "stalkoverflow.pkl"
    temp_file_path =  os.path.join(tempfile.gettempdir(), temp_file)
    if os.path.exists(temp_file_path) and not reauth:
        authority = pickle.load(open(temp_file_path))
    else:
        print "Requesting info for initial setup:"
        authority = {}
        authority["to"] = raw_input("send notifications to (self@gmail.com) ")
        authority["sender_id"] = raw_input("ID used for sending notifications (id@gmail.com) ")
        authority["password"] = getpass.getpass("password (for {0}) ".format(authority["sender_id"]))
        pickle.dump(authority, open(temp_file_path,"wb"))
    return authority

def parseFeed(rss_url):
    print "ping "+datetime.now().strftime("%H:%M:%S")
    page = urllib2.urlopen(rss_url)
    soup = BeautifulSoup(page)

    for el in soup.findAll("div", {"class":"question-summary"}, limit=1):
        new_title = el.find("h3").text
        new_link = "http://stackoverflow.com" + el.find("h3").find("a").get("href")
        new_link = new_link[:new_link.rfind("/")]
    
    return new_title, new_link

def stalk(tags, authority):
    tagnames = tags.replace(' ','').replace(',','+or+')
    rss_url="http://stackoverflow.com/questions/tagged/"+tagnames+"?sort=newest&pageSize=10"
    logging.info("rss url = {0}".format(rss_url))
    new_title, new_link = parseFeed(rss_url)
    old_title=""

    while True:
        if new_title == old_title:
            new_title, new_link = parseFeed(rss_url)
        else:
            old_title = new_title
            logging.info(new_title)
            logging.info(new_link)
            send_chat(new_title+"""
            """+new_link, authority)
        time.sleep(10)
        
def main():
    signal.signal(signal.SIGINT, signal_handling)
    opts, args =  get_option_parser()
    authority = authenticate(opts.reauth)
    if opts.logs_on:
        setup_logging()
    tags = raw_input("Enter tags to stalk on: ")
    send_chat("Started stalking {0} on StalkOverflow B-) ".format(tags), authority)
    logging.info("Tags = ".format(tags))
    logging.info("Started stalking {0} on StalkOverflow".format(tags))
    stalk(tags, authority)
    
if __name__ == "__main__":
    main()
