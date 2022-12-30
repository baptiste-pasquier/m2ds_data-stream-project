from kafka import KafkaProducer, KafkaConsumer
import time
import json
from ingest_tweets import RAW_TOPIC, BOOTSTRAP_ENDPOINT, TIME_SLEEP
import re 
import contractions
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
import nltk 

##WARNING FOR LEMMATIZATION, I HAD TO DOWNLOAD MANY THINGS RELATED TO NLTK ()
##SEE HOW TO MAKE SURE THE USER HAS EVERYTHING (OR REPLACE IT IF NOT NECESSARY)
#nltk.download('omw-1.4')
#nltk.download('wordnet')

GROUP_ID = "main_group"
NEGATION_SET = {'no', 'not'}
CLEAN_TOPIC = "clean_tweets"


def get_wordnet_pos(tag):
	"""
		TO DOCUMENT
	"""
	if tag.startswith('J'):
		return wordnet.ADJ
	elif tag.startswith('V'):
		return wordnet.VERB
	elif tag.startswith('N'):
		return wordnet.NOUN
	elif tag.startswith('R'):
		return wordnet.ADV
	else:
		return wordnet.NOUN


def text_cleaning(tweet, fg_stop_words=False, fg_lemmatization=False):
    """
        Clean/Transform the text of a tweet
        
        Arguments
        ---------------------------
            tweet(<str>): String to clean 
            fg_stop_words (<bool>): Remove or not stop words
            fg_lemmatization (<bool>): Apply or not lemmatization


        Returns
        ---------------------------
            tweet(<str>): Tokenized text
            mentions (<list>): List of mentionned users in the tweet (@'s)
            hashtags (<list>): List of hashtags in the tweets (#'s) 
    """
    
    # lowercase
    tweet = tweet.lower()

    # remove extra newlines
    tweet = re.sub(r'[\r|\n|\r\n]+',"",tweet)

    # remove URL
    tweet = re.sub(r'https?://[\S]+', '', tweet)

    # Extract @tag and #tag
    mentions = re.findall(r'@(\w+)',tweet)
    hashtags = re.findall(r'#(\w+)',tweet)
    #Remove them and special chars
    tweet = re.sub('[^A-Za-z0-9]+', ' ', tweet)

    
    # remove contractions
    tweet = ' '.join([contractions.fix(x) for x in tweet.split()])

    # tokenization
    tweet = word_tokenize(tweet)

    if fg_stop_words:        
        # remove stop words
        stop_words = set(stopwords.words('english')).difference(NEGATION_SET)
        tweet = [word for word in tweet if word not in stop_words]
    
    if fg_lemmatization:
        # lemmatization    
        tweet = nltk.tag.pos_tag(tweet)
        tweet = [(word, get_wordnet_pos(pos_tag)) for (word, pos_tag) in tweet]
        wordnet_lemmatizer = WordNetLemmatizer()
        tweet = [wordnet_lemmatizer.lemmatize(word, tag) for (word, tag) in tweet]

    return " ".join(tweet),mentions,hashtags



def main():
	producer = KafkaProducer(
		bootstrap_servers=BOOTSTRAP_ENDPOINT,
		value_serializer=lambda m: json.dumps(m).encode("utf-8"))
	#Call a Consumer to retrieve the raw tweets
	consumer = KafkaConsumer(RAW_TOPIC, 
		bootstrap_servers=BOOTSTRAP_ENDPOINT,
		group_id = GROUP_ID,
		value_deserializer = lambda m: json.loads(m.decode('utf-8')))

	#Preprocess the tweets 
	for data in consumer:
		data = data.value
		print(data['text'])
		print("tsf")
		data['text'],data['mentions'],data['hashtags'] = text_cleaning(data['text'])
		print(data['text'],data['mentions'],data['hashtags'])

		#Send the preprocessed data 
		producer.send(CLEAN_TOPIC,data)

		time.sleep(TIME_SLEEP)

	

if __name__ == "__main__":
	main()