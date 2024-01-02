import pandas as pd
import spacy
from spacy import Language
from spacy.tokens import Doc
from sense2vec import Sense2Vec
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import os.path

s2v = Sense2Vec().from_disk("../s2v_old")
# Create a pipe that converts lemmas to lower case:
@Language.component("lower_case_lemmas")
def lower_case_lemmas(doc) :
    for token in doc :
        token.lemma_ = token.lemma_.lower()
    return doc
# Initialize default spaCy pipeline
nlp = spacy.load('en_core_web_sm', disable=['ner'])
# lower_case_lemmas to pipeline
nlp.add_pipe(factory_name="lower_case_lemmas", after="tagger")

# saves the pretrained sentiment analysis model if user doesn't have it
model_name = "siebert/sentiment-roberta-large-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def toDocs(reviews : list[str]):
  return list(nlp.pipe(reviews))

# Detect whether or not a topic defined by topic_list is present in a sentence (span from spaCy doc)
def topicDetection(sentence, topic_list : list[str], pos : list[str], thresh, exclude_tokens = []) -> bool:
    for token in sentence:
      if token.pos_ not in pos or token.lemma_ in exclude_tokens:
        continue
      # Construct string to pass to Sense2Vec
      s = token.lemma_ + "|" + token.pos_
      # Only consider tokens that Sense2Vec model knows and are from specified part of speech
      # True if token is similar to topic_list
      if s in s2v and s2v.similarity(s, topic_list) > thresh:
        return True
    # Otherwise, topic not detected in sentence
    return False

class SentimentDetector:
# docs is a list of spaCy docs, each representing a restaurant review
  def __init__(self, docs : list[Doc]):
    food = ["food|NOUN", "pizza|NOUN", "meal|NOUN", "taco|NOUN", "chinese|ADJ", "mexican|ADJ", "sushi|NOUN", "bone|NOUN", "drink|NOUN", "pho|NOUN", "curry|NOUN", "coffee|NOUN", "teriyaki|NOUN"]
    service = ["waiter|NOUN", "staff|NOUN", "service|NOUN", "employee|NOUN"]
    location = ["crowded|ADJ", "atmosphere|NOUN", "quiet|ADJ", "interior|NOUN", "music|NOUN", "environment|NOUN", "space|NOUN", "vibe|NOUN", "location|NOUN"]
    clean = ["clean|ADJ", "dirty|ADJ", "fly|NOUN", "cockroach|NOUN", "filthy|ADJ", "spotless|ADJ"]
    price = ["cheap|ADJ", "expensive|ADJ", "price|NOUN", "worth|NOUN", "payment|NOUN", "tip|NOUN"]
    
    pos_food, pos_service, pos_location, pos_clean, pos_price = 0, 0, 0, 0, 0
    neg_food, neg_service, neg_location, neg_clean, neg_price = 0, 0, 0, 0, 0

    self.num_reviews = 0
    
    for doc in docs:
      # currently every newline marks a different review 
      if len(doc) != 0: self.num_reviews += 1      
      
      for sentence in doc.sents:
        sentence_topic = []
        # creates a list of topics the sentence is talking about
        if topicDetection(sentence, food, ["NOUN", "ADJ"], 0.6):
          sentence_topic.append("food")
        if topicDetection(sentence, service, ["NOUN", "ADJ"], 0.7, ["restaurant", "restraunt", "restaraunt"]):
          sentence_topic.append("service")
        if topicDetection(sentence, location, ["NOUN", "ADJ"], 0.67):
          sentence_topic.append("location")
        if topicDetection(sentence, clean, ["NOUN", "ADJ"], 0.7):
          sentence_topic.append("clean")
        if topicDetection(sentence, price, ["NOUN", "ADJ"], 0.7):
          sentence_topic.append("price") 

        sentiment = sentiment_pipeline(sentence.text)[0]
        # if the setence was positive, add to the positive topics (whatever was in the sentence)
        if sentiment['label'] == "POSITIVE":
          if "food" in sentence_topic: pos_food += 1
          if "service" in sentence_topic: pos_service += 1
          if "location" in sentence_topic: pos_location += 1
          if "clean" in sentence_topic: pos_clean += 1
          if "price" in sentence_topic: pos_price += 1
        else: 
          if "food" in sentence_topic: neg_food += 1
          if "service" in sentence_topic: neg_service += 1
          if "location" in sentence_topic: neg_location += 1
          if "clean" in sentence_topic: neg_clean += 1
          if "price" in sentence_topic: neg_price += 1

    self.raw_count = [pos_food, pos_service, pos_location, pos_clean, pos_price, neg_food, neg_service, neg_location, neg_clean, neg_price]
    if self.num_reviews == 0: self.num_reviews = 1
    
  def sentiment_count(self):
    keys = ["+food", "+service", "+location", "+clean", "+price", "-food", "-service", "-location", "-clean", "-price",]
    return {key: count for key, count in zip(keys, self.raw_count)}
    
  def weighted_input(self):
    return [float(x) / self.num_reviews for x in self.raw_count]


# DUMMY REVIEWS
# reviews = [
#     "I stumbled upon this hidden gem last night and had the most amazing dining experience. The atmosphere was cozy, the staff was friendly, and the food was a culinary masterpiece. I highly recommend the chef's special – a true delight for your taste buds!",
#     "This restaurant is a decent option if you're looking for a quick bite. The service was prompt, and the menu had a variety of options. The prices were reasonable, but don't expect anything extraordinary. It's a convenient choice for a casual meal.",
#     "From the moment we walked in, the staff made us feel welcome. The chef's recommendations were spot-on, and each dish was a culinary delight. The attention to detail and unique flavors set this restaurant apart. We left with happy taste buds!",
#     "I can't understand the hype around this place. The prices are exorbitant for the quality of food served. I ordered a dish that was supposed to be a specialty, but it was bland and lacked the promised flavors. Also the bathrooms were very dirty.Definitely not worth the money.",
#     "The restaurant had a nice ambiance, and the service was courteous. The food, however, was average. Nothing stood out, but nothing was terrible either. If you're in the neighborhood and need a meal, it's an okay choice, but I wouldn't go out of my way to dine here.",
#     "I'm thrilled to have discovered this hidden gem! The staff was friendly, the menu had a great selection, and the food was absolutely delicious. The prices were reasonable, making it a fantastic value for the quality of the dining experience. Can't wait to come back!"
# ]

# sd = SentimentDetector(toDocs(reviews))
# print(sd.sentiment_count())
