import { useState } from "react";
import {
  PredictionData,
  sampleSentMatrix,
  sampleText,
} from "./types/PredictionData";
import TextColumn from "./components/TextColumn";
import PredictionsInfo from "./components/PredictionsInfo";
import axios from "axios";

function App() {
  const [text, setText] = useState(sampleText);
  const [isFetching, setIsFetching] = useState(false);
  const [sentHighlights, setSentHighlights] = useState([
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  ]);
  const [data, setData] = useState<PredictionData>({
    linPred: 4.6,
    nnwPred: 4.45,
    nntPred: 4.38,
    totalSent: [25, 3, 4, 0, 4, 4, 1, 1, 0, 1],
    weightedSent: [
      1.786, 0.214, 0.286, 0, 0.286, 0.286, 0.071, 0.071, 0, 0.071,
    ],
    numReviews: 14,
    sentMatrix: sampleSentMatrix,
  });

  const handleSubmit = async () => {
    try {
      setIsFetching(true);
      const response = await axios.post("http://127.0.0.1:5000/submit", {
        reviews: text,
      });

      setIsFetching(false);
      setData(response.data);

      console.log(response.data); // Handle the response as needed
    } catch (error) {
      console.error("Error submitting form:", error);
      setIsFetching(false);
    }
  };

  return (
    <div className="bg-stone-900 h-screen flex items-center justify-center">
      <TextColumn
        text={text}
        setText={setText}
        handleSubmit={handleSubmit}
        isFetching={isFetching}
        handleMouseOut={() => setSentHighlights([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])}
        handleMouseOver={(index: number) =>
          setSentHighlights(data.sentMatrix[index])
        }
      />
      <PredictionsInfo
        data={data}
        isFetching={isFetching}
        sentHighlights={sentHighlights}
      />
    </div>
  );
}

export default App;
