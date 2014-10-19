stalk-overflow
=============
Get chat notifications for new questions posted on [StackOverflow] for the given tags.


***Why?***

It's such a pain to continuously click on the "n questions with new activity" button and refreshing the StackOverflow page to get updated with information. There doesn't seem to exist any other way of getting notified on what question was recently posted on StackOverflow related to my favorite tags.

It's crucial to get info on latest questions posted ASAP in order to get a better StackOverflow rating. Thus, I've decided to write a stalking application which would keep an eye on StackOverflow's activity for my favorite tags.

The best part is since XMPP protocol is being used, users could get notified across all their devices which support chatting!


**Requirements:**

* python 2.7
* dnspython
* sleekxmpp
* beautifulsoup
* python-twitter

All the above mentioned packages are available in pip.


**Setup:**

Clone this repo

`git clone https://github.com/alella/stalkoverflow.git`

Make sure you install all requirements

`sudo pip install -r requirements.txt`

The application uses XMPP protocol which supports most of the chat services like jabber and google-hangouts. Alternatively twitter chat can also be used

Run the service using

`python stalkoverflow.py`

Should prompt you for user id's and passwords for authentication. This information is stored until your system is switched off. Later asks you to pick tags to stalk on. If you're trying to get notified over twitter you need api keys and tokens.

Looks like this:

![](http://s30.postimg.org/60l0swy5t/terminal_scrot.png)

And if you're using a gmail-id you can get notified on hangouts!

![](http://s4.postimg.org/i0nghcn3x/chat_preview.png)

Extra argument specifications:
```
Usage: stalkoverflow.py [options]

Options:
  -h, --help  show this help message and exit
  --auth      Re run authentication process
  --delay     Time delay in seconds
```


[StackOverflow]:http://stackoverflow.com/
