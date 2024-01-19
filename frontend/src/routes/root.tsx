import { useCallback, useEffect, useState } from "react";
import AccountItemList from "../AccountItemList";
import "../App.css";
import { REQUEST_VERIFICATION_URL } from "../Constants";
import PlaidLink from "../PlaidLink";
import UserAuthModal from "../UserAuthModal";

import {
  PlaidLinkError,
  PlaidLinkOnEvent,
  PlaidLinkOnExit,
  PlaidLinkOnSuccess,
  PlaidLinkOnSuccessMetadata,
  PlaidLinkOptions,
  usePlaidLink,
} from "react-plaid-link";

const ACCESS_TOKEN_KEY = "moneyroundup_access_token";

export default function Root() {
  const [user, setUser] = useState();
  const [email, setEmail] = useState(null);
  const [token, setToken] = useState(null);
  const [userID, setUserID] = useState<string | null>(null);
  const [accounts, setAccounts] = useState(Array);

  useEffect(() => {
    // check if user is logged in
    // check local storage for access token
    const accessToken = localStorage.getItem(ACCESS_TOKEN_KEY);
    if (accessToken) {
      // fetch user data
      const isTokenValid = async () => {
        try {
          const data = await getUserInfo(accessToken);
          // token is valid so set user data
          setEmail(data["email"]);
          setUserID(data["id"]);
          fetchLinkToken();
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
      throw new Error("Failed to get user info");
    }
    const data = await res.json();
    return data;
  }

  function cleanUserData() {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    setUserID(null);
    setEmail(null);
  }

  async function createItem(userID: string | null, accessToken: string): Promise<boolean> {
    const res = await fetch(`${import.meta.env.VITE_LOCAL_BASE_BACKEND_URL}/api/item/create`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ user_id: userID, access_token: accessToken }),
    })

    if (res.status !== 200) {
      return false;
    }

    const data = await res.json();
    if (data["item_created"]) {
      return true;
    }
    return false;
  }

  const onSuccess: PlaidLinkOnSuccess = useCallback(
    async (publicToken: string, metadata: PlaidLinkOnSuccessMetadata) => {
      await fetch(`${import.meta.env.VITE_LOCAL_BASE_BACKEND_URL}/api/exchange/public/token`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ public_token: publicToken }),
      })
        .then((res) => res.json())
        .then(async (data) => {
          if (data["access_token_created"] === true) {
            const itemCreated = await createItem(userID, data["access_token"]);

            if (itemCreated) {
              fetchAccounts();
            }
          }
        })
        .catch((err) => alert("Failed to get access_token"));
    },
    [userID]
  );
  async function fetchLinkToken() {
    await fetch(`${import.meta.env.VITE_LOCAL_BASE_BACKEND_URL}/api/link/token/create`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        accept: "application/json",
        Authorization:
          "Bearer " + localStorage.getItem("moneyroundup_access_token"),
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setToken(data["link_token"]);
      })
      .catch((err) => console.log(err));
  }
  const onExit: PlaidLinkOnExit = async (error: PlaidLinkError | null) => {
    if (error != null) {
      console.log("Error: ", error);
    }
  }

  const onEvent: PlaidLinkOnEvent = async (eventName: string, metadata: any) => {
    console.info("onEvent: ", eventName, metadata);
  }

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

  const config: PlaidLinkOptions = {
    onSuccess,
    onExit,
    onEvent,
    token
  };
  const { open, ready, exit, error } = usePlaidLink(config);

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
          <PlaidLink
            open={open}
            ready={ready}
          />

          <AccountItemList accounts={accounts} />
        </>
      )}
    </div>
  );
}
