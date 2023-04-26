const GoogleLoginButton = () => {
    const handleGoogleLogin = async () => {
        const response = await fetch('http://localhost:8000/api/auth/google/authorize');
        const data = await response.json();
        // window.location.href = data.authorization_url;
        const redirectUrl = data.authorization_url;
        const popupWindow = window.open(redirectUrl, 'popupWindow', 'height=500,width=500');
        console.log(popupWindow);

      };

    return (
        <button onClick={handleGoogleLogin}>
        Sign in with Google
        </button>
    );
};

export default GoogleLoginButton;