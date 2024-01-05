interface PredictionData {
  linPred: number;
  nnwPred: number;
  nntPred: number;
  totalSent: number[];
  weightedSent: number[];
  numReviews: number;
}

export type { PredictionData };
