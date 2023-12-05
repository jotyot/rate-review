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
            <form method="post" action="/submit" enctype="multipart/form-data">
                <input type="file" name="review_file" accept=".json">
                <input type="submit" value="Submit">
                <button formaction="/">Back to Method Selection</button>
            </form>
        '''
    elif method == 'text':
        return '''
            <h1>Business Success Prediction with Sentiment Analysis</h1>
            <form method="post" action="/submit">
                <textarea name="reviews" placeholder="Enter reviews here"></textarea>
                <input type="submit" value="Submit">
                <button formaction="/">Back to Method Selection</button>
            </form>
        '''

@app.route('/submit', methods=['POST'])
def submit():
    result = ""
    if 'review_file' in request.files:
        file = request.files['review_file']
        if file.filename != '':
            # Process file data here
            result = "File processed. (Replace with actual model output)"
    else:
        # Assume each review is separated by a newline character
        reviews = request.form['reviews']
        
        # Process text reviews here
        docs = process_text.toDocs(reviews.split("\n"))
        sd = process_text.SentimentDetector(docs)
        input = sd.weighted_input()
        sentiments = sd.sentiment_count()
        
        # Prediction here
        linear = predict.LinearModel()
        prediction = linear.predict(input)
        weights = linear.parameters()
    
    return f'''
        <h1>Predicted Score</h1>
        <p>{prediction}</p>
        <h1>Detected Sentiments</h1>
        <p>{sentiments}</p>
        <h1>Model Weights</h1>
        <p>{weights}</p>
        <form action="/">
            <input type="submit" value="Submit Something New">
        </form>
        <h2>Inputed Text</h2>
        <p>{reviews}</p>
    '''

if __name__ == '__main__':
    app.run(debug=True)
