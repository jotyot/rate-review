from flask import Flask, make_response, request, jsonify

from flask_cors import CORS

# import process_text
# import predict
import torch

app = Flask(__name__)
CORS(app)


test = {
    "linPred": 0,
    "nntPred": 0,
    "nnwPred": 0,
    "totalSent": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "weightedSent": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "numReviews": 0,
    "sentMatrix": [],
    "sentences": [],
}


@app.route("/", methods=["POST"])
def main():
    try:
        # data = request.json  # Use request.form if you are sending form data
        # reviews = data["reviews"]

        # # Process text reviews here
        # docs = process_text.toDocs(reviews.split("\n"))
        # sd = process_text.SentimentDetector(docs)
        # w_input = sd.weighted_input()
        # sentiments = sd.sentiment_count()

        # # Prediction here
        # linear = predict.LinearModel()
        # prediction = round(linear.predict(w_input), 2)

        # # Total Sents
        # NNt = predict.TotalSentNN()
        # n_prediction = round(NNt.predict(sd.raw_count), 2)

        # # Weighted Sents
        # NNw = predict.WeightedNN()
        # w_prediction = round(NNw.predict(w_input), 2)

        # response_data = {
        #     "linPred": prediction,
        #     "nntPred": n_prediction,
        #     "nnwPred": w_prediction,
        #     "totalSent": sentiments,
        #     "weightedSent": w_input,
        #     "numReviews": sd.num_reviews,
        #     "sentMatrix": sd.sentiment_matrix,
        #     "sentences": sd.sentences,
        # }

        # return jsonify(response_data)
        return jsonify(test)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
