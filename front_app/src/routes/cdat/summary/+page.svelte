<script>
  // @ts-nocheck

  import Summarybetweendates from "$lib/Summary/Summarybetweendates.svelte";
  import Summarystatewise from "$lib/Summary/Summarystatewise.svelte";
  import Summarytotal from "$lib/Summary/Summarytotal.svelte";
  import Summarywithstate from "$lib/Summary/Summarywithstate.svelte";
  import Summarywithoutstate from "$lib/Summary/  Summarywithoutstate.svelte";
  import * as XLSX from "xlsx";
  import { writable } from "svelte/store";
  import { get } from "svelte/store";
  import { onMount } from "svelte";
  import { userDetailsStore } from '$lib/datastore.js';



  let number = "";
  let mode = "";
  let result;
  let onResult = "";
  let gotResult = false;
  let startDate = "";
  let endDate = "";
  let state = "";
  let selectedmode = "";
  let isSubmitted = false;
  let dataDownload = [];
  let submissioncount = 0;
  let propData;

  function handlesubmit() {
    propData = {};
    const ele = document.getElementById("display_div");
    isSubmitted = true;
    mode = selectedmode;

    propData["number"] = number;
    propData["startdate"] = startDate;
    propData["enddate"] = endDate;
    propData["state"] = state;

    if (ele) {
      ele.style.display = "block";
    }

    console.log("submitted:", {
      number,
      startDate,
      endDate,
      state,
      selectedmode,
      submissioncount,
    });
  }

  function updateDataForDownload(newData) {
    console.log(number);
    dataDownload = newData["detail"];
  }

  function downloadData() {
    if (Array.isArray(dataDownload) && dataDownload.length > 0) {
      const ws = XLSX.utils.json_to_sheet(dataDownload);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
      // XLSX.writeFile(wb, "data.xlsx");
      XLSX.writeFile(wb, `${number}_${startDate}_${endDate}_${mode}.xlsx`);
    } else {
      console.error("Invalid data format for XLSX export:", dataDownload);
    }
  }
  onMount(() => {});

  let userDetails;
            userDetailsStore.subscribe(value => {
            userDetails = value;
            });
            onMount(() => {
            // beware of truthy and falsy values
            if (localStorage.getItem("userAuth")==="true"){
            userDetailsStore.set(JSON.parse(localStorage.getItem("userDetails")))
            }
            else{
            goto('/');
            }
        });
</script>

