from flask import Flask, request, render_template_string, render_template
import process_text
import predict
import pandas as pd
import spacy
from spacy import Language
from sense2vec import Sense2Vec

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <h1>Business Success Prediction with Sentiment Analysis</h1>
        <form action="/select-method" method="get">
            <button type="submit" name="method" value="file">File Submission</button>
            <button type="submit" name="method" value="text">Text Submission</button>
        </form>
    '''

@app.route('/select-method')
def select_method():
    method = request.args.get('method')
    if method == 'file':
        return '''
            <h1>Business Success Prediction with Sentiment Analysis</h1>
            <p>Reviews are separated by newlines</p>
            <form method="post" action="/submit" enctype="multipart/form-data">
                <input type="file" name="review_file" accept=".txt">
                <input type="submit" value="Submit">
            </form>
            <form action="/">
                <button>Back to Method Selection</button>
            </form>
        '''
    elif method == 'text':
        return '''
            <h1>Business Success Prediction with Sentiment Analysis</h1>
            <p>Reviews are separated by newlines</p>
            <form method="post" action="/submit">
                <textarea name="reviews" placeholder="Enter reviews here" rows="20" cols="80"></textarea><br>
                <input type="submit" value="Submit">
            </form>
            <form action="/">
                <button>Back to Method Selection</button>
            </form>
        '''

@app.route('/submit', methods=['POST'])
def submit():
    if 'review_file' in request.files:
        file = request.files['review_file']
        if file.filename != '':
            reviews = file.read().decode('utf-8')
        else:
            reviews = ""
    else:
        # Assume each review is separated by a newline character
        reviews = request.form['reviews']

    # Process text reviews here
    docs = process_text.toDocs(reviews.split("\n"))
    sd = process_text.SentimentDetector(docs)
    w_input = sd.weighted_input()
    sentiments = sd.sentiment_count()
    
    # Prediction here
    linear = predict.LinearModel()
    prediction = round(linear.predict(w_input), 2)
    weights = linear.parameters()

    # Total Sents
    NNt = predict.TotalSentNN()
    n_prediction = round(NNt.predict(sd.raw_count), 2)   
    
    # Weighted Sents
    NNw = predict.WeightedNN()
    w_prediction = round(NNw.predict(w_input), 2)
    
    return f'''
        <h1>Predicted Score</h1>
        <h3>Linear: {prediction}</h3>
        <h3>Neural Network (total): {n_prediction}</h3>
        <h3>Neural Network (weighted): {w_prediction}</h3>
        <h1>Detected Sentiments</h1>
        <p>{sentiments}</p>
        <h3>Weighted</h3>
        <p>{w_input}</p>
        <h2>Linear Model Weights</h2>
        <p>{weights}</p>
        <form action="/">
            <input type="submit" value="Submit Something New">
        </form>
        <h2>Inputted Text</h2>
        <p>{reviews}</p>
    '''

if __name__ == '__main__':
    app.run(debug=True)
