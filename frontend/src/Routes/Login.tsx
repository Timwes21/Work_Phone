import { Link } from "react-router-dom";
import useForm from "../hooks/useForm.tsx";


export default function Login(){
    const initialState = {
        username: "",
        password: ""
    }

    const { handleInputChange, login, state } = useForm(initialState);

    console.log(state);
    
    return(
        <div className="page">
            <div className="page-content">
                <div className="auth-body">
                    <h3 className="auth-header">Login</h3>
                    <div className="inputs">

                        <label htmlFor="login-username">Username</label>
                        <input id="login-username" value={state.username} onChange={e=>handleInputChange(e, "username")} type="text" />
                        <label htmlFor="login-password">Password</label>
                        <input id="login-password" value={state.password} onChange={e=>handleInputChange(e, "password")} type="password" />
                    </div>
                    <p>Don't have an account? <Link to='/create-account' className="create-an-account">Create One</Link></p>
                    <button onClick={login} id="create-account-button">Login</button>
                </div>
            </div>
        </div>
    )
}