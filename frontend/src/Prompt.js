import './App.css';
import { useState } from 'react';
import { Link } from 'react-router-dom';
function Prompt() {
    const [data, setData] = useState("");
    const [response, setResponse] = useState("");
    const [loading, setLoading] = useState(false);

    const getResponse = async () => {
        setLoading(true);
        const res = await fetch(`${process.env.REACT_APP_BACKEND_SERVER}/query`, {
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'prompt': data })
        });
        const json = await res.json();
        if(!res.ok){
            alert("Error fetching response");
            console.log(json);
            setLoading(false);
            return;
        }
        setResponse(json.answer);
        setLoading(false);
    }

    return (
        <div className="App">
            <nav style={{ marginBottom: "20px" }}>
                <Link to="/">Home</Link> |{" "}
                <Link to="/prompt">Prompt</Link>
            </nav>
            <h1>AI Knowledge Inbox</h1>
            <p>Welcome to the AI Knowledge Inbox application!</p>

            <div>
                <h1>Enter your prompt Here</h1>
                <textarea
                    placeholder="Enter your Prompt here"
                    value={data}
                    onChange={(e) => setData(e.target.value)}
                    disabled={loading}
                    rows={10}
                    cols={50}
                />
                <br />
                {response !== "" && <textarea
                    placeholder="Enter your data here"
                    value={response}
                    disabled={true}
                    rows={10}
                    cols={50}
                />}
                <br />
                <button type='submit' onClick={getResponse} disabled={loading}>Submit</button>
                <button type='button' onClick={() => {setData(""); setResponse("")}} disabled={loading}>Clear</button>
            </div>
        </div>
    )
};

export default Prompt;
