<script>
  // @ts-nocheck

  import { goto } from "$app/navigation";
  import { basepath } from "$lib/config";
    import { postRequest } from "$lib/req_utils";
  import { onMount } from "svelte";

  let processdata;
  let filetype = "";
  let filestat = false;
  let fileup = "";
  let casename = "";
  let filestat_ind;
  let rendercasedata = [];
  let userDetails = JSON.parse(localStorage.getItem("userDetails"));
  onMount(() => {
    console.log(userDetails.email);
  });

  function getjson() {
    filestat = true;
    processdata = "Processing";
    const fileInput = document.querySelector("#fileupload");

    if (fileInput && fileInput.files.length > 0) {
      let formData = new FormData();
      console.log(fileInput.files);
      for (let i = 0; i < fileInput.files.length; i++) {
        formData.append("files", fileInput.files[i]);
        formData.append("casename", casename);
        formData.append("filetype", filetype);
        formData.append("user", userDetails.email);
      }

      console.log("Sending fetch request...");

      console.log(formData);
      const url = `${basepath()}/getjson`
        postRequest(fetch,url,formData)
        .then((response) => {
          filestat = response;
          filestat = false;
          fileup = "Upload Sucess";
          console.log(filestat);
        })
        .catch((err) => {
          console.log(err);
        });
    }
  }

  function getcasedata() {
    const body = {
        user: userDetails["email"],
        mode: "getcases",
      }
    const url = `${basepath()}/getcasedata`
    postRequest(fetch,url,body)
      .then((data) => {
        console.log(data);
        rendercasedata = data;
      });
  }
  getcasedata();
  // setInterval(getcasedata, 3000)

  let isOpen = false;

  function toggleContent() {
    isOpen = !isOpen;
  }

  function upload_ind(csname,index) {
    console.log("enterd");
    casename = csname;
    filestat_ind = true;
    processdata = "Processing";
    const indfileInput = document.querySelector("#indfile_"+index);
    console.log("que", indfileInput, indfileInput.files.length);
    if (indfileInput && indfileInput.files.length > 0) {
      console.log("in files");
      let formData = new FormData();
      console.log(indfileInput.files);
      for (let i = 0; i < indfileInput.files.length; i++) {
        formData.append("files", indfileInput.files[i]);
        formData.append("casename", casename);
        formData.append("filetype", "towercdr");
        formData.append("user", userDetails.email);
        formData.append("total_files", indfileInput.files.length);
      }

      console.log("Sending fetch request...");

      console.log(formData);
      const url = `${basepath()}/getjson`
      postRequest(fetch,url,formData)
        .then((response) => {
          filestat_ind = response;
          filestat_ind = false;
          // fileup = "Upload Sucess";
          console.log(filestat_ind);
        })
        .catch((err) => {
          console.log(err);
        });
    }
  }
  function updatecase(csnm, csetype) {
    localStorage.setItem("casename", csnm);
    localStorage.setItem("casetype", csetype);
    goto("/analysis/caseanalyst");
    // location.reload()
    // goto("/analysis")
  }
</script>

