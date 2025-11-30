import '../login_panel/LoginPanel.css';
import InputIconContainer from '../../components/icon_slots/input_icon_container/InputIconContainer';
import type { AuthPanelProps } from '../auth_panel/AuthPanel';
import AuthPanel from '../auth_panel/AuthPanel';
import { useState } from 'react';
import api, { loginUser, registerUser } from '../../api/api';

interface RegisterPanelProps extends AuthPanelProps {
  onRegisterSuccess: (user: any) => void;
}

function RegisterPanel({onRegisterSuccess, onToggle}: RegisterPanelProps) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleRegister(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    try {
      // 1. Register
      // await api.post("/users/", { username, password });
      await registerUser(username, password);

      // 2. Auto-login after registration
      // const loginRes = await api.post(
      //   "/auth/login",
      //   new URLSearchParams({ username, password }),
      //   { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
      // );
      // localStorage.setItem("token", (loginRes.data as { access_token: string }).access_token);
      const { access_token} = await loginUser(username, password);
      localStorage.setItem("token", access_token);


      // 3. Fetch profile
      const profile = await api.get("/users/me");
      onRegisterSuccess(profile.data);
    } catch (err: any) {
      setError(err.message || "Registration failed");
    }
  }
  
  return (
    <AuthPanel
      authTitle="Create Account"
      authSubtitle="Please register to continue"
      submitButtonText="Register"
      secondaryButtonText="Back to Login"
      onToggle={onToggle}   // 👈 pass toggle handler down
      // mode='register'
      onSubmit={handleRegister}
      onUsernameChange={setUsername}
      onPasswordChange={setPassword}
      error={error}

      extraInputs={
        <>
          <InputIconContainer
            icon={
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 5.25a3 3 0 0 1 3 3m3 0a6 6 0 0 1-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 .43-1.563A6 6 0 1 1 21.75 8.25Z" />
                </svg>

            }
            placeholder="Retype Password"
            type="password"
          />
        </>
      }
                  authPanelClassName="login-panel"
            authTitleClassName="login-title"
            authSubtitleClassName="login-subtitle"
            authFormClassName="login-form"
            submitButtonClassName="login-button"
            secondaryButtonClassName="secondary-button"
    />
  );
}

export default RegisterPanel;