import { Link } from "react-router-dom"

export default function Login(){


    return(
        <div className="page">
            <div className="page-content">
                <div className="auth-body">
                    <h3 className="auth-header">Login</h3>
                    <div className="inputs">

                        <label htmlFor="">Username</label>
                        <input type="text" />
                        <label htmlFor="">Password</label>
                        <input type="password" />
                    </div>
                    <p>Don't have an account? <Link to='/create-account' className="create-an-account">Create One</Link></p>
                    <button id="create-account-button">Login</button>
                </div>
            </div>
        </div>
    )
}