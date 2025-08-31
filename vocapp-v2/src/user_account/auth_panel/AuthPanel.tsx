import "./AuthPanel.css";

import InputIconContainer from "../../components/icon_slots/input_icon_container/InputIconContainer";

export interface AuthPanelProps {
  authTitle?: string;
  authSubtitle?: string;
  submitButtonText?: string;
  secondaryButtonText?: string;
  extraInputs?: React.ReactNode;
  onSubmit?: (e: React.FormEvent) => void;
  onUsernameChange?: (username: string) => void;
  onPasswordChange?: (password: string) => void;
  authPanelClassName?: string;
  authTitleClassName?: string;
  authSubtitleClassName?: string;
  authFormClassName?: string;
  submitButtonClassName?: string;
  secondaryButtonClassName?: string;
  error?: string;
  onToggle?: () => void;
}

function AuthPanel({
  authTitle = "Welcome Back",
  authSubtitle = "Please log in to continue",
  submitButtonText = "Proceed",
  secondaryButtonText = "Register",
  extraInputs,
  onToggle,
  authPanelClassName,
  authTitleClassName,
  authSubtitleClassName,
  authFormClassName,
  submitButtonClassName,
  secondaryButtonClassName,
  onSubmit,
  onUsernameChange,
  onPasswordChange,
  error,
}: // onLoginSuccess
AuthPanelProps) {
  return (
    <div
      className={`auth-panel${
        authPanelClassName ? ` ${authPanelClassName}` : ""
      }`}
    >
      <h2
        className={`auth-panel-title${
          authTitleClassName ? ` ${authTitleClassName}` : ""
        }`}
      >
        {authTitle}
      </h2>
      <p
        className={`login-subtitle${
          authSubtitleClassName ? ` ${authSubtitleClassName}` : ""
        }`}
      >
        {authSubtitle}
      </p>

      <form
        className={`login-form${
          authFormClassName ? ` ${authFormClassName}` : ""
        }`}
        onSubmit={onSubmit}
      >
        <InputIconContainer
          icon={
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              strokeWidth="1.5"
              stroke="currentColor"
              className="icon"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M15.75 6a3.75 3.75 0 1 1-7.5 0 
                            3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 
                            14.998 0A17.933 17.933 0 0 1 12 
                            21.75c-2.676 0-5.216-.584-7.499-1.632Z"
              />
            </svg>
          }
          clearable={false}
          placeholder="Username"
          type="text"
          onChange={(e) => onUsernameChange && onUsernameChange(e.target.value)}
        />

        <InputIconContainer
          icon={
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              strokeWidth="1.5"
              stroke="currentColor"
              className="icon"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M15.75 5.25a3 3 0 0 1 3 
                            3m3 0a6 6 0 0 1-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 
                            17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 
                            .43-1.563A6 6 0 1 1 21.75 8.25Z"
              />
            </svg>
          }
          clearable={false}
          placeholder="Password"
          type="password"
          onChange={(e) => onPasswordChange && onPasswordChange(e.target.value)}
        />

        {extraInputs}

        {error && <p className="auth-error">{error}</p>}

        <button
          type="submit"
          className={`login-button${
            submitButtonClassName ? ` ${submitButtonClassName}` : ""
          }`}
        >
          {submitButtonText}
        </button>
      </form>

      <button
        className={`secondary-button${
          secondaryButtonClassName ? ` ${secondaryButtonClassName}` : ""
        }`}
        onClick={() => {
          // call the provided toggle callback (if any)
          if (onToggle) onToggle();
        }}
      >
        {secondaryButtonText}
      </button>
    </div>
  );
}

export default AuthPanel;
