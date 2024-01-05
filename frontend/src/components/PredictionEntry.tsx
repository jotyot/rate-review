import { useState, ReactNode } from "react";

interface Props {
  name: string;
  prediction: number;
  children?: ReactNode;
}

function PredictionEntry({ name, prediction, children }: Props) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <div className="border-b h-32 p-1 flex flex-col relative">
        <div className="font-medium text-lg text-center grow">{name}</div>
        <div className="font-medium text-7xl text-center p-1">{prediction}</div>
        <div className="flex items-center justify-center absolute right-0 top-0 p-1">
          <button
            className="rounded-full bg-stone-500 hover:bg-stone-400 px-[11px]"
            onClick={() => setIsOpen(true)}
          >
            <div className="text-white text-lg font-bold">i</div>
          </button>
        </div>
      </div>
      {isOpen && (
        <div className="fixed inset-0 bg-stone-800 bg-opacity-50 items-center justify-center z-10 flex">
          <div className="bg-stone-800 rounded shadow-md w-96 border flex flex-col">
            <div className="bg-stone-700 border-b h-12 rounded-t font-medium text-2xl flex items-center justify-center">
              {name}
            </div>
            <div className="flex flex-col w-full h-full items-center">
              <div className="grow p-3">{children}</div>
              <button
                className="rounded w-20 text-center border mb-3 p-1 bg-stone-700 font-medium"
                onClick={() => setIsOpen(false)}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default PredictionEntry;
