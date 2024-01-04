from flask import Flask, request, jsonify
from flask_cors import CORS
import process_text
import predict

app = Flask(__name__)
CORS(app)


@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.json  # Use request.form if you are sending form data
        reviews = data["reviews"]

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

        response_data = {
            "linear_prediction": prediction,
            "nn_total_prediction": n_prediction,
            "nn_weighted_prediction": w_prediction,
            "sentiments": sentiments,
            "weighted_input": w_input,
            "linear_weights": weights,
            "inputted_text": reviews,
            "num_reviws": sd.num_reviews,
        }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
