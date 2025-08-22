import { useState } from "react";
import RegisterPanel from "../register_panel/RegisterPanel";
import LoginPanel from "../login_panel/LoginPanel";

function AuthPanelToggler() {
  const [isRegister, setIsRegister] = useState(false);

  const togglePanel = () => {
    setIsRegister((prev) => !prev);
  };

  return (
    <div>
      {isRegister ? (
        <RegisterPanel onToggle={togglePanel} />
      ) : (
        <LoginPanel onToggle={togglePanel} />
      )}
    </div>
  );
}

export default AuthPanelToggler;