import Log from "./log"

export default function MissedCalls(){
    return (
        <div className="missed-calls">
            <h2 style={{justifySelf: 'center'}}>Missed Calls</h2>
            <table border={1} className="table">
                <thead className="table-header">
                    <tr>
                        <th>Number</th>
                        <th>Name</th>
                        <th>Callback</th>
                        <th>Message</th>
                    </tr>
                </thead>
                <tbody>
                    <Log/>
                </tbody>
            </table>
        </div>
    )
}