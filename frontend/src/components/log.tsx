import { useState, useEffect } from "react"


interface CallBack {
    day_of_week: string,
    date: string
}


interface CallLogs{
    name: string, 
    caller_id: string, 
    message: string | null, 
    callback: CallBack | null 
}


export default function Log(){
    const [missedCallLogs, setMissedCallLogs ] = useState<CallLogs[]>();

    useEffect(()=> {
        fetch("http://127.0.0.1:3000/missed-call-logs")
        .then(response=>response.json())
        .then(data=>{
            console.log(data);
            
            setMissedCallLogs(data);

        })
    }, [setMissedCallLogs])


    return(
        <>
            {missedCallLogs && missedCallLogs.map(callLog=>{                
                const {name, caller_id, message, callback} = callLog;
                return (
                    <tr key={name}>
                        <td>{caller_id}</td>
                        <td>{name}</td>
                        <td>{callback?.date}, {callback?.day_of_week}</td>
                        <td>{message}</td>
                    </tr>
                )
            })}
        </>
    )
}