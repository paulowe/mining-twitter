import sys
from collections import Counter
import json
import matplotlib.pyplot as plt

def get_hastags(tweet):
    #receives list of hashtags from a tweet
    entities = tweet.get('entities', {}) #if no value is present, default {} to avoid key value error
    hashtags = entities.get('hashtags', [])
    return [tag['text'].lower() for tag in hashtags]

if __name__ == '__main__':
    fname = sys.argv[1] #script takes one cli argument fname
    with open(fname, 'r') as f:
        hashtags = Counter() #special dictionary object with strings/tags as key and respective frequency as values. this is an ordered collection and a subclass of dict()
        for line in f: #reads each line, and each line contains a json document (tweet)
            tweet = json.loads(line) #loads each json document into tweet variable
            hashtags_in_tweet = get_hastags(tweet) #helper function extracts a list of hashtags
            hashtags.update(hashtags_in_tweet)
        for tag, count in hashtags.most_common(20):
            print("{}: {}".format(tag, count))

    y = [count for tag, count in hashtags.most_common(20)]
    x = range(1, len(y)+1)

    plt.bar(x, y)
    plt.title("Term frequencies used in US-Iran Stream Data")
    plt.ylabel("Frequency")
    plt.savefig('us-iran-tag-distn.png')
