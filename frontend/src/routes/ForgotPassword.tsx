import { useEffect, useState } from "react";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [requesting, setRequesting] = useState(true);
  const [newPassword, setNewPassword] = useState("");
  const [token, setToken] = useState("");

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const error: string | null = params.get("error");
    const token: string | null = params.get("token");
    console.log(typeof error, error);
    if (error) {
      alert("There was an error resetting your password.");
    } else if (token) {
      setRequesting(false);
      setToken(token);
    }
  }, []);

  async function handleForgotPassword() {
    await fetch(
      `${import.meta.env.VITE_LOCAL_BASE_BACKEND_URL}/api/auth/forgot-password`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          accept: "application/json",
        },
        body: JSON.stringify({
          email: email,
        }),
      }
    )
      .then((res) => {
        if (res.ok) {
          alert("Password reset email sent");
        }
      })
      .catch((err) => console.error(err));
  }
  function handleEmailChange(e: any) {
    setEmail(e.target.value);
  }
  function handleNewPasswordChange(e: any) {
    setNewPassword(e.target.value);
  }
  async function handleResetPassword() {
    await fetch(
      `${import.meta.env.VITE_LOCAL_BASE_BACKEND_URL}/api/auth/reset-password`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          accept: "application/json",
        },
        body: JSON.stringify({
          token: token,
          password: newPassword,
        }),
      }
    )
      .then((res) => {
        if (res.ok) {
          alert("Password successfully reset");
        }
      })
      .then((data) => {
        console.log(data);
        window.location.href = "/";
      })
      .catch((err) => console.error(err));
  }
  return (
    <>
      {requesting && (
        <div>
          <h1>Forgot Password</h1>
          <p>Enter your email below to reset your password.</p>
          <input
            onChange={handleEmailChange}
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
            onChange={handleNewPasswordChange}
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
