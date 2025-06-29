import Files from "./files"
import Logs from "./logs"
export default function Content(){
    return (
        <div className="page-content">
            <Logs/>
            <Files/>
        </div>
    )
}