<main>
  <div class="main">
    <h1 style="margin-top: 1px; font-family: Comic Sans MS">Case Creation</h1>
    <div class="input-container">
      <div class="input-row">
        <!-- Case Name Input -->
        <label for="casename">Case Name</label>
        <input
          type="text"
          id="casename"
          bind:value={casename}
          name="casename"
        />
        <!-- File Type Dropdown -->
        <label for="filetype">File Type</label>
        <select id="filetype" bind:value={filetype} name="filetype">
          <option value="towercdr">Tower Cdr</option>
        </select>
        <!-- File Upload Section -->
        <label for="fileupload">Upload File</label>
        <input
          type="file"
          name="uploadFile"
          id="fileupload"
          multiple
          required
        />
        <button id="searchButton" on:click={getjson}>Upload</button>
        {#if filestat}
          <div class="spinner-border text-success" role="status">
            <span class="sr-only">++</span>
          </div>
        {:else}
          <p class="text-gray-800">Sucess</p>
        {/if}
      </div>
    </div>
  </div>

  <div>

   
    
  </div>
  <table>
    <thead>
      <tr>
        <th>Casename</th>
        <th>Case Type</th>
        <!-- <th>Total Documents</th> -->
        <th>Total Files</th>
        <!-- <th></th> -->
        <th>RFI's</th>
        <th>Action</th>
        <th> Add Files</th>
      </tr>
    </thead>
    <tbody>
      {#each rendercasedata as c_d, i}
        <tr>
          <td>{c_d["casename"]}</td>
          <td>{c_d["casetype"]}</td>
          <!-- <td>{c_d["totalDoc"]}</td> -->
          <td>{c_d['parsed_files']}/{c_d["file_count"]}</td>
          <!-- <td>{c_d["updatetime"]}</td> -->
          <td>
            <button class="btn-danger" on:click={()=>{goto("/notification")}}>
              
              {c_d['rfi']}
            </button>
          </td>
          <td
            ><button
              class="submit"
              on:click={() => updatecase(c_d["casename"], c_d["casetype"])}
            >
              Analyze
            </button></td
          >
          <td class="file-upload-container">
            <input
              type="file"
              name="uploadFile"
              id="indfile_{i}"
              multiple
              required
            />
            <button
              id="searchButton"
              on:click={() => upload_ind(c_d["casename"],i)}
              class="upload-button">Upload</button
            >
          </td>
          {#if filestat_ind && casename === c_d["casename"]}
            <div class="spinner-border text-success" role="status">
              <span class="sr-only">++</span>
            </div>
          {:else if casename === c_d["casename"] }
            <p>sucess</p>
          {/if}
        </tr>
      {/each}
    </tbody>
  </table>
</main>

<style>
  table {
    width: 98%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    margin-top: 2%;
    /* margin-left: 3%; */
    /* box-shadow: 0 9px 10px 0 rgba(0, 0, 0, 0.4); */
    border-radius: 8px;
  }

  th,
  td {
    border: 0.5px black;
    text-align: left;
    text-overflow: ellipsis;
    text-align: center;
    padding: 5px;
  }

  thead th {
    position: sticky;
    top: 0;
    background-color: #3498db;
    border: 1px solid #3498db;
    color: white;
    height: 5vh;
    border: 1px solid #116fad;
    /* height: 15px 10px; */
  }
  tbody tr:hover {
    background-color: rgb(241, 237, 237);
  }
  main {
    margin-left: 60px;
    border: 1px solid #14a2ee;
    /* margin-left: 3%; */
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 50px;
    width: 94.5vw;
  }
  .main {
    /* margin-left: 2%; */
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 20px;
    width: 100%;
  }
  .input-container {
    background-color: #d4ebf7;
    padding: 10px;
    width: calc(100% - 40px);
    box-sizing: border-box;
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    border-radius: 8px;
    height: 7vh;
    /* box-shadow: 0 9px 10px 0 rgba(0, 0, 0, 0.4); */
    margin-top: 50px;
  }
  .input-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
    justify-content: space-between;
    width: 99%;
  }
  .submit {
    padding: 8px 15px;
    background-color: rgb(72, 196, 56);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    display: inline-block;
    /* position: absolute;
        right: 20px;
        top: 20px */
  }
  .file-upload-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    /* justify-content: space-between; */
    /* padding: 0.5em; */
  }

  .upload-button {
    padding: 0.375rem 0.75rem;
    color: #fff;
    background-color: #3498db;
    border: 1px solid #3498db;
    border-radius: 0.25rem;
    cursor: pointer;
  }

  .loading-container {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  #casename {
    width: 20vw;
    height: 4vh;
  }
  #filetype {
    width: 20vw;
    height: 4vh;
  }
  #fileupload {
    width: 20vw;
    height: 4vh;
    background-color: white;
  }
  #searchButton {
    width: 8vw;
    height: 4vh;
    border-radius: 5px;
    background-color: #3498db;
    border: #3498db;
    color: white;
  }
  .dropzone {
        border: 2px dashed #ccc;
        padding: 20px;
        margin: 20px;
        text-align: center;
      }
    
      .dragover {
        background-color: #f0f0f0;
      }
</style>
