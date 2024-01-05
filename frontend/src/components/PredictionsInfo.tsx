import PredictionEntry from "./PredictionEntry";
import { PredictionData } from "../types/PredictionData";
import SentimentChart from "./SentimentChart";

interface Props {
  data: PredictionData;
  isFetching: boolean;
}

function PredictionsInfo({ data, isFetching }: Props) {
  const { linPred, nnwPred, nntPred, totalSent, weightedSent, numReviews } =
    data;

  return (
    <div
      className={`flex flex-col w-[400px] text-white rounded-r-lg border-t border-r border-b pt-3 ${
        isFetching ? "bg-stone-600" : "bg-stone-700"
      }`}
    >
      <div className="flex justify-center items-center pb-3">
        <div className="text-xl text-center font-medium">Predictions</div>
      </div>
      <div
        className={`h-[700px] w-full flex flex-col ${
          isFetching ? "bg-stone-700" : "bg-stone-800"
        } rounded-br-lg`}
      >
        <PredictionEntry name="Linear" prediction={linPred} />
        <PredictionEntry
          name="Neural Network (Weighted)"
          prediction={nnwPred}
        />
        <PredictionEntry name="Neural Network (Total)" prediction={nntPred} />
        <div className="border-b p-1 text-center bg-stone-700">{`Number of Reviews: ${numReviews}`}</div>
        <SentimentChart totalSent={totalSent} weightedSent={weightedSent} />
      </div>
    </div>
  );
}

export default PredictionsInfo;
