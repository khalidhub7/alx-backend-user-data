const credentials = btoa("username:password");  // Base64 encode
localStorage.setItem('auth', credentials);  // Store securely

fetch("/api/v1/protected-route", {
    headers: {
        "Authorization": `Basic ${localStorage.getItem('auth')}`
    }
});
