export const REQUEST_VERIFICATION_URL =
  import.meta.env.VITE_ENV === "DEVELOPMENT"
    ? `${
        import.meta.env.VITE_LOCAL_BASE_BACKEND_URL
      }/api/auth/request-verify-token`
    : `${
        import.meta.env.VITE_PRODUCTION_BASE_BACKEND_URL
      }/api/auth/request-verify-token`;
