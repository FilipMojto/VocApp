import './LoginPanel.css';
import InputIconContainer from '../../components/icon_slots/input_icon_container/InputIconContainer';
import AuthPanel, { type AuthPanelProps } from '../auth_panel/AuthPanel';
export interface LoginPanelProps extends AuthPanelProps {
    // Define any props if needed in the future
    // loginTitle?: string;
    // loginSubtitle?: string;
    // loginButtonText?: string;
    // registerButtonText?: string;
    // extraInputs?: React.ReactNode;
    // onToggle: () => void;
}


function LoginPanel({
    authTitle = "Welcome Back",
    authSubtitle = "Please log in to continue",
    submitButtonText = "Proceed",
    secondaryButtonText = "Register",
    extraInputs,
    onToggle,
}: LoginPanelProps) {
    return (
        <AuthPanel
            authTitle={authTitle}
            authSubtitle={authSubtitle}
            submitButtonText={submitButtonText}
            secondaryButtonText={secondaryButtonText}
            extraInputs={extraInputs}
            onToggle={onToggle}
            authPanelClassName="login-panel"
            authTitleClassName="login-title"
            authSubtitleClassName="login-subtitle"
            authFormClassName="login-form"
            submitButtonClassName="login-button"
            secondaryButtonClassName="secondary-button"
        />
        // <div className="login-panel">
        //     <h2 className="login-title">{loginTitle}</h2>
        //     <p className="login-subtitle">{loginSubtitle}</p>

        //     <form className="login-form" onSubmit={(e) => e.preventDefault()}>
        //         <InputIconContainer
        //             icon={
        //                 <svg xmlns="http://www.w3.org/2000/svg" 
        //                     viewBox="0 0 24 24" 
        //                     fill="none" 
        //                     strokeWidth="1.5" 
        //                     stroke="currentColor" 
        //                     className="icon">
        //                     <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 
        //                     3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 
        //                     14.998 0A17.933 17.933 0 0 1 12 
        //                     21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
        //                 </svg>
        //             }
        //             clearable={false}
        //             placeholder="Username"
        //             type="text"
        //         />

        //         <InputIconContainer
        //             icon={
        //                 <svg xmlns="http://www.w3.org/2000/svg" 
        //                     viewBox="0 0 24 24" 
        //                     fill="none" 
        //                     strokeWidth="1.5" 
        //                     stroke="currentColor" 
        //                     className="icon">
        //                     <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 5.25a3 3 0 0 1 3 
        //                     3m3 0a6 6 0 0 1-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 
        //                     17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 
        //                     .43-1.563A6 6 0 1 1 21.75 8.25Z" />
        //                 </svg>
        //             }
        //             clearable={false}
        //             placeholder="Password"
        //             type="password"
        //         />

        //         {extraInputs}
        //     </form>

        //     <button className="login-button">{loginButtonText}</button>
        //     <button className="secondary-button" onClick={onToggle}>{registerButtonText}</button>
        // </div>
    );
}

export default LoginPanel;