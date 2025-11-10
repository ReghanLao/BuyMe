import React, { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL;

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();

    if (!loggedIn) {
        try {
            const response = await fetch(`${API_URL}/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (response.ok) {
                setMessage(data.message);
                setLoggedIn(true);
            } else {
                setMessage(data.message || "Invalid username or password.");
            }
            } catch (err) {
                console.error(err);
                setMessage("Error connecting to server.");
        }
    } else {
        setLoggedIn(false);
        setUsername("");
        setPassword("");
        setMessage("Logged out");
    }

  };

  return (
        <div className="login-container">
            <h2>Login</h2>
            <form onSubmit={handleLogin}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                    disabled={loggedIn}
                />
                <input
                    type="text"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    disabled={loggedIn}
                />
                <button type="submit">
                    {loggedIn ? "Logout" : "Login"}
                </button>
            </form>
            <p>{message}</p>
        </div>
    );
}

export default Login;
