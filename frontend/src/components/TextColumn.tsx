import React from "react";
import { useState, ChangeEvent } from "react";

interface Props {
  text: string;
  setText: (text: string) => void;
  handleSubmit: () => void;
  isFetching: boolean;
}

function TextColumn({ text, setText, handleSubmit, isFetching }: Props) {
  const [isEditing, setIsEditing] = useState(false);

  const handleInputChange = (event: ChangeEvent<HTMLTextAreaElement>) => {
    const { value } = event.target;
    setText(value);
  };

  const handleEdit = () => {
    if (isFetching) return;

    if (isEditing) handleSubmit();

    setIsEditing(!isEditing);
  };

  return (
    <div
      className={`flex flex-col w-[400px] text-white rounded-l-lg border pt-3 ${
        isFetching ? "bg-stone-600" : "bg-stone-700"
      }`}
    >
      <div className="flex justify-center items-center pb-3">
        <div className="text-xl text-center font-medium">Review Text</div>
        <button
          onClick={handleEdit}
          className={`w-20 h-10 border rounded-lg ml-2 hover:bg-stone-600 absolute translate-x-36`}
        >
          {isEditing ? "Submit" : "Edit"}
        </button>
      </div>

      <div
        className={` h-[700px] w-full ${
          isFetching ? "bg-stone-700" : "bg-stone-800"
        } rounded-bl-lg ${isEditing ? "overflow-hidden" : "overflow-auto"}`}
      >
        {isEditing ? (
          <textarea
            value={text}
            onChange={handleInputChange}
            placeholder="Enter reviews here"
            className="w-full resize-none focus:outline-none h-full p-4 bg-inherit"
          />
        ) : (
          <div className="h-full whitespace-pre-line p-4 ">
            {text.split("\n").map((line, index) => (
              <React.Fragment key={index}>
                {line}
                <br />
              </React.Fragment>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default TextColumn;
