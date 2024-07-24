<script>
    import { basepath } from "$lib/config";

let processdata;
let filetype = '';
let res;
let filestat=false;
let fileup = "";
let username = 'test'
let provider;
let options = ['cdr', 'towercdr', 'ipdr', 'zip']
let providers = ['airtel', 'jio', 'vodafone', 'cellone']
    function getjson() {
        filestat = true
        processdata = "Processing";
        const fileInput = document.querySelector('#fileupload') ;
        
        if (fileInput && fileInput.files.length > 0) {
            let formData = new FormData();
            console.log(fileInput.files)
            for (let i = 0; i < fileInput.files.length; i++) {
                formData.append('files', fileInput.files[i]);
                formData.append('usename',username)
                formData.append('filetype',filetype)
                formData.append('provider', provider)
            }      
            
            console.log("Sending fetch request...");
            
            
            console.log(formData)
            fetch(`${basepath()}/zipupload`,{
                method: "post",
                
                body: formData
            })
            .then(res => res.json())
            .then(response => {
                res = response.message
                console.log(filestat)
                if (res === 'sucess'){
                    filestat = false
                    fileup = "Upload Sucess"
                }
            })
            .catch(err => {
                console.log(err)
            })
        }
        
    }
</script>


<main>
    <div class="container">
        <div class="file-upload">
            <!-- File Type Dropdown -->
            <label for="filetype">File Type</label>
            <select id="filetype"  class="file" bind:value={filetype} name="filetype">
                {#each options as o}
                <option value={o}>{o}</option>
                {/each}
            </select>
        
            <!-- File Upload Section -->
            <label for="fileupload">Upload File</label>
            <input type="file" name="uploadFile" id="fileupload" multiple required>
        </div>
        <button id="searchButton" class="upload" on:click={getjson}>Upload</button>
        {#if filestat}
        <div class="file-status">
            <span> file uploading.............</span>
        </div>
            {:else}
            <p>{fileup}</p>
            {/if}
    </div>
</main>
    

<style>
    main {
        margin-left: 4%;
        display: flex;
        flex-direction: row;
        align-items: center;
        margin-top: 30px;
    }
    .container {
        background-color: rgba(198, 216, 207, 0.445);
        padding: 10px;
        width: calc(100% - 40px);
        box-sizing: border-box;
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        border-radius: 8px;
        box-shadow: 0 9px 10px 0 rgba(0, 0, 0, 0.4);
        width: 40%;
        margin-top: 20px;
    }
    .file {
        height: 30px;
    }
    .file-upload {
        margin-top: 10px;
    }
    .upload {
        background-color: rgb(39, 201, 34);
        padding: 8px 15px;
        color: white;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border: none;
        border-radius: 4px;
        position: relative  ;
        right: 20px;
        border-radius: 50px;
    }
    .file-status {
        display: flex;
        align-items: center;
        text-align: center;
        margin-top: 10%;
    }
</style>