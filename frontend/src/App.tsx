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
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);
  const [userID, setUserID] = useState("")
  const [accounts, setAccounts] = useState()

  const createLinkToken = useCallback(async () => {
    const response = await fetch("http://127.0.0.1:8000/link/token/create", {});
    const data = await response.json();
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
      body: JSON.stringify({ public_token: publicToken}),
    })
    .then(res => res.json())
    .then((data) => {
      if (data["access_token_created"] === true) {
        fetch(`${import.meta.env.VITE_BACKEND_BASE_URL}/item`, {
          "method": "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({user_id: userID, access_token: data["access_token"]})
        })
        .then(res => res.json())
        .then((data) => {
          if (data["item_created"]) return;
        })
        .catch((err) => console.log(err))
      }
    })
    .catch(err => alert("Failed to get access_token"));
  }, [userID])

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
      .then((res) => res.json())
      .then((data) => {
        // Once the user logs in, fetch a link token to add Bank Connections
        const fresh_link_token = createLinkToken()
        setToken(fresh_link_token)
        // Once the token is created, set the user object
        setUser(userObj);
        console.log(data)
        setUserID(data.user_id)
        document.getElementById("signInDiv").hidden = true; // hide the login button
      })
      .catch((err) => console.error(err));
  };

  function handleSignOut(event: any) {
    setUser(undefined);
    document.getElementById("signInDiv").hidden = false;
  }

  const fetchAccounts = useCallback((event: any) => {
    fetch(`${import.meta.env.VITE_BACKEND_BASE_URL}/account?user_id=${userID}`)
    .then(res => res.json())
    .then((data) => {
      console.log(data)
    })
    .catch(err => console.error(err))
  }, [userID])

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
      {user && <><button onClick={(e) => handleSignOut(e)}>Sign Out</button> <PlaidLink ready={ready} open={open} /> <button onClick={(e) => fetchAccounts(e)}>Fetch Accounts</button> </>}
      <div id="signInDiv"></div>
      {}
    </div>
  )
}

export default App
