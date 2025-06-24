import Files from "./files"
import MissedCalls from "./missed-calls"

export default function Content(){
    return (
        <div className="page-content">
            <MissedCalls/>
            <Files/>
        </div>
    )
}