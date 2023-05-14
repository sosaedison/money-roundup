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
]);

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
