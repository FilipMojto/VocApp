// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'
import PersonalVocabulary from './personal_vocabulary/PersonalVocabulary.tsx'
import VocapHeaderV1 from './headers/VocapHeaderV1/VocappHeaderV1.tsx'
import LoginPanel from './user_account/login_panel/LoginPanel.tsx'
import RegisterPanel from './user_account/register_panel/RegisterPanel.tsx'
import AuthPanelToggler from './user_account/panel_toggler/AuthPanelToggler.tsx'
import { useState } from 'react'
import { AuthProvider } from './user_account/auth_context/AuthContext.tsx'
import Homepage from './homepage/Homepage.tsx'
import { type WindowType } from './headers/VocapHeaderV1/VocapHeaderMenuBarV1/VocapHeaderMenuBarV1.tsx'

function App() {
  // const [count, setCount] = useState(0)
  // const [mode, setMode] = useState<"login" | "register">("login");
  const [currentWindow, setCurrentWindow] = useState<WindowType>("home");

  return (
    // <>
    <AuthProvider>
      <div id="app-container">
        <header>
          <VocapHeaderV1 setCurrentWindow={setCurrentWindow} />
        </header>
        
        <main>
          {/* <PersonalVocabulary /> */}
          {/* <AuthPanelToggler></AuthPanelToggler> */}
          {currentWindow === "home" && <Homepage />}
          {currentWindow === "vocab" && <PersonalVocabulary />}
          {/* {currentWindow === "recommender" && <AuthPanelToggler/>} */}
          {currentWindow === "auth" && <AuthPanelToggler setCurrentWindow={setCurrentWindow}/>}
        </main>

        <footer>

        </footer>
      </div>
    </AuthProvider>
    // </>
  )
}

export default App
