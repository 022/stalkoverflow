stalk-overflow
=============
Get chat notifications for new questions posted on [StackOverflow] for a given tag.


***Why?***

It's such a pain in the *** to continously click on the "n questions with new activity" button and refreshing the SO page to get updated with information. There doesn't seem to exist any other way of getting notified on what question was recently posted on SO related to my favourite tags.

It's crucial to get info on latest questions posted ASAP inorder to get a better SO rating. Thus, I've decided to write a stalking application which would keep an eye on SO's activity for my favourite tags.

The best part is sice xmpp protocol is being used, users could get notified across all their devices which support chatting!


**Requirements:**

* dnspython
* sleekxmpp
* feedparser

All the above mentioned packages are available in pip.


**Setup:**

Clone this repo

`git clone https://github.com/022/stalkoverflow.git`

Make sure you install all requirements

`sudo pip2 install -r requirements.txt`

Setup your chat preferences in `secret.py` . The script uses xmpp protocol which supports most of the chat services like jabber and gtalk

Run the service using

`python2 stalkoverflow.py`


[StackOverflow]:http://stackoverflow.com/
