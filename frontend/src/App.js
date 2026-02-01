import './App.css';
import { useState, useEffect } from 'react';
import { Link } from "react-router-dom";
function App() {
  const [data, setData] = useState("");
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [items, setItems] = useState([]);

  useEffect(() => {
    console.log("useEffect called");
    const func = async () => {
      const res = await fetch(`${process.env.REACT_APP_BACKEND_SERVER}/items`, {
        'method': 'GET',
        headers: {
          "ngrok-skip-browser-warning": "true",
        },
      })
      console.log("Fetch completed");
      const json = await res.json();
      setItems(json.items);
      console.log("Items updated:", json.items);
    };
    func();
  }, [loading]);

  const save = async () => {
    setLoading(true);
    const res = await fetch(`${process.env.REACT_APP_BACKEND_SERVER}/ingest`, {
      'method': 'POST',
      'headers': {
        'Content-Type': 'application/json'
      },
      'body': JSON.stringify(
        url
          ? { 'url': data }
          : { 'text': data }
      )
    });
    const json = await res.json();
    console.log(json);
    setLoading(false);
  };

  return (
    <div className="App">
      <nav style={{ marginBottom: "20px" }}>
        <Link to="/">Home</Link> |{" "}
        <Link to="/prompt">Prompt</Link>
      </nav>
      <h1>AI Knowledge Inbox</h1>
      <p>Welcome to the AI Knowledge Inbox application!</p>

      <div>
        {loading ? (<h1>Loading...</h1>) : (
          <div>
            <h1>Save your context</h1>
            <div>
              <button onClick={() => { setData(""); setUrl(false) }}>Text</button>
              <button onClick={() => { setData(""); setUrl(true) }}>Url</button>
            </div>
            {url ? (<input
              type="text"
              placeholder="Enter the URL"
              value={data}
              onChange={(e) => setData(e.target.value)}
            />)
              :
              (<textarea
                placeholder="Enter your data here"
                value={data}
                onChange={(e) => setData(e.target.value)}
                rows={10}
                cols={50}
              />)
            }
            <br />
            <button onClick={save}>Save Data</button>

            <div>
              <h2>Saved Items:</h2>
              {items.length === 0 ? (
                <p>No items saved yet.</p>
              ) : (
                <ol>
                  {items.map((item, index) => (
                    <li key={index}>
                      <p>{item.data} - Added on{" "}
                        {new Date(item.added_at).toLocaleString()}</p>
                    </li>
                  ))}
                </ol>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
