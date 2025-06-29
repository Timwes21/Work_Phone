import { useState } from "react"

export default function Logs(){
    const [ logs, setLogs ] = useState();
    return (
        <div className="missed-calls">
            <div className="log">
                <span>7726210972</span>
                <p>this is about something that requires alot</p>
            </div>
            <div className="log">
                <span>7726210972</span>
                <p>This i salso something but i think i like food</p>
            </div>
        </div>
    )
}