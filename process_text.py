import pandas as pd
import spacy
from spacy import Language
from sense2vec import Sense2Vec

s2v = Sense2Vec().from_disk("s2v_old")
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

'''
## DUMMY REVIEWS
reviews = [
    "I stumbled upon this hidden gem last night and had the most amazing dining experience. The atmosphere was cozy, the staff was friendly, and the food was a culinary masterpiece. I highly recommend the chef's special – a true delight for your taste buds!",
    
    "This restaurant is a decent option if you're looking for a quick bite. The service was prompt, and the menu had a variety of options. The prices were reasonable, but don't expect anything extraordinary. It's a convenient choice for a casual meal.",
    
    "From the moment we walked in, the staff made us feel welcome. The chef's recommendations were spot-on, and each dish was a culinary delight. The attention to detail and unique flavors set this restaurant apart. We left with happy taste buds!",
    
    "I can't understand the hype around this place. The prices are exorbitant for the quality of food served. I ordered a dish that was supposed to be a specialty, but it was bland and lacked the promised flavors. Also the bathrooms were very dirty.Definitely not worth the money.",
    
    "The restaurant had a nice ambiance, and the service was courteous. The food, however, was average. Nothing stood out, but nothing was terrible either. If you're in the neighborhood and need a meal, it's an okay choice, but I wouldn't go out of my way to dine here.",
    
    "I'm thrilled to have discovered this hidden gem! The staff was friendly, the menu had a great selection, and the food was absolutely delicious. The prices were reasonable, making it a fantastic value for the quality of the dining experience. Can't wait to come back!"
]
'''
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

# docs is a list of spaCy docs, each representing a restaurant review
def detectRestaurantTopics(docs):
  food = ["food|NOUN", "pizza|NOUN", "meal|NOUN", "taco|NOUN", "chinese|ADJ", "mexican|ADJ", "sushi|NOUN", "bone|NOUN", "drink|NOUN", "pho|NOUN", "curry|NOUN", "coffee|NOUN", "teriyaki|NOUN"]
  food_hits = []
  for i, doc in enumerate(docs):
    for j, sentence in enumerate(doc.sents):
      if topicDetection(sentence, food, ["NOUN", "ADJ"], 0.6):
        # if food detected in sentence, record doc index and sentence index
        food_hits.append([i,j])
  
  service = ["waiter|NOUN", "staff|NOUN", "service|NOUN", "employee|NOUN"]
  service_hits = []
  for i, doc in enumerate(docs):
    for j, sentence in enumerate(doc.sents):
      if topicDetection(sentence, service, ["NOUN", "ADJ"], 0.7, ["restaurant", "restraunt", "restaraunt"]):
        # if service detected in sentence
        service_hits.append([i,j])

  location = ["crowded|ADJ", "atmosphere|NOUN", "quiet|ADJ", "interior|NOUN", "music|NOUN", "environment|NOUN", "space|NOUN", "vibe|NOUN", "location|NOUN"]
  location_hits = []
  for i, doc in enumerate(docs):
    for j, sentence in enumerate(doc.sents):
      if topicDetection(sentence, location, ["NOUN", "ADJ"], 0.67):
        # if location detected in sentence
        location_hits.append([i,j])

  clean = ["clean|ADJ", "dirty|ADJ", "fly|NOUN", "cockroach|NOUN", "filthy|ADJ", "spotless|ADJ"]
  clean_hits = []
  for i, doc in enumerate(docs):
    for j, sentence in enumerate(doc.sents):
      if topicDetection(sentence, clean, ["NOUN", "ADJ"], 0.7):
        # if cleanliness detected in sentence
        clean_hits.append([i,j])
  
  price = ["cheap|ADJ", "expensive|ADJ", "price|NOUN", "worth|NOUN", "payment|NOUN", "tip|NOUN"]
  price_hits = []
  for i, doc in enumerate(docs):
    for j, sentence in enumerate(doc.sents):
      # exclude verbs like "pay" or "buy"
      if topicDetection(sentence, price, ["NOUN", "ADJ"], 0.7):
        # if price detected in sentence
        price_hits.append([i,j])
  
  return [food_hits, service_hits, location_hits, clean_hits, price_hits]