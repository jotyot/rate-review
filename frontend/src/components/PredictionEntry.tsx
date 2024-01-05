interface Props {
  name: string;
  prediction: number;
}

function PredictionEntry({ name, prediction }: Props) {
  return (
    <div className="border-b h-32 p-1 flex flex-col">
      <div className="flex-grow font-medium text-lg">{name}</div>
      <div className=" text-3xl font-medium ">{prediction}</div>
    </div>
  );
}

export default PredictionEntry;
