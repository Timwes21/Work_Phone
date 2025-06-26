import { Link } from "react-router-dom";

export default function CreateAccount(){
    return(
        <div className="page">
            <div className="page-content">
                <div className="auth-body">
                    <h3 className="auth-header">Create Account</h3>
                    <div className="inputs">

                        <label htmlFor="">Username</label>
                        <input type="text" />
                        <label htmlFor="">Password</label>
                        <input type="password" />
                        <label htmlFor="">Twilio Number</label>
                        <input type="text" />
                    </div>
                    <span>Have an account? <Link to='/login' className="create-an-account">Log in</Link></span>
                    <Link to='/twilio-tutorial'>How to get a Twilio Number?</Link>
                    <button id="create-account-button">Create Account</button>

                </div>
            </div>
        </div>    
    )
}