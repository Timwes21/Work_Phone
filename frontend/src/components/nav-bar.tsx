import { authBase } from "../routes.ts"
import { getToken, setToken } from "../token.ts"
import { useNavigate } from "react-router-dom"

export default function NavBar(){
    const nav = useNavigate()
    const logout = () => {
        fetch(authBase + "/logout", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({token: getToken()})
        })
        .then(response=>response.json())
        .then(data=>{
            setToken("");
            console.log(data.message);
            nav("/login");


        })
        .catch(err=>console.log(err))

    }

    return (
        <header className="nav-bar">
            <h1>Work Phone</h1>
            <button onClick={logout} id="logout-button">Logout</button>
        </header>
    )
}