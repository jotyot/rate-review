# ECS 171 Final Project: Predicting Restaurant Ratings with Sentiment Analysis

## Authors
- Nicholas Martinez
- Olivia Shen
- Jonathan Tran

## Project Overview
The goal of this project was to create a tool for predicting restaurant ratings given a review input, as well as to determine what kind of sentiments are most important for predicting the success of a restaurant.

## Installation
To install the required libraries, please run:
```
pip install -r requirements.txt
```

To install the model needed to extract the key topics from the reviews, run:
```
wget https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz
tar -xvzf s2v_reddit_2015_md.tar.gz
rm s2v_reddit_2015_md.tar.gz
rm ._s2v_old
```
Note: The downloaded tar file is 573 MB so it may take a while. 
If the wget takes too long to run click that github link and download it in your browser, into the ecs-171-final-project folder.
Then run the other 3 lines (after the wget) above.

## Folders
### inital-data-cleaning
These files converted the large file containing the reviews of every business in california to the reviews of every restaurant in Sacramento and Yolo county. It is not very important to run.

The files do require a download of the large file because it is too big to upload to github https://datarepo.eng.ucsd.edu/mcauley_group/gdrive/googlelocal/#subsets <br>
California -> both reviews and metadata

### model-testing
These files train, evaulate, and save the models to be used on the website. This is the most related to our ECS 171 course.
- `linear_model.ipynb`
  - based on weighted sentiments
  - generates` linear.pt`
- `neural_model.ipynb`
  - based on weighted sentiments
  - generates `nn_model.pt`
- `poly_model.ipynb`
  - we ended up not using this one and the file takes 1 hour to run so its not important
- `total_sent_neural_model.ipynb`
  - based on the total sentiment counts 
  - generates `nn4_40.pt`

### models
The saved pytorch models to be loaded for the website

### processed_data
Contains files that are used to train the model.
The json files are the training data. The csv files are for initial data cleaning and aren't very important.

### topics-sentiments
This is the code that ends up generating the files that contain the features used in the models.
- `eda.ipynb`
  - mostly graphs and tables of the data thats generated
- `sentiment_analysis.ipynb`
  - runs a sentiment analysis model on every review and assigns positive or negative food/service/location/clean/price to every sentence in the review.
  - it then appends these reviews to their corresponding restaurants
  - this code takes up to 24 hours so probably don't run this
- `topic-detection.ipynb `
  - uses a model to assign a list of topics to every sentence (food/service/location/clean/price)
- `topic-sentiment.ipynb`
  - generates the final files to be used in the models
  - each row represents a business
  - the columns represent the types/counts of sentiments the business has
  - generates `restaurant-topic-sentiment.json` and `restaurant-topic-sentiment2.json`

### website
Has the code needed to run the website

To run:
```
cd ./website
flask --app app.py run
```

- `app.py`
  - contains the actual flask backend
- `predict.py`
  - a file that contains classes to help abstract the models and their methods
- `process_text.py`
  - this is code that requires installation of the topic detection models. This code will also download a sentiment analysis model.