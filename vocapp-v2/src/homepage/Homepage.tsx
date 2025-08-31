import NewTranslationModalWindow from '../personal_vocabulary/new_translation_modal_window/NewTranslationModalWindow';
import { useAuth } from '../user_account/auth_context/AuthContext';
import './Homepage.css';

function Homepage() {
  const { user, setUser } = useAuth();

  return (
    <div id="homepage-container">
      <div className="hero">
        <h1>Welcome to <span className="highlight">VocApp</span></h1>
        <p className="subtitle">
          Your personal vocabulary management tool.
        </p>

        {user ? (
          <div className="welcome-user">
            <p>Hello, <span className="username">{user.username}</span> 👋</p>
            {/* <button
              className="logout-button"
              onClick={() => {
                localStorage.removeItem('token');
                setUser(null);
              }}
            >
              Logout
            </button> */}
          </div>
        ) : (
          <div className="auth-buttons">
            {/* <button
              className="login-button"
              onClick={() => {
                // Optionally trigger AuthPanelToggler to show login
                const event = new CustomEvent('show-login-panel');
                window.dispatchEvent(event);
              }}
            >
              Login
            </button> */}
            {/* <button
              className="register-button"
              onClick={() => {
                const event = new CustomEvent('show-register-panel');
                window.dispatchEvent(event);
              }}
            >
              Register
            </button> */}
          </div>
        )}
      </div>

      <div className="features">
        <div className="feature-card">
          <h3>Track Vocabulary</h3>
          <p>Keep all your new words organized and accessible.</p>
        </div>
        <div className="feature-card">
          <h3>Test Yourself</h3>
          <p>Challenge yourself with personalized quizzes.</p>
        </div>
        <div className="feature-card">
          <h3>Learn Smartly</h3>
          <p>Get insights and recommendations for effective learning.</p>
        </div>
      </div>

      {/* <NewTranslationModalWindow></NewTranslationModalWindow> */}
    </div>
  );
}

export default Homepage;