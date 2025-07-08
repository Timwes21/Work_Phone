import { useState, useEffect } from "react"
import { fileBase } from "../routes.ts";
import { getToken } from "../token.ts";


export default function Files(){
    const [ fileNames, setFileNames ] = useState<string[]>([]);
    const [ fileAdded, setFileAdded ] = useState<boolean>(false);
    const [ fileExists, setFileExists ] = useState<boolean>(false);
    

    const deleteFile =(fileName: string) => {
        fetch(fileBase+"/delete-file", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({filename: fileName, token: getToken()})
        })
        .then(response=>response.json())
        .then(data=>{
            if (data.file_exists){
                setFileExists(true);
                return;
            }
            setFileExists(false);
            setFileAdded(!fileAdded)
            
        })
    }

    useEffect(()=> {
        fetch(fileBase + "/get-files", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({"token": getToken()})
        })
        .then(response => response.json())
        .then(data=>{
            console.log(data);
            
            data.files && setFileNames(data.files)
        })
    },[fileAdded])

    const showFiles = () => {
        if (fileNames.length < 1) 
            return <p className="no-file-message">Add Files for your call assistant to reference if the caller has questions</p> 
        
        return (
            <div className="file-names">
            {fileNames.map((value, _)=>(
                <div key={value} className="file-name-con">
                    <span className="file-name">{value}</span>
                    <button onClick={()=>deleteFile(value)} id="remove-file">Remove</button>
                </div>
            ))}
        </div>
        )
    }
        
    


    return(
        <div className="files">
            <h3>Files</h3>
            {fileExists && <>File already exists</>}
            <hr />
            <label id="choose-file-label" htmlFor="choose-file">Add File</label>
            <input id="choose-file" type="file" onChange={e=>{
                let currentFile = e.target.files?.[0]
                if (currentFile){
                    const token: string = getToken();
                    const formData = new FormData();
                    formData.append("file", currentFile);
                    formData.append("token", token)
                    
                    fetch(fileBase + "/save-files", {
                        method: "POST",
                        body: formData
                    })
                    .then(()=>setFileAdded(!fileAdded))
                    .catch(err=>console.log("Something went wrong", err))
                }
            }}/>
            {showFiles()}
        </div>
    )
}