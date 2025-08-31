import { useState } from "react";
import LoginPanel from "../login_panel/LoginPanel";
import RegisterPanel from "../register_panel/RegisterPanel";
import { useAuth } from "../auth_context/AuthContext";
import type { WindowType } from "../../headers/VocapHeaderV1/VocapHeaderMenuBarV1/VocapHeaderMenuBarV1";

export interface AuthContainerProps {
  // setMode: (mode: "login" | "register") => void;
  setCurrentWindow: (window: WindowType) => void;

}

export default function AuthContainer({setCurrentWindow}: AuthContainerProps) {
  // const [mode, setMode] = useState<"login" | "register">("login");
  // const [user, setUser] = useState<any>(null);
  const { user, setUser, mode, setMode } = useAuth();

  if (user) {
    return (
      <></>
    );
  }

  return (
    <div>
      {mode === "login" ? (
        <LoginPanel
           onLoginSuccess={(u: any) => {
            setUser(u);
            setCurrentWindow("home");
          }}
          onToggle={() => setMode("register")}
        />
      ) : mode === "register" ? (
        <RegisterPanel
          onRegisterSuccess={(u: any) => {
            setUser(u);
            setCurrentWindow("home");
          }}
          onToggle={() => setMode("login")}
        />
      ) : null}
    </div>
  );
}
