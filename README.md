stalk-overflow
=============
Get chat notifications for new questions posted on [StackOverflow] for the given tags.


***Why?***

It's such a pain in the *** to continously click on the "n questions with new activity" button and refreshing the StackOverflow page to get updated with information. There doesn't seem to exist any other way of getting notified on what question was recently posted on StackOverflow related to my favourite tags.

It's crucial to get info on latest questions posted ASAP inorder to get a better StackOverflow rating. Thus, I've decided to write a stalking application which would keep an eye on StackOverflow's activity for my favourite tags.

The best part is sice XMPP protocol is being used, users could get notified across all their devices which support chatting!


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

The application uses XMPP protocol which supports most of the chat services like jabber and gtalk

Run the service using

`python2 stalkoverflow.py`

Should prompt you for user id's and passwords for authentication. This works only once. Later asks you to pick tags to stalk on.

Looks like this:

![](http://s30.postimg.org/60l0swy5t/terminal_scrot.png)

And if you're using gmail id you can get notified on hangouts!

![](http://s4.postimg.org/i0nghcn3x/chat_preview.png)



[StackOverflow]:http://stackoverflow.com/
