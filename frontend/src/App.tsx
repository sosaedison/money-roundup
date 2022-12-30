import { useState, useCallback, useEffect } from 'react'
import './App.css'

import {
  usePlaidLink,
  PlaidLinkOptions,
  PlaidLinkOnSuccess,
  PlaidLinkOnSuccessMetadata,
} from 'react-plaid-link';


function App() {
  const [token, setToken] = useState(null);
  // const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  const createLinkToken = useCallback(async () => {
    const response = await fetch("http://127.0.0.1:8000/link/token/create", {});
    const data = await response.json();
    console.log(data)
    console.log(data.link_token)
    setToken(data.link_token);
    localStorage.setItem("link_token", data.link_token);
  }, [setToken])

  const onSuccess: PlaidLinkOnSuccess = useCallback(async (publicToken: string, metadata: PlaidLinkOnSuccessMetadata) => {
    setLoading(true)
    await fetch("http://127.0.0.1:8000/exchange/public/token", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ public_token: publicToken, metadata: metadata }),
    });
  }, [])

  const onExit = useCallback(async () => {}, [])

  const config: PlaidLinkOptions = {
    onSuccess,
    onExit,
    token
  }

  const {open, ready, exit, error} = usePlaidLink(config)

  useEffect(() => {
    if(token == null) {
      createLinkToken()
    }
    console.log(ready)
    if (ready) {
      open();
    }
  })

  return (
    <div className="App">
      <button onClick={() => open()
        } disabled={!ready}>
        <strong>Link account</strong>
      </button>
     
    </div>
  )
}

export default App
