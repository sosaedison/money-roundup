import { useCallback, useState } from 'react';
import {
    usePlaidLink,
    PlaidLinkOptions,
    PlaidLinkOnSuccess,
    PlaidLinkOnSuccessMetadata,
  } from 'react-plaid-link';

  interface Props {
    token: string | undefined,
    open: Function,
    ready: boolean
  }

export default function PlaidLink({token, open, ready}: Props) {

    const onSuccess: PlaidLinkOnSuccess = useCallback(async (publicToken: string, metadata: PlaidLinkOnSuccessMetadata) => {
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

    return (
        <button onClick={() => open()
        } disabled={!ready}>
        <strong>Link account</strong>
      </button>
    )
}