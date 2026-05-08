import { useState } from "react";
import axios from "axios";

function App() {

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const askQuestion = async () => {

    const response = await axios.post(
      "http://localhost:8000/chat",
      null,
      {
        params: {
          question: question
        }
      }
    );

    setAnswer(response.data.answer);
  };

  return (
    <div>

      <h1>AI Chatbot</h1>

      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={askQuestion}>
        Ask AI
      </button>

      <p>{answer}</p>

    </div>
  );
}

export default App;