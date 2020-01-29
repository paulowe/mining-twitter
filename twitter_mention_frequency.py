#This script can be run to find out the most common tags from a timeline, a users page or any jsonl file we posess

import sys
from collections import Counter
import json

def get_mentions(tweet):
    #receives list of hashtags from a tweet
    entities = tweet.get('entities', {}) #if no value is present, default {} to avoid key value error
    mentions = entities.get('user_mentions', [])
    return [tag['screen_name'].lower() for tag in mentions]

if __name__ == '__main__':
    fname = sys.argv[1] #script takes one cli argument fname
    with open(fname, 'r') as f:
        mentionfreq = Counter() #special dictionary object with strings as key and respective frequency(count) as values. this is an ordered collection and a subclass of dict()
        for line in f: #reads each line, and each line contains a json document (tweet)
            tweet = json.loads(line) #loads each json document into tweet variable
            mentions_in_tweet = get_mentions(tweet) #helper function extracts a list of hashtags
            mentionfreq.update(mentions_in_tweet) #binds the keys, value pairs/ our dictionary
        for tag, count in mentionfreq.most_common(20):
            print("{}: {}".format(tag, count))
