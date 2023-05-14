import { useState } from "react";
import { REQUEST_VERIFICATION_URL } from "../Constants";

export default function VerifyEmailError() {
  const [userEmailForVerification, setUserEmailForVerification] = useState("");

  async function requestVerificationEmail() {
    await fetch(REQUEST_VERIFICATION_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email: userEmailForVerification }),
    }).then((response) => {
      if (response.ok) {
        alert("Email sent. If you do not receive it, please try again.");
      }
    });
  }
  function handleEmailChange(e: any) {
    setUserEmailForVerification(e.target.value);
  }
  return (
    <div>
      <h1>Verify Email Error</h1>
      <p>There was an error verifying your email.</p>
      <p>Please try again.</p> <br />
      <input
        id="email-for-reverification"
        onChange={handleEmailChange}
        type="email"
        placeholder="Please enter your email"
      />
      <button onClick={requestVerificationEmail}>
        Resend Email Verification
      </button>
    </div>
  );
}
