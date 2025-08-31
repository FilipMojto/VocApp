import './vocap_header_menu_bar_v1.css';

// src/types/Window.ts
// src/types/Window.ts
export type WindowType = "home" | "vocab" | "test" | "recommender" | "auth";

export interface VocapHeaderMenuBarV1Props {
  setCurrentWindow?: (window: "home" | "vocab" | "test" | "recommender" | "auth") => void;
}

function VocapHeaderMenuBarV1({setCurrentWindow} : VocapHeaderMenuBarV1Props) {
  return (
    <nav id="vocap-header-menu-bar-v1">
      <a href="#" onClick={() => setCurrentWindow?.("home")}>Home</a>
      <a href="#" onClick={() => setCurrentWindow?.("vocab")}>My Vocabulary</a>
      <a href="#" onClick={() => setCurrentWindow?.("test")}>Test Me</a>
      <a href="#" onClick={() => setCurrentWindow?.("recommender")}>Get Smart Words</a>
    </nav>
  );
}

export default VocapHeaderMenuBarV1;