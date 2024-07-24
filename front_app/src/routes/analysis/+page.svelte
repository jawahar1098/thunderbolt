<script>
  import NameSearch from "$lib/analysis/nameSearch.svelte";
  import NumberSearch from "$lib/analysis/numberSearch.svelte";
  import AddressSearch from "$lib/analysis/addressSearch.svelte";
  import DateTarget from "$lib/analysis/dateTarget.svelte";
  import RoamingDetails from "$lib/analysis/roamingDetails.svelte";
  import Activeperiod from "$lib/analysis/activeperiod.svelte";
  import Rechargehistory from "$lib/analysis/rechargehistory.svelte";
  import * as XLSX from "xlsx";
  import { writable } from "svelte/store";
  import { get } from "svelte/store";

  let number;
  let sitename;
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

  function handlesubmit() {
    mode = selectedmode;
    isSubmitted = true;
  }

  function updateDataForDownload(newData) {
    console.log(newData);
    dataDownload = newData["detail"];
  }

  function downloadData() {
    // const data = get(dataDownload);
    if (Array.isArray(dataDownload) && dataDownload.length > 0) {
      const ws = XLSX.utils.json_to_sheet(dataDownload);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
      XLSX.writeFile(wb, "data.xlsx");
    } else {
      console.error("Invalid data format for XLSX export:", dataDownload);
    }
  }
</script>

<main>
  <div class="input-container">
    <div class="input-row">
      <label class=" input-label" for="mobileNumber">Enter Number</label>
      <input
        class="input-field"
        id="mobileNumber"
        type="text"
        placeholder=" Enter  Mobile no"
        size="10"
        bind:value={number}
      />
      <label class=" input-label" for="mobileNumber">Enter Name</label>
      <input
        class="input-field"
        id="mobileNumber"
        type="text"
        placeholder=" Enter Name"
        size="10"
        bind:value={name}
      />
      <label class=" input-label" for="mobileNumber">Enter Address</label>
      <input
        class="input-field"
        id="mobileNumber"
        type="text"
        placeholder=" Enter Address"
        size="10"
        bind:value={address}
      />
      <label for="fromDate" class="front-blod">From Date:</label>
      <input
        class="date-input"
        id="fromDate"
        type="date"
        bind:value={startDate}
      />
      <label for="toDate" class="front-blod">To Date:</label>
      <input class="date-input" id="toDate" type="date" bind:value={endDate} />
      <label class="input-label" for="option">Mode</label>
      <select name="" id="filter_type" bind:value={selectedmode}>
        <option value="NameSearch">Name Search</option>
        <option value="NumberSearch">Number Search</option>
        <option value="AddressSearch">Address Search</option>
        <option value="DateTarget">Date Target</option>
        <option value="RoamingDetails">Roaming Details</option>
        <option value="Activeperiod">Active Period</option>
        <option value="RechargeHistory">Rechargehistory</option>
      </select>
      <button class="submit" on:click={handlesubmit}>Submit</button>
      <button class="download-button" on:click={downloadData}
        ><i class="bi bi-download"></i></button
      >
    </div>
    <div></div>
  </div>
</main>

<div>
  {#if isSubmitted}
    {#if mode === "NameSearch"}
      <NameSearch {name} on:updateData={updateDataForDownload} />
    {/if}
    {#if mode === "NumberSearch"}
      <NumberSearch
        {number}
        {startDate}
        {endDate}
        on:updateData={updateDataForDownload}
      />
    {/if}
    {#if mode === "AddressSearch"}
      <AddressSearch {address} on:updateData={updateDataForDownload} />
    {/if}
    {#if mode === "DateTarget"}
      <DateTarget {number} on:updateData={updateDataForDownload} />
    {/if}
    {#if mode === "RoamingDetails"}
      <RoamingDetails
        {number}
        {startDate}
        {endDate}
        on:updateData={updateDataForDownload}
      />
    {/if}
    {#if mode === "Activeperiod"}
      <Activeperiod {number} on:updateData={updateDataForDownload} />
    {/if}
    {#if mode === "RechargeHistory"}
      <Rechargehistory {number} on:updateData={updateDataForDownload} />
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
    margin-left: 3%;
  }
  .input-container {
    background-color: whitesmoke;
    padding: 10px;
    width: 95vw;
    box-sizing: border-box;
    display: flex;
    flex-wrap: wrap;
    gap: 1px;
    border-radius: 8px;
    box-shadow: 5px 5px gray;
    margin-left: 3%;
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
    /* position: absolute;
        right: 20px;
        top: 20px */
  }
  .download-button {
    background-color: darkcyan;
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
