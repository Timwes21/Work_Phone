import { useEffect, useState } from "react"
import { authBase } from "../routes";
import { getToken } from "../token";

type UserSetings = {
    realNumber: string,
    name: string
    twilioNumber: string
}

export default function Settings(){
    const settingsSkeleton = {
        realNumber: "",
        name: "",
        twilioNumber: ""
    }
    const [ settings, setSettings ] = useState<UserSetings>(settingsSkeleton);
    const [ settingsCopy, setSettingsCopy ] = useState<UserSetings>(settingsSkeleton)
    const [ isEditing, setIsEditing ] = useState<boolean>(false)
    const [ triggerReload, setTriggerReload ] = useState<boolean>(false)

    useEffect(()=> {
        fetch(authBase + "/user-settings", {
            headers: {"token": getToken()},
        })
        .then(response=>{
            if (response.status === 200){
                return response.json();
            }
        })
        .then(data=>{
            console.log(data);
            
            const {name, real_number, twilio_number} = data;
            const fetchedSettings = {
                name: name,
                realNumber: real_number,
                twilioNumber: twilio_number
            }
            setSettings(fetchedSettings);
            setSettingsCopy(fetchedSettings);
        })
    }, [triggerReload])

    const onChangeSettings = (setting: keyof UserSetings, value: string) => {
        setSettings(prev=>({
            ...prev,
            [setting]: value
        }))
    }

    const userSettings = (
        <>
            <div className="settings-content">
                <span>{settings?.name}</span>
                <span>{settings?.realNumber}</span>
                <span>{settings?.twilioNumber}</span>
            </div>
            <button className="edit-button" onClick={()=>setIsEditing(true)}>Edit</button>
        </>
    )

    const changeSettings = () => {
        const changed = {}

        Object.entries(settings).map(([key, value])=>{
            if (value !== settingsCopy[key]){
                
                changed[key] = value;
            }
        })
        
        if (Object.keys(changed).length === 0){
            return;
        }
        fetch(authBase + "/change-user-settings",{
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "token": getToken()
            },
            body: JSON.stringify({changed: changed})
        })
        .then(response=>{
            if (response.status == 200){
                return response.json()
            }
        })
        .then(()=>{
            setIsEditing(false);
            setTriggerReload(!triggerReload);
            
        })
    }

    const edittingUserSettings  = (
        <>
            <div className="settings-content">
                <input type="text" value={settings?.name} onChange={e=>onChangeSettings("name", e.target.value)}/>
                <input type="text" value={settings?.realNumber} onChange={e=>onChangeSettings("realNumber", e.target.value)}/>
                <input type="text" value={settings?.twilioNumber} onChange={e=>onChangeSettings("twilioNumber", e.target.value)}/>
            </div>
            <button className="edit-button" onClick={changeSettings}>Save</button>
            <button className="edit-button" onClick={()=>setIsEditing(false)}>Cancel</button>
        </>
    )

    return(
        <div className="settings">
            <div className="settings-label">
                <span><b>Name:</b> </span>
                <span><b>Number to Route To:</b> </span>
                <span><b>Twilio Number:</b> </span>
            </div>
            {isEditing ? edittingUserSettings: userSettings}
        </div>
    )
}