<main>
  <div class="input-container">
    <div class=" input-row">
      <select
        name=""
        placeholder="Select Mode"
        id="filter_type"
        bind:value={selectedmode}
      >
        <option value="" disabled>Mode</option>
        <option value="Summarytotal">Summary Total</option>
        <option value="Summarynew">Summary new</option>
        <option value="SummaryStateWise">Summary State Wise</option>
        <option value="SummarywithoutState">Summary Other Than a State</option>
      </select>
      {#if selectedmode === "SummarywithoutState"}
        <input class="input-field" id="mobileNumber" type="text" placeholder=" Enter number" size="7" bind:value={number} style="width:15vw;" />
        <label for="fromDate">From Date:</label>
        <input class="date-input" id="fromDate" type="datetime-local" bind:value={startDate}/>
        <label for="toDate">To Date:</label>
        <input class="date-input" id="toDate" type="datetime-local" bind:value={endDate}/>

        <!-- <label class="input-label" for="state">State</label> -->
        <select name="state" id="state" class="select-state" bind:value={state}>
          <option value="" disabled>State</option>
          <option value="Andhra Pradesh">ANDHRA_PRADESH</option>
          <option value="Andaman and Nicobar Islands"
            >Andaman and Nicobar Islands</option
          >
          <option value="Arunanchal Pradesh">Arunanchal Pradesh</option>
          <option value="Assam">Assam</option>
          <option value="Bihar">Bihar</option>
          <option value="Chandigarh">Chandigarh</option>
          <option value="Chhattisgarh">Chhattisgarh</option>
          <option value="Dadar and Nagar Haveli">Dadar and Nagar Haveli</option>
          <option value="Daman and Diu">Daman and Diu</option>
          <option value="Delhi">Delhi</option>
          <option value="Lakshadweep">Lakshadweep</option>
          <option value="Puducherry">Puducherry</option>
          <option value="Goa">Goa</option>
          <option value="Gujarat">Gujarat</option>
          <option value="Haryana">Haryana</option>
          <option value="Himachal Pradesh">Himachal Pradesh</option>
          <option value="Jammu and Kashmir">Jammu and Kashmir</option>
          <option value="Jharkhand">Jharkhand</option>
          <option value="Karnataka">Karnataka</option>
          <option value="Kerala">Kerala</option>
          <option value="Madhya Pradesh">Madhya Pradesh</option>
          <option value="Maharashtra">Maharashtra</option>
          <option value="Manipur">Manipur</option>
          <option value="Meghalaya">Meghalaya</option>
          <option value="Mizoram">Mizoram</option>
          <option value="Nagaland">Nagaland</option>
          <option value="Odisha">Odisha</option>
          <option value="Punjab">Punjab</option>
          <option value="Rajasthan">Rajasthan</option>
          <option value="Sikkim">Sikkim</option>
          <option value="Tamil Nadu">Tamil Nadu</option>
          <option value="Telangana">Telangana</option>
          <option value="Tripura">Tripura</option>
          <option value="Uttra Pradesh">Uttra Pradesh</option>
          <option value="Uttarakhand">Uttarakhand</option>
          <option value="West Bengal">West Bengal</option>
        </select>
        
      {:else if selectedmode === 'Summarytotal' || selectedmode === 'Summarynew' || selectedmode === 'SummaryStateWise'}
        <input
          class="input-field"
          id="mobileNumber"
          type="text"
          placeholder=" Enter number"
          size="10"
          bind:value={number}
        />

        <label for="fromDate">From Date:</label>
        <input
          class="date-input"
          id="fromDate"
          type="datetime-local"
          bind:value={startDate}
        />

        <label for="toDate">To Date:</label>
        <input
          class="date-input"
          id="toDate"
          type="datetime-local"
          bind:value={endDate}
        />
      {/if}
      <!-- <label class="input-label" for="mobileNumber">Number</label> -->

      <!-- <label class="input-label" for="option">Mode</label> -->

      <button class="submit" on:click={handlesubmit}>Submit</button>
      <button class="download-button" on:click={downloadData}
        ><i class="bi bi-download"></i></button
      >
    </div>
  </div>
</main>

{#if isSubmitted}
  <div class="display_div">
    {#if mode === "Summarytotal"}
      <Summarytotal
        {propData}
        {endDate}
        on:updateData={updateDataForDownload}
      />
    {/if}
    {#if mode === "Summarynew"}
      <Summarybetweendates {propData} on:updateData={updateDataForDownload} />
    {/if}
    {#if mode === "SummaryStateWise"}
      <Summarystatewise
        {propData}
        {endDate}
        on:updateData={updateDataForDownload}
      />
    {/if}
    {#if mode === "SummarywithoutState"}
      <Summarywithoutstate {propData} on:updateData={updateDataForDownload} />
    {/if}
  </div>
{/if}

<style>
  main {
    margin-left: 4%;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 10px;
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
    justify-content: center;
    /* box-shadow: 5px 5px gray; */
  }
  .input-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
    justify-content: space-between;
    width: 100%;
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
    width: 12vw;
  }
  #filter_type {
    margin-right: 10px;
      flex-grow: 1;
      background-color: white;
      border: none;
      font-size: 1.2em;
      color: #296b97;
      height: 4vh;
      border-radius: 3px;
  }

  .select-state {
    height: 4vh;
    border: none;
    color: #296b97;
    background-color: white;
    flex-grow: 1;
    width: 12vw;
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
    padding: 8px 15px;
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
