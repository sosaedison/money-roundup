import { useState, useCallback, useEffect } from 'react'
import './App.css'

import PlaidLink from "./PlaidLink"

import {
  usePlaidLink,
  PlaidLinkOptions,
  PlaidLinkOnSuccess,
  PlaidLinkOnSuccessMetadata,
} from 'react-plaid-link';
import jwt_decode from "jwt-decode";


function App() {
  const [user, setUser] = useState()
  const [token, setToken] = useState(undefined);
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


  const handleGoogleResponseCallBack = (response: any) => {
    let userObj: any = jwt_decode(response.credential);

    fetch(`${import.meta.env.VITE_BACKEND_BASE_URL}/user`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        first_name: userObj.given_name,
        last_name: userObj.family_name,
        email: userObj.email,
        profile_pic_url: userObj.picture,
      }),
      credentials: "omit",
    })
      .then((res) => {
        if (res.ok) {
          setUser(userObj);
          document.getElementById("signInDiv").hidden = true;
        }
      })
      .catch((err) => console.error(err));
  };

  function handleSignOut(event: any) {
    setUser(undefined);
    document.getElementById("signInDiv").hidden = false;
  }

  useEffect(() => {
    /* global google */
    google.accounts.id.initialize({
      client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
      callback: handleGoogleResponseCallBack,
    });

    google.accounts.id.renderButton(document.getElementById("signInDiv"), {
      theme: "outline",
      size: "large",
    });
  })

  return (
    <div className="App">
      {user && <button onClick={(e) => handleSignOut(e)}>Sign Out</button>}
      <div id="signInDiv"></div>
      {user && <PlaidLink token={token} ready={ready} open={open} />}
    </div>
  )
}

export default App
