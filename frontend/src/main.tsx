import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import ErrorPage from "./ErrorPage";
import "./index.css";
import ForgotPassword from "./routes/ForgotPassword";
import Root from "./routes/root";
import VerifyEmailError from "./routes/VerifyEmailError";
import VerifyEmailSuccess from "./routes/VerifyEmailSuccess";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/verification-success",
    element: <VerifyEmailSuccess />,
  },
  {
    path: "/verification-error",
    element: <VerifyEmailError />,
  },
  {
    path: "/forgot-password",
    element: <ForgotPassword />,
  },
  {
    // Supabase redirects here after email verification/password reset.
    // The SDK picks up the token from the URL hash automatically,
    // then onAuthStateChange in Root fires. Redirect to home.
    path: "/auth/callback",
    element: <Root />,
  },
]);

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
