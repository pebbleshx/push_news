import feedparser
import pprint
from pushbullet import Pushbullet
from wxpy import * # wechat client
import time

def send_pb_msg(title, msg):
    ACCESS_TOKEN = 'o.aLZj2KPbkK3HIgYkiK0QaXoXioAc6FxN'
    ACCESS_TOKEN2 = 'o.3aJg1PdLnf5z0m9KDcCCbCytVislbCzG'

    pb = Pushbullet(ACCESS_TOKEN)
    push = pb.push_note(title, msg)

    pb2 = Pushbullet(ACCESS_TOKEN2)
    push2 = pb2.push_note(title, msg)


def contains_wanted(in_str, key_words):
    # returns true if the in_str contains a keyword
    # we are interested in. Case-insensitive
    #print(in_str)
    for wrd in key_words:
        if wrd.lower() in in_str:
            #print(wrd) 
            return True
    return False

def url_is_new(urlstr,urls):
    # returns true if the url string does not exist 
    # in the list of strings extracted from the text file
    if urlstr in urls:
        #print(urlstr)
        return False
    else:
        return True


# Function to fetch the rss feed and return the parsed RSS
def parseRSS( rss_url ):
    return feedparser.parse( rss_url )

# Function grabs the rss feed headlines (titles) and returns them as a list
def getHeadlines( rss_url, bot, my_grp, key_words, urls):
    #headlines = []

    feed = parseRSS( rss_url )
    print(feed)
    #for newsitem in feed['items']:
    #    headlines.append(newsitem['title'])

    #return headlines
    for key in feed["entries"]:
        url = key['links'][0]['href']
        title = key['title']
        #content = key['content']

        if contains_wanted(title.lower(), key_words) and url_is_new(url, urls):
            print('{} - {}'.format(title, url))

            msgtitle = title
            msg = '{}\n{}'.format(title, url)

            #send_pb_msg(msgtitle, msg)
            
            # send to wechat group
            my_grp.send(msg)

            with open('viewed_urls.txt', 'a') as f:
                f.write('{}\n'.format(url))
            with open('news_pushed.txt', 'a') as f2:
                f2.write('{}\n'.format(msg))



def run_main(bot, my_grp):
    
    #key_words = ['Oil','Crude Oil Price', 'OPEC', 'donald trump', 'PetroChina', 'CNPC', 'China', 'china', 'Trump']
    with open('keywords.txt', 'r') as f:
        key_words = f.read().splitlines()

    print(key_words)

    # get the urls we have seen prior
    f = open('viewed_urls.txt', 'r')
    viewed_urls = f.readlines()
    viewed_urls = [url.rstrip() for url in viewed_urls] # remove the '\n' char
    f.close()

    # List of RSS feeds that we will fetch and combine
    newsurls={}
    with open("news_urls.txt") as f_news:
        for line in f_news:
            (key, val) = line.split()
            newsurls[key]=val
  
   
    # Iterate over the feed urls
    for key,url in newsurls.items():
        # Call getHeadlines() and combine the returned headlines with allheadlines
        #allheadlines.extend( getHeadlines( url))
        
        getHeadlines(url, bot, my_grp, key_words,viewed_urls)

def run_backend():
    # init, need to scan QR code to login, cache to autologin
    #bot = Bot(cache_path='wxpy.pkl', console_qr=True,qr_path='./wxpy.pkl') 
    #bot = Bot(console_qr=True,cache_path=True) 
    #bot = Bot(console_qr=2,cache_path='pushnews.pkl', qr_path='qr.png')
    bot = Bot(console_qr=2,cache_path='pushnews.pkl')  

    #this is the group name in your wechat
    my_grp = bot.groups().search('push_news')[0]
    run_main(bot, my_grp)
    
        
if __name__=="__main__":
    #run_backend()
    while True:
        run_backend()
        time.sleep(60*60*2)  

