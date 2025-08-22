// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'
import PersonalVocabulary from './personal_vocabulary/PersonalVocabulary.tsx'
import VocapHeaderV1 from './headers/VocapHeaderV1/VocappHeaderV1.tsx'
import LoginPanel from './user_account/login_panel/LoginPanel.tsx'
import RegisterPanel from './user_account/register_panel/RegisterPanel.tsx'
import AuthPanelToggler from './user_account/panel_toggler/AuthPanelToggler.tsx'

function App() {
  // const [count, setCount] = useState(0)

  return (
    <>
      <div id="app-container">
        <header>
          <VocapHeaderV1 />
        </header>
        
        <main>
          {/* <PersonalVocabulary /> */}
          <AuthPanelToggler></AuthPanelToggler>
        </main>

        <footer>

        </footer>
      </div>
    </>
  )
}

export default App
