import { useState } from "react"
import { base } from "../routes";
import { StringDecoder } from "string_decoder";


export default function Files(){
    const [files, setFiles ] = useState<any[]>([]);
    const [file, setFile] = useState<File| null>();
    


    const addFiles = async() => {
        console.log(file);
        if (file){
            const formData = new FormData()
            formData.append("file", file)
            
            
            
            
            fetch(base + "/save-files", {
                method: "POST",
                body: formData
            })
            .then(async(data)=>console.log(await data.json()))
            .catch(err=>console.log("Something went wrong", err))
        }
    }



    return(
        <div className="files">
            <h3>Files</h3>
            <hr />
            <input type="file" onChange={e=>{
                let currentFile = e.target.files?.[0]
                if (currentFile){
                    setFile(e.target.files?.[0])
                }
                else{
                    setFile(null)
                }

            }}/>
            {file && <button onClick={addFiles}>Add Files</button>}
            {file && <p className="no-file-message">Add Files for your call agent to reference if the caller has questions</p>}
        </div>
    )
}