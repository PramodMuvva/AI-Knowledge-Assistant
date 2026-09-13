import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [uploadStatus, setUploadStatus] = useState("");
const [sources, setSources] = useState([]);
const [askStatus, setAskStatus] = useState("");


  const uploadFile = async () => {
    if (!file) return;

    const formData = new FormData();

    formData.append("file", file);

    setUploadStatus("Uploading...");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      setUploadStatus(
        `Uploaded successfully! ${data.pages} pages, ${data.chunks} chunks.`
      );

    } catch (error) {
      setUploadStatus(`Error: ${error.message}`);
    }
  };


const askQuestion = async () => {
  if (!question.trim()) return;

  setAskStatus("Thinking...");
  setAnswer("");
  setSources([]);

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/ask",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Failed to get answer");
    }

    setAnswer(data.answer);
    setSources(data.sources);
    setAskStatus("");

  } catch (error) {
    setAskStatus(`Error: ${error.message}`);
  }
};

  return (
    <div className="app">
      <header>
        <h1>AI Knowledge Assistant</h1>
        <p>Upload a document and ask questions about it.</p>
      </header>

      <main>
        <section className="upload-section">
          <h2>Upload Document</h2>

          <input
            type="file"
            accept=".pdf"
            onChange={(event) => setFile(event.target.files[0])}
          />

          {file && (
            <p className="file-name">
              Selected: {file.name}
            </p>
          )}

          <button disabled={!file} onClick={uploadFile}>
            Upload PDF
          </button>

          {uploadStatus && (
  <p className="upload-status">
    {uploadStatus}
  </p>
)}
        </section>

        <section className="question-section">
          <h2>Ask a Question</h2>

          <textarea
            placeholder="Ask something about your document..."
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
          />

          <button disabled={!question.trim()} onClick={askQuestion}>
            Ask
          </button>
        </section>

        {askStatus && (
  <p className="ask-status">
    {askStatus}
  </p>
)}

{answer && (
  <section className="answer-section">
    <h2>Answer</h2>

    <p>{answer}</p>

    {sources.length > 0 && (
      <div className="sources">
        <h3>Sources</h3>

        {sources.map((source, index) => (
          <p key={index}>
            📄 {source.source} — Page {source.page}
          </p>
        ))}
      </div>
    )}
  </section>
)}
        
      </main>
    </div>
  );
}

export default App;