export default function VerifyEmailSuccess() {
  function redirectToLogin() {
    window.location.href = "/";
  }

  return (
    <div>
      <h1>Email Verified!</h1>
      <p>Your email has been verified successfully.</p>
      <p>You can now log in.</p>
      <button onClick={redirectToLogin}>Login Here</button>
    </div>
  );
}
