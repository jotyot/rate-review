from flask import Flask, request, render_template_string

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
        reviews = request.form['reviews']
        # Process text reviews here
        result = "Text processed. (Replace with actual model output)"
    
    return f'''
        <h1>Results</h1>
        <p>{result}</p>
        <form action="/">
            <input type="submit" value="Submit Something New">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
