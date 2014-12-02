#!/bin/python2
import time
import os
import sys
import getpass
import sleekxmpp
import signal
import pickle
import tempfile
import getpass
import urllib2
import twitter

from optparse import OptionParser
from datetime import datetime
from BeautifulSoup import BeautifulSoup
from HTMLParser import HTMLParser

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
    if authority["chat_type"] == "xmpp":
        xmpp = SendMsgBot(authority["x_sender_id"], authority["x_password"], authority["x_to"], message)
        xmpp.register_plugin('xep_0030') # Service Discovery
        xmpp.register_plugin('xep_0199') # XMPP Ping
    
        if xmpp.connect():
            xmpp.process(block=True)
        else:
            print("Unable to connect.")
    elif authority["chat_type"] == "twitter":
        api = twitter.Api(consumer_key=authority["t_consumer_key"],
                          consumer_secret=authority["t_consumer_secret"],
                          access_token_key=authority["t_access_token_key"],
                          access_token_secret=authority["t_access_token_secret"])

        def send_message(message):
            if message:
                api.PostDirectMessage(message[:140], screen_name=authority["t_to"])
                message = message[140:]
                send_message(message)
                
        send_message(message)


def signal_handling(signum, frame):
    sys.exit()
    
def get_option_parser():
    options = OptionParser(description=__doc__)
    options.add_option('--auth', action="store_true", dest='reauth', default=False, help="Re run authenticative process")
    options.add_option('--delay', action="store_true", dest='delay', default=20, help="Time delay in seconds")
    return options.parse_args()
                    
def authenticate(reauth):
    temp_file = "stalkoverflow.pkl"
    temp_file_path =  os.path.join(tempfile.gettempdir(), temp_file)
    if os.path.exists(temp_file_path) and not reauth:
        authority = pickle.load(open(temp_file_path))
    else:
        print "Requesting info for initial setup:"
        authority = {}
        authority["chat_type"] = raw_input("Do you want to get notified over xmpp(like google hangouts) or twitter ?\n[1] xmpp\n[2] twitter\n : ")
        if authority["chat_type"] == "1":
            authority["chat_type"] = "xmpp"
            authority["x_to"] = raw_input("send notifications to (self@gmail.com) ")
            authority["x_sender_id"] = raw_input("ID used for sending notifications (id@gmail.com) ")
            authority["x_password"] = getpass.getpass("password (for {0}) ".format(authority["x_sender_id"]))
        elif authority["chat_type"] == "2":
            authority["chat_type"] = "twitter"
            authority["t_to"] = raw_input("send messages to (twitter id) ")
            authority["t_consumer_key"] =  raw_input("consumer_key: ")
            authority["t_consumer_secret"] =  raw_input("consumer_secret: ")
            authority["t_access_token_key"] =  raw_input("access_token_key: ")
            authority["t_access_token_secret"] =  raw_input("access_token_secret: ")
        else:
            print "unknown option"
            print "exiting"
            sys.exit()
        pickle.dump(authority, open(temp_file_path,"wb"))
    return authority

def parseFeed(rss_url, h):
    page = urllib2.urlopen(rss_url)
    soup = BeautifulSoup(page)

    for el in soup.findAll("div", {"class":"question-summary"}, limit=1):
        new_title = h.unescape(el.find("h3").text)
        new_link = "http://stackoverflow.com" + el.find("h3").find("a").get("href")
        new_link = new_link[:new_link.rfind("/")]
        question_id = new_link.split("/")[-1]
    
    return new_title, new_link, question_id

def stalk(tags, authority, delay, h):
    tagnames = tags.replace(' ','').replace(',','+or+')
    rss_url="http://stackoverflow.com/questions/tagged/"+tagnames+"?sort=newest&pageSize=10"
    title, link, new_question_id = parseFeed(rss_url, h)
    old_question_id = ""
    question_buffer = []

    while True:
        if new_question_id in question_buffer:
            title, link, new_question_id = parseFeed(rss_url, h)
        else:
            print "[{}]: {}".format(datetime.now(), title)
            question_buffer.append(new_question_id)
            send_chat(title+"""
            """+link, authority)
        time.sleep(delay)
        if len(question_buffer) > 120:
            del question_buffer[0:-20]
        
def main():
    signal.signal(signal.SIGINT, signal_handling)
    opts, args =  get_option_parser()
    authority = authenticate(opts.reauth)
    tags = raw_input("Enter tags to stalk on: ")
    send_chat("Started stalking {0} on StalkOverflow ".format(tags), authority)
    h = HTMLParser()
    stalk(tags, authority, opts.delay, h)
    
if __name__ == "__main__":
    main()
