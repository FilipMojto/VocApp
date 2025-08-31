import { useEffect, useRef, useState } from "react";
import ButtonIconContainer from "../../components/icon_slots/label_icon_container/ButtonIconContainer";
import VocapHeaderMenuBarV1, { type VocapHeaderMenuBarV1Props } from "./VocapHeaderMenuBarV1/VocapHeaderMenuBarV1.tsx";
import AccountMenuBar from "./AccountMenuBar/AccountMenuBar.tsx";
import "./vocapp_header_v1.css";
import { useAuth } from "../../user_account/auth_context/AuthContext.tsx";

export interface VocapHeaderV1Props extends VocapHeaderMenuBarV1Props {
  
}

function VocapHeaderV1({setCurrentWindow} : VocapHeaderV1Props) {
    const { user, setUser, mode, setMode } = useAuth();
      const menuRef = useRef<HTMLDivElement>(null);
  const [isAccountMenuOpen, setIsAccountMenuOpen] = useState(false);

  useEffect(() => {
    if (!isAccountMenuOpen) return;

    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsAccountMenuOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isAccountMenuOpen]);
  
  return (
    <div id="vocap-header-v1">
      <h1>Vocapp</h1>
      <VocapHeaderMenuBarV1 setCurrentWindow={setCurrentWindow} />

      <div style={{ position: "relative" }} ref={menuRef}>
        <ButtonIconContainer
          icon={
            <svg
              id="vocap-header-account-icon"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="size-6"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
              />
            </svg>
          }
          label="Account"
          containerClassName="vocap-header-button-container"
          iconSlotClassName="vocap-header-icon-slot"
          labelClassName="vocap-header-label"
          // onClick={() => setIsAccountMenuOpen((prev) => !prev)}
          onClick={() => {
            if (user) {
              // Toggle account menu if logged in
              setIsAccountMenuOpen((prev) => !prev);
            } else {
              // Force AuthPanelToggler to show login panel
              setMode("login");
              setCurrentWindow?.("auth")
            }}}
        />

        {isAccountMenuOpen && user && (
          <div className="account-menu-wrapper">
            <AccountMenuBar />
          </div>
        )} 
      </div>
    </div>
  );
}

export default VocapHeaderV1;