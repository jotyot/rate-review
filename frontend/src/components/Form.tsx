import { useState, ChangeEvent, FormEvent } from "react";
import axios from "axios";

interface FormData {
  reviews: string;
}

function Form() {
  const [formData, setFormData] = useState<FormData>({
    reviews: "",
  });

  const handleInputChange = (event: ChangeEvent<HTMLTextAreaElement>) => {
    const { value } = event.target;
    setFormData({
      reviews: value,
    });
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    console.log("submitted");

    try {
      const response = await axios.post("http://127.0.0.1:5000/submit", {
        reviews: formData.reviews,
      });

      console.log(response.data); // Handle the response as needed
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Reviews:
        <textarea
          name="reviews"
          value={formData.reviews}
          onChange={handleInputChange}
          placeholder="Enter reviews here"
          rows={5}
          cols={50}
        />
      </label>
      <button type="submit">Submit</button>
    </form>
  );
}

export default Form;
