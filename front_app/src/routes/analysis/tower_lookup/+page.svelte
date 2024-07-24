<script>
    // @ts-nocheck
    import Rawdatanumber from "$lib/towerlookup/rawdatanumber.svelte";
    import Imeisummary from "$lib/towerlookup/imeisummary.svelte";
    import * as XLSX from "xlsx";
    import { goto } from "$app/navigation";
  
    let mode = "";
    let number = "";
    let endDate;
    let startDate;
    let dataDownload = [];
    let isSubmitted = false;
    let selectedmode = "";
    let propData;
  
    function checkuser() {
      const token = localStorage.getItem("jwt");
      if (token === null) goto("/");
    }
    checkuser();
  
    function handlesubmit() {
      propData = {};
      isSubmitted = true;
      mode = selectedmode;
      
      propData["number"] = number;
      propData["startdate"] = startDate;
      propData["enddate"] = endDate;
      propData["mode"] = mode;
    }
    console.log(propData,"------probdata")
  
    function updateDataForDownload(newData) {
      console.log(newData);
      dataDownload = newData["detail"].map((row) => {
        Object.keys(row).forEach((key) => {
          if (Array.isArray(row[key])) {
            row[key] = row[key].join(", ");
          }
        });
        return row;
      });
      console.log(dataDownload, "download values");
    }
  
    function downloadData() {
      // const data = get(dataDownload);
      if (Array.isArray(dataDownload) && dataDownload.length > 0) {
        const ws = XLSX.utils.json_to_sheet(dataDownload);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
        XLSX.writeFile(wb, `${number}_${startDate}_${endDate}_${mode}.xlsx`);
      } else {
        console.error("Invalid data format for XLSX export:", dataDownload);
      }
    }
  </script>
  
  <main>
    <div class="input-container">
      <div class="input-row">
        <select name="" id="filter_type" bind:value={selectedmode}>
            <option value="" disabled>Mode</option>
            <option value="source">Phone</option>
            <option value="destination">Other</option>
            <option value="imei">Imei CDR</option>
            <option value="imeisummary">Imei To Phone</option>
            <option value="phonesummary">Phone To Imei</option>
            <!-- <option value="CommonContacts">Common contacts</option> -->
          </select>

        
        <input
          class="input-field"
          id="mobileNumber"
          type="text"
          placeholder=" Enter Number"
          size="10"
          bind:value={number}
        />
         
        {#if selectedmode == "source" || selectedmode == "destination" || selectedmode == "imei"}
        <label for="fromDate"><b>From Date:</b></label>
        <input
          class="date-input"
          id="fromDate"
          type="datetime-local"
          bind:value={startDate}
        />
  
        <label for="toDate"><b>To Date:</b></label>
        <input
          class="date-input"
          id="toDate"
          type="datetime-local"
          bind:value={endDate}
        />
        {/if}
  
        <!-- <label class="input-label" for="option">Mode</label> -->
        
        <button class="submit" on:click={handlesubmit}>Submit</button>
        <button class="download-button" on:click={downloadData}
          ><i class="bi bi-download"></i></button
        >
      </div>
    </div>
  </main>
  <div>
    {#if isSubmitted}
      
      {#if mode === "source" || mode == "destination" || mode === "imei"}
        <Rawdatanumber {propData} on:updateData={updateDataForDownload} />
        {/if}
        {#if mode === "imeisummary" || mode === "phonesummary"}
        <Imeisummary {propData} on:updateData={updateDataForDownload} />
        {/if}
      
      
    {/if}
  </div>
  
  <style>
    main {
      margin-left: 4%;
      display: flex;
      flex-direction: column;
      align-items: center;
      /* margin-top: 0px; */
      /* position: fixed; */
    }
    .input-container {
      background-color: #d4ebf7;
      padding: 10px;
      width: calc(100% - 0px);
      box-sizing: border-box;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      border-radius: 8px;
      height: 7vh;
      justify-content: center;
      /* box-shadow: 5px 5px gray; */
    }
    .input-row {
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
      align-items: center;
      /* justify-content: space-between; */
      /* width: 98%; */
      width: 100;
    }
  
    label {
      color: #296b97;
    }
  
    .input-field {
      height: 4vh;
      border: none;
      color: #296b97;
      background-color: white;
      flex-grow: 1;
      width: 18vw;
    }
    .date-input {
      height: 4vh;
      border: none;
      color: #296b97;
      background-color: white;
      flex-grow: 1;
      width: 15vw;
    }
    .input-field,
  .date-input,
  #filter_type {
    /* margin-right: 10px; */
    flex-grow: 1;
    background-color: white;
    border: none;
    font-size: 1.2em;
    color: #296b97;
    height: 4vh;
    border-radius: 3px;
  }
    .submit {
      padding: 8px 15px;
      background-color: #3498db;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      width: 10vw;
      /* position: absolute;
              right: 20px;
              top: 20px */
    }
    .download-button {
      background-color: #3498db;
      padding: 8px 14px;
      color: white;
      text-align: center;
      text-decoration: none;
      display: inline-block;
      font-size: 16px;
      /* margin: 4px 2px; */
      transition-duration: 0.4s;
      cursor: pointer;
      border: none;
      border-radius: 4px;
      /* position: absolute;
              right: 20px; */
      border-radius: 50%;
    }
  </style>
  