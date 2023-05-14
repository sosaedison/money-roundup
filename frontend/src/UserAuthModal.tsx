import React, { useState } from "react";
import "./UserAuthModal.css";

interface UserAuthModalProps {
  handleSignUp: (e: React.FormEvent) => void;
  handleSignIn: (e: React.FormEvent) => void;
  routeToForgotPassword?: (e: React.FormEvent) => void;
}

const UserAuthModal: React.FC<UserAuthModalProps> = ({
  handleSignUp,
  handleSignIn,
  routeToForgotPassword,
}) => {
  const [isSignUp, setIsSignUp] = useState(false);

  const handleTabClick = (value: boolean) => {
    setIsSignUp(value);
  };

  // prefill email if provided in URL from email verification success
  let userEmail: string | null | undefined = new URLSearchParams(
    window.location.search
  ).get("email");
  if (userEmail === null) {
    userEmail = undefined;
  }

  return (
    <div className="flex items-center bg-zinc-900">
      <div className="">
        <div className="tab-container">
          <button
            className={`tab ${!isSignUp ? "active" : ""}`}
            onClick={() => handleTabClick(false)}
          >
            Sign In
          </button>
          <button
            className={`tab ${isSignUp ? "active" : ""}`}
            onClick={() => handleTabClick(true)}
          >
            Sign Up
          </button>
        </div>
        <div className="form-container">
          {!isSignUp ? (
            <form onSubmit={handleSignIn} className="form">
              <input
                type="email"
                placeholder="Email"
                value={userEmail}
                required
              />
              <input type="password" placeholder="Password" required />
              <button type="submit">Sign In</button>
              <button type="button" onClick={routeToForgotPassword}>
                Forgot Password?
              </button>
            </form>
          ) : (
            <form onSubmit={handleSignUp} className="form">
              <input type="email" placeholder="Email" required />
              <input type="password" placeholder="Password" required />
              <input type="password" placeholder="Confirm Password" required />
              <button type="submit">Sign Up</button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserAuthModal;
