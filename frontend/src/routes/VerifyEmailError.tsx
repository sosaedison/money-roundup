export default function VerifyEmailError() {
  return (
    <div>
      <h1>Verification Error</h1>
      <p>There was an error verifying your email.</p>
      <p>Please try signing up again or contact support.</p>
      <button onClick={() => (window.location.href = "/")}>
        Back to Home
      </button>
    </div>
  );
}
