<script>
  // @ts-nocheck
  import NameSearch from "$lib/analysis/nameSearch.svelte";
  import NumberSearch from "$lib/analysis/numberSearch.svelte";
  import AddressSearch from "$lib/analysis/addressSearch.svelte";
  import DateTarget from "$lib/analysis/dateTarget.svelte";
  import RoamingDetails from "$lib/analysis/roamingDetails.svelte";
  import Activeperiod from "$lib/analysis/activeperiod.svelte";
  import Rechargehistory from "$lib/analysis/rechargehistory.svelte";
  import * as XLSX from "xlsx";
  import Smpoa from "$lib/analysis/smpoa.svelte";
  import AlternateNumber from "$lib/analysis/alternateNumber.svelte";

  let number;
  let startDate = "";
  let endDate = "";
  let name;
  let address;

  let mode = "";
  let showdata = false;
  let gotResult = false;
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
    propData["name"] = name;
    propData["address"] = address;
  }

  function updateDataForDownload(newData) {
    console.log(newData);
    dataDownload = newData["detail"];
    console.log(dataDownload, "download values");
  }

  // function updateDataForDownload(newData) {
  //     console.log(newData);
  //     dataDownload = newData['detail'].map(row => {

  //         Object.keys(row).forEach(key => {
  //             if (Array.isArray(row[key])) {
  //                 row[key] = row[key].length;
  //             }
  //         });
  //         return row;
  //     });
  //     console.log(dataDownload, 'download values');
  // }

  function downloadData() {
    // const data = get(dataDownload);
    if (Array.isArray(dataDownload) && dataDownload.length > 0) {
      const ws = XLSX.utils.json_to_sheet(dataDownload);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
      if (mode === "NameSearch") {
        XLSX.writeFile(wb, `${name}_${mode}.xlsx`);
      } else if (
        mode === "NumberSearch" ||
        mode === "RoamingDetails" ||
        mode === "RechargeHistory" ||
        mode === "sm_poa" ||
        mode === "alternate_number"
      ) {
        XLSX.writeFile(wb, `${number}_${startDate}_${endDate}_${mode}.xlsx`);
      } else if (mode === "AddressSearch") {
        XLSX.writeFile(wb, `${address}_${mode}.xlsx`);
      } else if (mode === "DateTarget" || mode === "Activeperiod") {
        XLSX.writeFile(wb, `${number}_${mode}.xlsx`);
      }
    } else {
      console.error("Invalid data format for XLSX export:", dataDownload);
    }
  }

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
    <div class="input-row">
      <!-- <label class="input-label" for="option">Mode</label> -->
      <select name="" id="filter_type" bind:value={selectedmode}>
        <option value="" disabled>Mode</option>
        <option value="NameSearch">Name Search</option>
        <option value="NumberSearch">Number Search</option>
        <option value="AddressSearch">Address Search</option>
        <option value="DateTarget">Date Target</option>
        <option value="RoamingDetails">Roaming Details</option>
        <option value="Activeperiod">Active Period</option>
        <option value="RechargeHistory">RechargeHistory</option>
        <option value="sm_poa">SMPOA</option>
        <option value="alternate_number">Alternate Number</option>
      </select>
      {#if selectedmode === "NameSearch"}
        <input
          class="input-field"
          type="text"
          placeholder="Enter Name"
          bind:value={name}
        />
      {:else if selectedmode === "NumberSearch"}
        <input
          class="input-field"
          type="text"
          placeholder="Enter Number"
          bind:value={number}
        />
        <input
          class="input-field"
          type="date"
          placeholder="Enter StartDate"
          bind:value={startDate}
        />
        <input
          class="input-field"
          type="date"
          placeholder="Enter EndDate"
          bind:value={endDate}
        />
      {:else if selectedmode === "AddressSearch"}
        <input
          class="input-field"
          type="text"
          placeholder="Enter Address"
          bind:value={address}
        />
      {:else if selectedmode === "DateTarget"}
        <input
          class="input-field"
          type="text"
          placeholder="Enter Number"
          bind:value={number}
        />
      {:else if selectedmode === "RoamingDetails"}
        <input
          class="input-field"
          type="text"
          placeholder="Enter Number"
          bind:value={number}
        />
        <input
          class="input-field"
          type="date"
          placeholder="Enter StartDate"
          bind:value={startDate}
        />
        <input
          class="input-field"
          type="date"
          placeholder="Enter EndDate"
          bind:value={endDate}
        />
      {:else if selectedmode === "Activeperiod"}
        <input
          class="input-field"
          type="text"
          placeholder="Enter Number"
          bind:value={number}
        />
      {:else if selectedmode === "RechargeHistory"}
        <input
          class="input-field"
          type="text"
          placeholder="Enter Number"
          bind:value={number}
        />
        <input
          class="input-field"
          type="date"
          placeholder="Enter StartDate"
          bind:value={startDate}
        />
        <input
          class="input-field"
          type="date"
          placeholder="Enter EndDate"
          bind:value={endDate}
        />
      {:else if selectedmode === "sm_poa"}
        <input
          class="input-field"
          type="text"
          placeholder="Enter Number"
          bind:value={number}
        />
        <input
          class="input-field"
          type="date"
          placeholder="Enter StartDate"
          bind:value={startDate}
        />
        <input
          class="input-field"
          type="date"
          placeholder="Enter EndDate"
          bind:value={endDate}
        />
      {:else if selectedmode === "alternate_number"}
        <input
          class="input-field"
          type="text"
          placeholder="Enter Number"
          bind:value={number}
        />
        <input
          class="input-field"
          type="date"
          placeholder="Enter StartDate"
          bind:value={startDate}
        />
        <input
          class="input-field"
          type="date"
          placeholder="Enter EndDate"
          bind:value={endDate}
        />
      {/if}

      <button class="submit" on:click={handlesubmit}>Submit</button>
      <button class="download-button" on:click={downloadData}
        ><i class="bi bi-download"></i></button
      >
      <div></div>
    </div>
  </div>
</main>

<div style="width:100%;">
  {#if isSubmitted}
    {#if mode === "NameSearch"}
      <NameSearch {propData} on:updateData={updateDataForDownload} />
    {/if}
    {#if mode === "NumberSearch"}
      <NumberSearch {propData} on:updateData={updateDataForDownload} />
    {/if}
    {#if mode === "AddressSearch"}
      <AddressSearch {propData} on:updateData={updateDataForDownload} />
    {/if}
    {#if mode === "DateTarget"}
      <DateTarget {propData} on:updateData={updateDataForDownload} />
    {/if}
    {#if mode === "RoamingDetails"}
      <RoamingDetails {propData} on:updateData={updateDataForDownload} />
    {/if}
    {#if mode === "Activeperiod"}
      <Activeperiod {propData} on:updateData={updateDataForDownload} />
    {/if}
    {#if mode === "RechargeHistory"}
      <Rechargehistory {propData} on:updateData={updateDataForDownload} />
    {/if}
    {#if mode === "sm_poa"}
      <Smpoa {propData} on:updateData={updateDataForDownload} />
    {/if}
    {#if mode === "alternate_number"}
      <AlternateNumber {propData} on:updateData={updateDataForDownload} />
    {/if}
  {/if}
</div>

<style>
  main {
    /* margin-left: 4%; */
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 50px;
    /* margin-left: %; */
  }
  .input-container {
    background-color: #d4ebf7;
    padding: 10px;
    width: 94vw;
    box-sizing: border-box;
    display: flex;
    flex-wrap: wrap;
    gap: 1px;
    border-radius: 8px;
    /* box-shadow: 5px 5px gray; */
    margin-left: 4%;
    margin-top: 1%;
    /* margin-left: -23%; */
  }
  .input-row {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    align-items: center;
    /* justify-content: flex-start; */
    width: 100%;
  }

  .input-label {
    white-space: nowrap;
    margin-right: 10px;
    /* margin-bottom: 5px;
          font-weight: bold;
          color: #333; */
  }
  .input-field,
  .date-input,
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

  .submit,
  .download-button {
    flex-grow: 0;
  }
  .submit {
    padding: 8px 15px;
    background-color: rgb(72, 196, 56);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-left: auto;
    background-color: #3498db;
    border: #3498db;
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
    margin: 4px 2px;
    transition-duration: 0.4s;
    cursor: pointer;
    border: none;
    border-radius: 4px;
    position: relative;
    right: 2px;
    border-radius: 50%;
    margin-left: 10px;
  }
</style>
