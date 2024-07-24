<script>
    // @ts-nocheck

    import Directcontacts from "$lib/suspecteddb/Directcontacts.svelte";
    import Secondlevelcontacts from "$lib/suspecteddb/Secondlevelcontacts.svelte";
    import { userDetailsStore } from '$lib/datastore.js';
    import * as XLSX from "xlsx";
    import { onMount } from "svelte";

  

  let mode="";
  let number="";
  let dataDownload = [];
  let isSubmitted = false;
  let selectedmode = "";
  let propData;

    function handlesubmit() {
        propData = {}
        isSubmitted = true;
        mode = selectedmode;
        propData['number'] = number
    }

    function updateDataForDownload(newData) {
        console.log(newData)
        dataDownload = newData['detail'];
    }

    const placeholderMap = {
        Directcontacts: "Enter Phone number",
        secondlevelcontacts: "Enter a Number"

    };

    function downloadData() {
        // const data = get(dataDownload);
        if (Array.isArray(dataDownload) && dataDownload.length > 0) {
            const ws = XLSX.utils.json_to_sheet(dataDownload);
            const wb = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
            // let filename = selectedmode ? `${selectedmode}.xlsx` : "data.xlsx";
            XLSX.writeFile(wb, `${number}_${mode}.xlsx`);
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
    <div class="input-container  border-top" >
        <div class="input-row ">
            <div class="input_group">
                <!-- <label class="input-label" for="option">Mode</label> -->
                <select name="" placeholder="Select Mode" id="filter_type" bind:value={selectedmode}>
                    <option value="" disabled>Mode</option>
                    <option value="Directcontacts">Direct Contacts</option>
                    <option value="Secondlevelcontacts">Second Level Contacts</option>
                </select>
            </div>
            <div class="input_group">
                <!-- <label class="input-label" for="mobileNumber">Enter Mobile Number</label> -->
                <input class="input-field" id="mobileNumber" type="text" placeholder={mode ? placeholderMap[mode] : "Enter Number"} size="10" bind:value={number}/>
            </div>
            <button class="submit" on:click={handlesubmit}>Submit</button>
            <button class="download-button" on:click={downloadData}><i class="bi bi-download"></i></button>
        </div>
    </div>  
    <div>
        {#if mode === "Directcontacts"}
        <Directcontacts  {propData} on:updateData = {updateDataForDownload}/>
        {/if}
        {#if mode === "Secondlevelcontacts"}
        <Secondlevelcontacts  {propData} on:updateData = {updateDataForDownload}/>
        {/if}
</div>
</main>

<style>
    main {
      margin-left: 4%;
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-top: 15px;
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
      width: 37vw;
    }
    /* .date-input {
      height: 4vh;
      border: none;
      color: #296b97;
      background-color: white;
      flex-grow: 1;
      width: 15vw;
    } */
    #filter_type {
      /* margin-right: 10px;  */
      height: 4vh;
      border: none;
      color: #296b97;
      background-color: white;
      flex-grow: 1;
      width: 40vw;
    }
  
    /* .select-state{
      height: 4vh;
      border: none;
      color: #296b97;
      background-color: white;
      flex-grow: 1;
      width: 12vw;
  
    } */
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
  