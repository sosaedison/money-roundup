import { useEffect, useState } from "react";
import { supabase } from "../supabaseClient";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [requesting, setRequesting] = useState(true);
  const [newPassword, setNewPassword] = useState("");

  useEffect(() => {
    // If the URL contains a recovery token (via hash fragment from Supabase),
    // the SDK will automatically pick it up and establish a session.
    // We just need to detect that we're in "reset" mode.
    const params = new URLSearchParams(window.location.search);
    const type = params.get("type");
    if (type === "recovery") {
      setRequesting(false);
    }

    // Also check hash params (Supabase sends tokens in the hash)
    const hashParams = new URLSearchParams(
      window.location.hash.replace("#", "?")
    );
    if (hashParams.get("type") === "recovery") {
      setRequesting(false);
    }
  }, []);

  async function handleForgotPassword() {
    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/forgot-password?type=recovery`,
    });
    if (error) {
      alert(error.message);
    } else {
      alert("Password reset email sent. Check your inbox.");
    }
  }

  async function handleResetPassword() {
    const { error } = await supabase.auth.updateUser({
      password: newPassword,
    });
    if (error) {
      alert(error.message);
    } else {
      alert("Password successfully reset!");
      window.location.href = "/";
    }
  }

  return (
    <>
      {requesting && (
        <div>
          <h1>Forgot Password</h1>
          <p>Enter your email below to reset your password.</p>
          <input
            onChange={(e) => setEmail(e.target.value)}
            type="email"
            placeholder="Email"
          />
          <button onClick={handleForgotPassword}>Reset Password</button>
        </div>
      )}
      {!requesting && (
        <div>
          <h1>Please enter your new password</h1>
          <input
            onChange={(e) => setNewPassword(e.target.value)}
            type="password"
            placeholder="New Password"
          />
          <input type="password" placeholder="Confirm New Password" />
          <button onClick={handleResetPassword}>Submit</button>
        </div>
      )}
    </>
  );
}
