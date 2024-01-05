import { useState, ChangeEvent } from "react";

interface Props {
  text: string;
  setText: (text: string) => void;
  handleSubmit: () => void;
  isFetching: boolean;
  handleMouseOver: (index: number) => void;
  handleMouseOut: () => void;
}

function TextColumn({
  text,
  setText,
  handleSubmit,
  isFetching,
  handleMouseOut,
  handleMouseOver,
}: Props) {
  const [isEditing, setIsEditing] = useState(false);
  const [onSent, setOnSent] = useState(-1);

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
            {text
              .replace(/!/g, ".")
              .replace("...", ".")
              .replace(/([^\n.])(\n|$)/g, "$1.$2")
              .split(".")
              .map((line, index) => (
                <span
                  className={`${index == onSent && "bg-stone-600"}`}
                  onMouseOut={() => {
                    handleMouseOut();
                    setOnSent(-1);
                  }}
                  onMouseOver={() => {
                    handleMouseOver(index);
                    setOnSent(index);
                  }}
                  key={index}
                >
                  {line.length > 0 ? line + "." : line}
                </span>
              ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default TextColumn;
