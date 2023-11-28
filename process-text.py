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
# Sanity check to make sure we have the right pipeline order
print(nlp.pipe_names)

## DUMMY REVIEWS
reviews = [
    "I stumbled upon this hidden gem last night and had the most amazing dining experience. The atmosphere was cozy, the staff was friendly, and the food was a culinary masterpiece. I highly recommend the chef's special – a true delight for your taste buds!",
    
    "This restaurant is a decent option if you're looking for a quick bite. The service was prompt, and the menu had a variety of options. The prices were reasonable, but don't expect anything extraordinary. It's a convenient choice for a casual meal.",
    
    "From the moment we walked in, the staff made us feel welcome. The chef's recommendations were spot-on, and each dish was a culinary delight. The attention to detail and unique flavors set this restaurant apart. We left with happy taste buds!",
    
    "I can't understand the hype around this place. The prices are exorbitant for the quality of food served. I ordered a dish that was supposed to be a specialty, but it was bland and lacked the promised flavors. Also the bathrooms were very dirty.Definitely not worth the money.",
    
    "The restaurant had a nice ambiance, and the service was courteous. The food, however, was average. Nothing stood out, but nothing was terrible either. If you're in the neighborhood and need a meal, it's an okay choice, but I wouldn't go out of my way to dine here.",
    
    "I'm thrilled to have discovered this hidden gem! The staff was friendly, the menu had a great selection, and the food was absolutely delicious. The prices were reasonable, making it a fantastic value for the quality of the dining experience. Can't wait to come back!"
]

docs = list(nlp.pipe(reviews))

# Detect if a topic defined by topic_list is present in a sentence (span from spaCy doc)
def topicDetection(sentence, topic_list : list[str], pos : list[str], thresh) -> list[int]:
    indices = []
    for i, token in enumerate(sentence):
      # Construct string to pass to Sense2Vec
      s = token.lemma_ + "|" + token.pos_
      # Only consider tokens that Sense2Vec model knows and are from specified part of speech
      if (s in s2v and token.pos_ in pos) and (s2v.similarity(s, topic_list) > thresh):
        indices.append(i)
    # return a list of indices where topic was detected
    return indices

# Operates like TopicDetection, except looks or matches to each string in topics_list seperately
# Instead of averaging their vector representations
def seperateTopicsDetection(sentence, topics_list : list[str], thresh, exclude_pos = []) -> list[int]:
    indices = []
    for i, token in enumerate(sentence):
      # Skip token if explicitly told to ignore part of speech
      if token.pos_ in exclude_pos:
        continue
      # Construct string to pass to Sense2Vec
      s = token.lemma_ + "|" + token.pos_
      # Only consider tokens that Sense2Vec model knows
      if s in s2v:
        # Add to indices list if token matches at least one topic from topic_list
        for topic in topics_list:
          if s2v.similarity(s, topics_list) > thresh:
            indices.append(i)
            break
    return indices

# docs is a list of spaCy docs, each representing a restaurant review
def detectRestaurantTopics(docs):
  food = ["food|NOUN", "pizza|NOUN", "meal|NOUN", "taco|NOUN", "chinese|ADJ", "mexican|ADJ", "sushi|NOUN", "bone|NOUN", "drink|NOUN", "pho|NOUN", "curry|NOUN", "coffee|NOUN", "teriyaki|NOUN"]
  food_hits = []
  for i, doc in enumerate(docs):
    for j, sentence in enumerate(doc.sents):
      for k in topicDetection(sentence, food, ["NOUN", "ADJ"], 0.6):
        # for each token where the food topic is detected
        # record lemma, doc index, sentence index, and token index
        food_hits.append([i,j])
  
  service = ["waiter|NOUN", "staff|NOUN", "service|NOUN", "employee|NOUN"]
  service_hits = []
  for i, doc in enumerate(docs):
    for j, sentence in enumerate(doc.sents):
      for k in topicDetection(sentence, service, ["NOUN", "ADJ"], 0.7):
        # for each token where the food topic is detected
        # record lemma, doc index, sentence index, and token index
        service_hits.append([i,j])

  location = ["crowded|ADJ", "atmosphere|NOUN", "quiet|ADJ", "interior|NOUN", "music|NOUN", "environment|NOUN", "space|NOUN", "vibe|NOUN", "location|NOUN"]
  location_hits = []
  for i, doc in enumerate(docs):
    for j, sentence in enumerate(doc.sents):
      for k in seperateTopicsDetection(sentence, location, 0.67):
        # for each token where the food topic is detected
        # record lemma, doc index, sentence index, and token index
        location_hits.append([i,j])

  clean = ["clean|ADJ", "dirty|ADJ", "fly|NOUN", "cockroach|NOUN", "filthy|ADJ", "spotless|ADJ"]
  clean_hits = []
  for i, doc in enumerate(docs):
    for j, sentence in enumerate(doc.sents):
      for k in seperateTopicsDetection(sentence, clean, 0.7):
        # for each token where the food topic is detected
        # record lemma, doc index, sentence index, and token index
        clean_hits.append([i,j])
  
  price = ["cheap|ADJ", "expensive|ADJ", "price|NOUN", "worth|NOUN", "payment|NOUN", "tip|NOUN"]
  price_hits = []
  for i, doc in enumerate(docs):
    for j, sentence in enumerate(doc.sents):
      # exclude verbs like "pay" or "buy"
      for k in seperateTopicsDetection(sentence, price, 0.7, ["VERB"]):
        # for each token where the food topic is detected
        # record lemma, doc index, sentence index, and token index
        price_hits.append([i,j])
  
  return [food_hits, service_hits, location_hits, clean_hits, price_hits]

# List of 5 lists. Each list represents a topic. Each topic list has 2-element lists representing hits.
# First element is doc index, second is sentence index.
topics = detectRestaurantTopics(docs)
for t in topics:
  print(t)