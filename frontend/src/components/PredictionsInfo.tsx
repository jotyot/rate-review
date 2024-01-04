import PredictionEntry from "./PredictionEntry";
import { PredictionData } from "../types/PredictionData";

interface Props {
  data: PredictionData;
}

function PredictionsInfo({ data }: Props) {
  const { linPred, nnwPred, nntPred } = data;

  return (
    <div className="flex flex-col w-[400px] text-white rounded-r-lg border-t border-r border-b pt-3 bg-stone-700">
      <div className="flex justify-center items-center pb-3">
        <div className="text-xl text-center font-medium">Predictions</div>
      </div>
      <div className=" h-[700px] w-full bg-stone-800 rounded-br-lg">
        <PredictionEntry name="Linear" prediction={linPred} />
        <PredictionEntry
          name="Neural Network (Weighted)"
          prediction={nnwPred}
        />
        <PredictionEntry name="Neural Network (Total)" prediction={nntPred} />
      </div>
    </div>
  );
}

export default PredictionsInfo;
