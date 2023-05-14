export default function VerifyEmailSuccess() {
  const LOGIN_URL =
    import.meta.env.VITE_ENV === "DEVELOPMENT"
      ? import.meta.env.VITE_LOCAL_BASE_FRONTEND_URL
      : import.meta.env.VITE_PRODUCTION_BASE_FRONTEND_URL;

  const params = new URLSearchParams(window.location.search);

  const userEmail: string | null = params.get("email");

  function redirectToLogin() {
    window.location.href = `${LOGIN_URL}?email=${userEmail}`;
  }
  return (
    <div>
      <h1>Verify Email Success</h1>
      <p>Your email has been verified.</p>
      <p>You can now log in.</p>
      <button onClick={redirectToLogin}>Login Here</button>
    </div>
  );
}
