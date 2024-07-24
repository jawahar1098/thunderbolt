<script>
    // @ts-nocheck
    
        import CdrBetweenDates from "$lib/CallDetails/CDRbetweenDates.svelte";
        import CdrBetweenmultiplePhoneNumber from "$lib/CallDetails/CDRBetweenmultiplePhoneNumber.svelte";
        import Cdripdrgprs from "$lib/CallDetails/CDRIPDRGPRS.svelte";
        import Gprs from "$lib/CallDetails/GPRS.svelte";
        import Imeicdr from "$lib/CallDetails/IMEICDR.svelte";
        import Ipdr from "$lib/CallDetails/IPDR.svelte";
        import MultiplePhoneNumberCdrs from "$lib/CallDetails/MultiplePhoneNumberCDRS.svelte";
        import CommonContactsMulti from "$lib/CallDetails/CommonContactsMulti.svelte";
        import SilentPeriod from "$lib/CallDetails/SilentPeriod.svelte";
        import * as XLSX from "xlsx";
        import { userDetailsStore } from '$lib/datastore.js';
        import { onMount } from "svelte";
    import { goto } from "$app/navigation";


        
    
        let mode ="";
        let number ="";
        let endDate ="";
        let startDate="";
        let number1 ="";
        let number2= "";
        let loopCount= "";
        let dataDownload = [];
        let isSubmitted = false;
        let selectedmode = "";
        let propData;

        function handlesubmit() {
            propData = {}
            isSubmitted = true;
            mode = selectedmode;
            propData['number'] = number
            propData['startdate'] = startDate
            propData['enddate'] = endDate
        }

        function updateDataForDownload(newData) {
            console.log(newData);
            dataDownload = newData['detail'].map(row => {
                Object.keys(row).forEach(key => {
                    if (Array.isArray(row[key])) {
                        row[key] = row[key].join(', '); 
                    }
                });
                return row;
            });
            console.log(dataDownload, 'download values');
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
            <div class="input-row ">
                <label class="input-label" for="mobileNumber"><b>Number</b></label>
                <input class="input-field" id="mobileNumber"  type="text" placeholder=" Enter  Mobile no" size="10" bind:value={number}/>
                <label for="fromDate"><b>From Date:</b></label>
                <input class="date-input" id="fromDate" type="datetime-local" bind:value={startDate} />
    
                <label for="toDate"><b>To Date:</b></label>
                <input class="date-input" id="toDate" type="datetime-local" bind:value={endDate} />
    
                <!-- <label class="input-label" for="option">Mode</label> -->
                <select name="" id="filter_type" bind:value={selectedmode}>
                    <option value="" disabled>Mode</option>
                    <option value="CDRBetweenDates">CDR</option>
                    <option value="MultiplePhoneNumberCDRS">Multiple Phone Number CDR</option>
                    <option value="CDRBetweenmultiplePhoneNumber">CDR Between Multiple Phone Number</option>
                    <option value="IMEICDR">IMEI CDR</option>
                    <!-- <option value="IMEICDR">Multiple IMEI CDR</option> -->
                    <option value="GPRS">GPRS</option>
                    <!-- <option value="IPDR">IPDR</option> -->
                    <option value="CDRIPDRGPRS">CDR-IPDR-GPRS</option>
                    <!-- <option value="CommonCantacts">Common Cantacts</option> -->
                    <!-- <option value="SilentPeriod">Silent Period</option> -->
                    <!-- <option value="CommonContacts">Common contacts</option> -->
                </select>
                <button class="submit" on:click={handlesubmit}>Submit</button>
                <button class="download-button" on:click={downloadData}><i class="bi bi-download"></i></button>
            </div>
        </div>
    </main>
    <div>
        {#if isSubmitted}
            <!-- {#if mode === "CDR"}
                <Cdr {number} on:updateData = {updateDataForDownload}/>
            {/if} -->
            {#if mode === "IPDR"}
            <Ipdr {propData} on:updateData = {updateDataForDownload}/>
            {/if}
            {#if mode === "GPRS"}
            <Gprs {propData}  on:updateData = {updateDataForDownload}/>
            {/if}
            {#if mode === "CDRIPDRGPRS"}
            <Cdripdrgprs {propData} on:updateData = {updateDataForDownload}/>
            {/if}
            {#if mode === "CDRBetweenDates"}
            <CdrBetweenDates {propData} on:updateData = {updateDataForDownload}/>
            {/if}
            {#if mode === "MultiplePhoneNumberCDRS"}
            <MultiplePhoneNumberCdrs {propData} on:updateData = {updateDataForDownload}/>
            {/if}
            {#if mode === "CommonCantacts"}
            <CommonContactsMulti {propData} on:updateData = {updateDataForDownload}/>
            {/if}

            {#if mode === "CDRBetweenmultiplePhoneNumber"}
            <CdrBetweenmultiplePhoneNumber {propData} on:updateData = {updateDataForDownload}/>
            {/if}
            {#if mode === "IMEICDR"}
            <Imeicdr {propData} on:updateData = {updateDataForDownload}/>
            {/if}
            {#if mode === "SilentPeriod"}
            <SilentPeriod {propData} on:updateData = {updateDataForDownload}/>
            {/if}
        {/if}
    </div>
    
    <style>
        main {
            margin-left: 4%;
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 15px;
            /* position: fixed; */
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
            /* width: 98%; */
        }

        label{
            color: #296b97;
        }
        

        .input-field{
            height: 4vh;
            border: none;
            color: #296b97;
            background-color: white;
            flex-grow: 1;
            width: 18vw;
        }
        .date-input{
            height: 4vh;
            border: none;
            color: #296b97;
            background-color: white;
            flex-grow: 1;
            width: 15vw;
        }
        #filter_type {
            /* margin-right: 10px;  */
            height: 4vh;
            border: none;
            color: #296b97;
            background-color: white;
            flex-grow: 1;
            width: 17vw;
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
            /* display: inline-block;    */
            font-size: 16px;
            /* margin: 4px 2px; */
            transition-duration: 0.4s;
            cursor: pointer;
            border: none;
            border-radius: 4px;
            /* position: absolute; */
            /* margin-right: 2px; */
            border-radius: 50%;
        }
    </style>