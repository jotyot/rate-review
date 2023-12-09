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
If the wget takes too long to run click that github link and download it in your browser, into the ecs-171-final-project folder