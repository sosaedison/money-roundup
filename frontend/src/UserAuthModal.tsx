import React, { useState } from "react";
import "./UserAuthModal.css";

interface UserAuthModalProps {
  handleSignUp: (email: string, password: string) => void;
  handleSignIn: (email: string, password: string) => void;
  routeToForgotPassword?: () => void;
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

  const onSignIn = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const email = (form.elements.namedItem("email") as HTMLInputElement).value;
    const password = (form.elements.namedItem("password") as HTMLInputElement)
      .value;
    handleSignIn(email, password);
  };

  const onSignUp = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const email = (form.elements.namedItem("email") as HTMLInputElement).value;
    const password = (form.elements.namedItem("password") as HTMLInputElement)
      .value;
    handleSignUp(email, password);
  };

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
            <form onSubmit={onSignIn} className="form">
              <input name="email" type="email" placeholder="Email" required />
              <input
                name="password"
                type="password"
                placeholder="Password"
                required
              />
              <button type="submit">Sign In</button>
              <button type="button" onClick={routeToForgotPassword}>
                Forgot Password?
              </button>
            </form>
          ) : (
            <form onSubmit={onSignUp} className="form">
              <input name="email" type="email" placeholder="Email" required />
              <input
                name="password"
                type="password"
                placeholder="Password"
                required
              />
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
