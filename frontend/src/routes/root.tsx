import { Session } from "@supabase/supabase-js";
import { useCallback, useEffect, useState } from "react";
import AccountItemList from "../AccountItemList";
import "../App.css";
import PlaidLink from "../PlaidLink";
import UserAuthModal from "../UserAuthModal";
import { supabase } from "../supabaseClient";

import {
  PlaidLinkOnSuccess,
  PlaidLinkOnSuccessMetadata,
  PlaidLinkOptions,
  usePlaidLink,
} from "react-plaid-link";

const API_BASE = import.meta.env.VITE_LOCAL_BASE_BACKEND_URL;

export default function Root() {
  const [session, setSession] = useState<Session | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [accounts, setAccounts] = useState<{ name: string }[]>([]);

  useEffect(() => {
    // Check for existing session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
    });

    // Listen for auth state changes (login, logout, token refresh)
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });

    return () => subscription.unsubscribe();
  }, []);

  const accessToken = session?.access_token;
  const userID = session?.user?.id;
  const email = session?.user?.email;

  const onSuccess: PlaidLinkOnSuccess = useCallback(
    async (publicToken: string, metadata: PlaidLinkOnSuccessMetadata) => {
      if (!accessToken) return;

      try {
        const exchangeRes = await fetch(
          `${API_BASE}/api/exchange/public/token`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${accessToken}`,
            },
            body: JSON.stringify({ public_token: publicToken }),
          }
        );
        const exchangeData = await exchangeRes.json();

        if (exchangeData["access_token_created"]) {
          const itemRes = await fetch(`${API_BASE}/api/item`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${accessToken}`,
            },
            body: JSON.stringify({
              access_token: exchangeData["access_token"],
            }),
          });
          const itemData = await itemRes.json();

          if (itemData["item_created"]) {
            fetchAccounts();
          }
        }
      } catch (err) {
        console.error("Failed to exchange token:", err);
      }
    },
    [accessToken]
  );

  const onExit = useCallback(async () => {}, []);

  const config: PlaidLinkOptions = {
    onSuccess,
    onExit,
    token,
  };
  const { open, ready } = usePlaidLink(config);

  async function handleSignOut() {
    await supabase.auth.signOut();
  }

  const fetchAccounts = () => {
    if (!accessToken) return;

    fetch(`${API_BASE}/api/account`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    })
      .then((res) => res.json())
      .then((data) => setAccounts(data))
      .catch((err) => console.error(err));
  };

  async function handleSignUp(email: string, password: string) {
    const { error } = await supabase.auth.signUp({ email, password });
    if (error) {
      alert(error.message);
    } else {
      alert("Check your email for a verification link!");
    }
  }

  async function handleSignIn(email: string, password: string) {
    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });
    if (error) {
      alert(error.message);
    }
  }

  function routeToForgotPassword() {
    window.location.href = "/forgot-password";
  }

  return (
    <div className="App">
      {!session && (
        <UserAuthModal
          handleSignUp={handleSignUp}
          handleSignIn={handleSignIn}
          routeToForgotPassword={routeToForgotPassword}
        />
      )}

      {session && (
        <>
          <p>Signed in as {email}</p>
          <button onClick={handleSignOut}>Sign Out</button>
          <PlaidLink ready={ready} open={open} />
          <AccountItemList accounts={accounts} />
        </>
      )}
    </div>
  );
}
