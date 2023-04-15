import React, { useState } from 'react';
import './UserAuthModal.css';

interface UserAuthModalProps {
  handleSignUp: (e: React.FormEvent) => void,
  handleSignIn: (e: React.FormEvent) => void;
}


const UserAuthModal: React.FC<UserAuthModalProps> = ({ handleSignUp, handleSignIn }) => {
    const [isSignUp, setIsSignUp] = useState(false);

    const handleTabClick = (value: boolean) => {
      setIsSignUp(value);
    };

    return (
    <div className="modal">
        <div className="modal-content">
            <div className="tab-container">
                <button
                    className={`tab ${!isSignUp ? 'active' : ''}`}
                    onClick={() => handleTabClick(false)}
                >
                Sign In
                </button>
                <button
                    className={`tab ${isSignUp ? 'active' : ''}`}
                    onClick={() => handleTabClick(true)}
                >
                Sign Up
                </button>
            </div>
            <div className="form-container">
                {!isSignUp ? (
                    <form onSubmit={handleSignIn} className="form">
                    <input type="email" placeholder="Email" required />
                    <input type="password" placeholder="Password" required />
                    <button type="submit">Sign In</button>
                    </form>
                ) : (
                    <form onSubmit={handleSignUp} className="form">
                    <input type="email" placeholder="Email" required />
                    <input type="password" placeholder="Password" required />
                    <button type="submit">Sign Up</button>
                    </form>
                )}
            </div>
        </div>
    </div>
  );
}

export default UserAuthModal