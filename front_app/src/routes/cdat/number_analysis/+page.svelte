<script>
    // @ts-nocheck
  
    import SingleAnalysis from "$lib/numanalysis/single_number_analysis.svelte";
    import MultipleAnalysis from "$lib/numanalysis/multiple_number_analysis.svelte";
    import * as XLSX from "xlsx";
  
  
    let mode = "";
    let number = "";
    let endDate;
    let startDate;
    let dataDownload = [];
    let isSubmitted = false;
    let selectedmode = "";
    let propData;
  
  
    function handlesubmit() {
      propData = {};
      isSubmitted = true;
      mode = selectedmode;
      propData["number"] = number;
      propData["startdate"] = startDate;
      propData["enddate"] = endDate;
    }
  
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
    <div class="header">
      <h1 class="heading">Number Analysis</h1>
    </div>
    <div class="input-container">
      <div class="input-row">
        <input
          class="input-field"
          id="mobileNumber"
          type="text"
          placeholder=" Enter  Mobile no"
          size="10"
          bind:value={number}
        />
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
  
        <button class="submit" on:click={handlesubmit}>Submit</button>
        <button class="download-button" on:click={downloadData}><i class="bi bi-download"></i></button>
      </div>
    </div>
    <div class="data_container">
      {#if isSubmitted}
         {#if propData["number"].split(',').length === 1}
         <SingleAnalysis {propData} on:updateData = {updateDataForDownload}/>
         {:else}
         <MultipleAnalysis {propData} on:updateData = {updateDataForDownload}/>
         {/if}
        
      {/if}
  </div>
  </main>
  
  
  <style>
    .heading {
      color: #296b97;
      text-transform: uppercase;
      font-size: 34px;
    }
    .header {
      width: 100%;
      height: 5vh;
    }
    main {
      margin-left: 5%;
      margin-top: 15px;
      height: 92vh;
      width: 100%;
      position: fixed;
    }
    .input-container {
      background-color: #d4ebf7;
      padding: 10px;
      width: calc(100% - 8em);
      box-sizing: border-box;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      border-radius: 8px;
      height: 7vh;
      justify-content: center;
    }
    .input-row {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      justify-content: space-between;
      /* width: 98%; */
    }
  
    label {
      color: #296b97;
    }
  
    .input-field {
      height: 5vh;
      border: none;
      color: #296b97;
      background-color: white;
      flex-grow: 1;
      width: 30vw;
      border-radius: 5px;
    }
    .date-input {
      height: 5vh;
      border: none;
      color: #296b97;
      background-color: white;
      flex-grow: 1;
      width: 16vw;
      border-radius: 5px;
    }
  
    .submit {
      padding: 8px 15px;
      background-color: #3498db;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      width: 10vw;
    }
    .download-button {
      background-color: #3498db;
      padding: 8px 15px;
      color: white;
      text-align: center;
      text-decoration: none;
      display: inline-block;
      font-size: 16px;
      transition-duration: 0.4s;
      cursor: pointer;
      border: none;
      border-radius: 4px;
      border-radius: 50%;
    }
    .data_container{
      width: 100%;
      height: 100%;
    }
  </style>