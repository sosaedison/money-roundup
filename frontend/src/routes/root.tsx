import { useCallback, useEffect, useState } from "react";
import AccountItemList from "../AccountItemList";
import "../App.css";
import { REQUEST_VERIFICATION_URL } from "../Constants";
import PlaidLink from "../PlaidLink";
import UserAuthModal from "../UserAuthModal";

import {
  PlaidLinkOnSuccess,
  PlaidLinkOnSuccessMetadata,
  PlaidLinkOptions,
  usePlaidLink,
} from "react-plaid-link";

export default function Root() {
  const [user, setUser] = useState();
  const [email, setEmail] = useState(null);
  const [token, setToken] = useState(null);
  const [userID, setUserID] = useState(null);
  const [accounts, setAccounts] = useState(Array);

  useEffect(() => {
    // check if user is logged in
    // check local storage for access token
    const accessToken = localStorage.getItem("moneyroundup_access_token");
    if (accessToken) {
      // fetch user data
      const isTokenValid = async () => {
        try {
          const data = await getUserInfo(accessToken);
          // token is valid
          // set user data
          setEmail(data["email"]);
          setUserID(data["id"]);
        } catch (error) {
          // token is invalid
          cleanUserData();
        }
      };
      isTokenValid();
    } else {
      console.log("User is not logged in");
    }
  }, []);

  async function getUserInfo(accessToken: string) {
    const res = await fetch(
      `${import.meta.env.VITE_LOCAL_BASE_BACKEND_URL}/api/auth/users/me`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    if (res.status !== 200) {
      throw new Error("Get userInfo was not ok");
    }
    const data = await res.json();
    return data;
  }

  function cleanUserData() {
    localStorage.removeItem("moneyroundup_access_token");
    setUserID(null);
    setEmail(null);
  }

  const onSuccess: PlaidLinkOnSuccess = useCallback(
    async (publicToken: string, metadata: PlaidLinkOnSuccessMetadata) => {
      await fetch("http://127.0.0.1:8000/exchange/public/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ public_token: publicToken }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data["access_token_created"] === true) {
            fetch(`${import.meta.env.VITE_LOCAL_BASE_BACKEND_URL}/item`, {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                user_id: userID,
                access_token: data["access_token"],
              }),
            })
              .then((res) => res.json())
              .then((data) => {
                if (data["item_created"]) {
                  fetchAccounts();
                }
              })
              .catch((err) => console.log(err));
          }
        })
        .catch((err) => alert("Failed to get access_token"));
    },
    [userID]
  );
  const onExit = useCallback(async () => {}, []);

  const config: PlaidLinkOptions = {
    onSuccess,
    onExit,
    token,
  };
  const { open, ready, exit, error } = usePlaidLink(config);

  function handleSignOut(event: any) {
    event.preventDefault();
    setUserID(null);
    setEmail(null);
    localStorage.removeItem("moneyroundup_access_token");
  }

  const fetchAccounts = () => {
    fetch(
      `${import.meta.env.VITE_LOCAL_BASE_BACKEND_URL}/account?user_id=${userID}`
    )
      .then((res) => res.json())
      .then((data) => {
        console.log(`data ${data[0]}`);
        setAccounts(data);
      })
      .catch((err) => console.error(err));
  };

  function routeToForgotPassword(event: any) {
    event.preventDefault();
    window.location.href = "/forgot-password";
  }
  const handleSignUp = async (e: any) => {
    e.preventDefault();
    const email = e.target[0].value;
    const password = e.target[1].value;

    await fetch(
      `${import.meta.env.VITE_LOCAL_BASE_BACKEND_URL}/api/auth/register`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          accept: "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password,
          is_active: true,
          is_superuser: false,
          is_verified: false,
        }),
      }
    )
      .then((res) => res.json())
      .then((data) => {
        requestEmailVerification(data["email"]);
      })
      .catch((err) => console.error(err));
  };

  async function requestEmailVerification(email: string) {
    await fetch(REQUEST_VERIFICATION_URL, {
      method: "POST",
      headers: {
        accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email: email }),
    }).then((res) => {
      if (res.ok) {
        alert("Verification email sent");
      }
    });
  }

  const handleSignIn = (e: any) => {
    e.preventDefault();
    const username = e.target[0].value;
    const password = e.target[1].value;

    const urlSearchParams = new URLSearchParams();
    urlSearchParams.append("username", username);
    urlSearchParams.append("password", password);
    const urlEncodedString = urlSearchParams.toString();

    fetch(`${import.meta.env.VITE_LOCAL_BASE_BACKEND_URL}/api/auth/jwt/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: urlEncodedString,
    })
      .then((res) => res.json())
      .then((data) => {
        localStorage.setItem("moneyroundup_access_token", data["access_token"]);
        fetch(
          `${import.meta.env.VITE_LOCAL_BASE_BACKEND_URL}/api/auth/users/me`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${data["access_token"]}`,
            },
          }
        )
          .then((res) => res.json())
          .then((data) => {
            setEmail(data);
            setUserID(data["id"]);
          })
          .catch((err) => console.error(err));
      })
      .catch((err) => console.error(err));
  };
  return (
    <div className="App">
      {!userID && (
        <>
          <UserAuthModal
            handleSignUp={handleSignUp}
            handleSignIn={handleSignIn}
            routeToForgotPassword={routeToForgotPassword}
          />
        </>
      )}

      {userID && (
        <>
          <button onClick={(e) => handleSignOut(e)}>Sign Out</button>
          <PlaidLink ready={ready} open={open} />

          <AccountItemList accounts={accounts} />
        </>
      )}
    </div>
  );
}
