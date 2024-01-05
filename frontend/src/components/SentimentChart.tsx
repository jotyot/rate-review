interface Props {
  totalSent: number[];
  weightedSent: number[];
  sentHighlights: number[];
}

const sentimentLabel = [
  "+food",
  "+service",
  "+location",
  "+clean",
  "+price",
  "-food",
  "-service",
  "-location",
  "-clean",
  "-price",
];

function SentimentChart({ totalSent, weightedSent, sentHighlights }: Props) {
  return (
    <div className="grid grid-cols-3 grow">
      <div className="grid grid-rows-11 border-r">
        <div className="font-medium text-center border-b bg-stone-700">
          Sentiment
        </div>
        {sentimentLabel.map((label, i) => (
          <div
            className={`text-center ${sentHighlights[i] && "bg-stone-600"}`}
            key={i}
          >
            {label}
          </div>
        ))}
      </div>
      <div className="grid grid-rows-11 border-r">
        <div className="font-medium text-center border-b bg-stone-700">
          Total Count
        </div>
        {totalSent.map((label, i) => (
          <div className="text-center" key={i}>
            {label}
          </div>
        ))}
      </div>
      <div className="grid grid-rows-11">
        <div className="font-medium text-center border-b bg-stone-700">
          Weighted Count
        </div>
        {weightedSent.map((label, i) => (
          <div className="text-center" key={i}>
            {label}
          </div>
        ))}
      </div>
    </div>
  );
}

export default SentimentChart;
