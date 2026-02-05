import { useState } from "react";
function App() {
  const [question,setquestion]=useState("");
  const[answer,setanswer]=useState("");
  const[loading,setloading]=useState(false);

  console.log("Ask button clicked");

  const askquestion=async()=>{
    setloading(true);

    const response=await fetch("http://127.0.0.1:8000/ask",{
      method:"POST",
      headers:{
        "Content-Type":"application/json"
      },
      body:JSON.stringify({question}),
    });
    const data=await response.json();
    setanswer(data.answer);
    setloading(false);
  };


  return (
    <div style={{padding:"2rem",maxWidth:"800px",margin:"auto"}}>
      <h1 style={{textAlign:"center"}}>GATE Exam Bot</h1>

      <textarea
        rows="4"
        placeholder="Ask a gate question"
        value={question}
        onChange={(e)=>setquestion(e.target.value)}
        style={{width:"100%"}}
        />

        <br /><br />

        <button onClick={askquestion} disabled={loading}>
        {loading ? "Thinking..." : "Ask"}
      </button>

      <pre style={{ marginTop: "1rem", whiteSpace: "pre-wrap" }}>
        {answer}
      </pre>
    </div>
  );
}

export default App;
