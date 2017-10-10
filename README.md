stalk-overflow
=============
Get chat notifications for new questions posted on [StackOverflow] for the given tags.


***Why?***

It's such a pain to continuously click on the "n questions with new activity" button and refreshing the StackOverflow page to get updated with information. There doesn't seem to exist any other way of getting notified on what question was recently posted on StackOverflow related to my favorite tags.

It's crucial to get info on latest questions posted ASAP in order to get a better StackOverflow rating. Thus, I've decided to write a stalking application which would keep an eye on StackOverflow's activity for my favorite tags.

this application currently supports messaging through pushbullet, hangouts, twitter.


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

Run the service using

`python stalkoverflow.py`

That should prompt you for selecting a messaging platform. Choosing pushbullet is recommended. Then, enter your developer api token.

This information is stored until your system is switched off. Later asks you to pick tags to stalk on.

Looks like this:

![](https://s1.postimg.org/7y0f1y2cfz/scrot_M0j_Zs.png)

<p>&nbsp;</p>And if you're using a gmail-id you can get notified on hangouts!

<center><img src="https://s1.postimg.org/1wehacfmcf/scrot5f_Wok.png" width="400"></center><p>&nbsp;</p><p>&nbsp;</p>

Extra argument specifications:
```
Usage: stalkoverflow.py [options]

Options:
  -h, --help  show this help message and exit
  --auth      Re run authentication process
  --delay     Time delay in seconds
```


[StackOverflow]:http://stackoverflow.com/
