import { Link } from "react-router-dom";
import useForm from "../hooks/useForm.tsx";



export default function CreateAccount(){

    const initialState = {
        username: "",
        password: "",
        email: "",
        number: ""
    }

    const {handleInputChange, createAccount, state} = useForm(initialState);    
    

    return(
        <div className="page">
            <div className="page-content">
                <div className="auth-body">
                    <h3 className="auth-header">Create Account</h3>
                    <div className="inputs">

                        <label htmlFor="create-account-username">Username</label>
                        <input id="create-account-username" value={state.username} onChange={e=>handleInputChange(e, "username")} type="text" />
                        <label htmlFor="create-account-password">Password</label>
                        <input id="create-account-password" value={state.password} onChange={e=>handleInputChange(e, "password")} type="text" />
                        <label htmlFor="number">Twilio Number</label>
                        <input id="number" value={"number" in state && state.number} onChange={e=>handleInputChange(e, "number")} type="text" />
                        <label htmlFor="email">Email</label>
                        <input id="email" value={"email" in state && state.email} onChange={e=>handleInputChange(e, "email")} type="text" name=""/>
                    </div>
                    <span>Have an account? <Link to='/login' className="create-an-account">Log in</Link></span>
                    <Link to='/twilio-tutorial'>How to get a Twilio Number?</Link>
                    <button onClick={createAccount} id="create-account-button">Create Account</button>

                </div>
            </div>
        </div>    
    )
}