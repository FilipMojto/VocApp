import { useState } from "react";
import ButtonIconContainer from "../../components/icon_slots/label_icon_container/ButtonIconContainer";
import VocapHeaderMenuBarV1 from "./VocapHeaderMenuBarV1/VocapHeaderMenuBarV1.tsx";
import AccountMenuBar from "./AccountMenuBar/AccountMenuBar.tsx";
import "./vocapp_header_v1.css";

function VocapHeaderV1() {
  const [isAccountMenuOpen, setIsAccountMenuOpen] = useState(false);

  return (
    <div id="vocap-header-v1">
      <h1>Vocapp</h1>
      <VocapHeaderMenuBarV1 />

      <div style={{ position: "relative" }}>
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
          onClick={() => setIsAccountMenuOpen((prev) => !prev)}
        />

        {isAccountMenuOpen && (
          <div className="account-menu-wrapper">
            <AccountMenuBar />
          </div>
        )}
      </div>
    </div>
  );
}

export default VocapHeaderV1;