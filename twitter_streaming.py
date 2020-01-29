import sys
import string
import time
from tweepy import Stream
from tweepy.streaming import StreamListener
from twitterclient import get_twitter_auth


class CustomListener(StreamListener):
    """ Custom StreamListener for streaming twitter data."""

    def __init__(self, fname):
        safe_fname = format_filename(fname)
        self.outfile = "stream_%s.jsonl" % safe_fname

    def on_data(self, data):
        #called when data is coming through. This method simply stores data as it is received in a .jsonl file. Each line in this file will contain a single tweet in json format
        # return True after data is written, any other errors will be caught and we will write it to our log file, put the application to sleep for 5 seconds and return true to continue execution
        try:
            with open(self.outfile, 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            sys.stderr.write("Error on_data: {}\n".format(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        #this method will deal with explicit errors from twitter. Theres a complete list of error codes and responses on the twitter API
        #we are specifically looking to stop execution only on error 420 - Rate limit
        if status == 420:
            sys.stderr.write("Rate limit exceeded\n")
            return False #stops execution only on fail
        else:
            sys.stderr.write("Error {}\n".format(status))
            return True


def format_filename(fname):
    """ Convert fname into a safe string fo a file name.
        Return string.
    """

    return ''.join(convert_valid(one_char) for one_char in fname)

def convert_valid(one_char):

    """ Converts a character into '_' if "invalid".
        Return string.
    """

    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'

# when we run this script we have to provide arguments in the command line, separated by whitespace.
#For example in your CLI you can run: python3 twitter_streaming.py \#popularhashtag1 \#popularhashtag2 search_keyword**
#Stream for about 1 hour and retrieve results in your jsonl file
if __name__ == '__main__':
    query = sys.argv[1:] # list of CLI argumentsquery_fname
    query_fname = ' '.join(query) # string
    auth = get_twitter_auth()
    twitter_stream = Stream(auth, CustomListener(query_fname))
    twitter_stream.filter(track=query, is_async=True)
