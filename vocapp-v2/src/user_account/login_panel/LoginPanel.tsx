import "./LoginPanel.css";
import AuthPanel, { type AuthPanelProps } from "../auth_panel/AuthPanel";
import { useState } from "react";
import api, { loginUser } from "../../api";

export interface LoginPanelProps extends AuthPanelProps {
  onLoginSuccess: (user: any) => void;
}

function LoginPanel({
  authTitle = "Welcome Back",
  authSubtitle = "Please log in to continue",
  submitButtonText = "Proceed",
  secondaryButtonText = "Register",
  extraInputs,
  onToggle,
  onLoginSuccess,
}: // onLoginSuccess
LoginPanelProps) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleLogin(e: React.FormEvent) {
    console.log("Logging in with", username, password);
    e.preventDefault();
    setError("");

    try {
      // const profile = await api.get("/users/me");
      const { access_token } = await loginUser(username, password);
      localStorage.setItem("token", access_token);

      // Fetch profile after login
      const profile = await api.get("/users/me");
      onLoginSuccess(profile.data);
      // onLoginSuccess(profile.data);
    } catch (err: any) {
      setError("Invalid username or password");
    }
  }

  return (
    <AuthPanel
      authTitle={authTitle}
      authSubtitle={authSubtitle}
      submitButtonText={submitButtonText}
      secondaryButtonText={secondaryButtonText}
      extraInputs={extraInputs}
      onSubmit={handleLogin}
      onUsernameChange={setUsername}
      onPasswordChange={setPassword}
      onToggle={onToggle}
      // mode='login'
      authPanelClassName="login-panel"
      authTitleClassName="login-title"
      authSubtitleClassName="login-subtitle"
      authFormClassName="login-form"
      submitButtonClassName="login-button"
      secondaryButtonClassName="secondary-button"
      error={error}
    />
  );
}

export default LoginPanel;
