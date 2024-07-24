<script>
  // @ts-nocheck

  import { onMount } from "svelte";
  import Commonnumbers from "$lib/towercdr/Commonnumbers.svelte";
  import Commondest from "$lib/towercdr/Commondest.svelte";
  import Commonimei from "$lib/towercdr/Commonimei.svelte";
  import Sameconvo from "$lib/towercdr/Sameconvo.svelte";
  import Internalcalling from "$lib/towercdr/Internalcalling.svelte";
  import Callsundertower from "$lib/towercdr/Callsundertower.svelte";
  import Numbersummary from "$lib/towercdr/Numbersummary.svelte";
  import Groupofnum from "$lib/towercdr/Groupofnum.svelte";
  import Towerformulaone from "$lib/towercdr/towerformulaone.svelte";
  import Cdrtower from "$lib/towercdr/Cdrtower.svelte";
  import { basepath } from "$lib/config";
  import * as XLSX from "xlsx";

  let lat = "";
  let long = "";
  let radius = "";
  let date = "";
  let time = "";
  let final_result = [];
  let gotResult = false;
  let showDropdown1 = false;
  let showDropdown = false;
  let selectedprovider = [];
  let towerSelection = [];
  let cellIDs = [];
  let provider3 = [];
  let unique_providers = [];
  let show_providers = [];
  let unique_states = [];
  let show_states = [];
  let show_tower = [];
  let cellidSelection = [];
  let SelectedTowerAndCell = [];
  let tabledata = [];
  let selectedValues = [];
  let dataDownload = [];
  let startDate = "";
  let endDate = "";
  let number;
  let propData;

  let mode;
  let showdata;
  let handleClickOutside;

  function closeDropdown() {
    showDropdown1 = false; // Set showDropdown1 to false to close the dropdown
  }

  function handleSubmit() {
    if (lat !== "" && long !== "" && radius !=="" ){

      showDropdown = !showDropdown;
      showDropdown1 = !showDropdown1;

      const towergroup_creation = new FormData();
      towergroup_creation.append("lat", lat);
      towergroup_creation.append("long", long);
      towergroup_creation.append("radius", radius);
      towergroup_creation.append("date", date);
      towergroup_creation.append("time", time);
      towergroup_creation.append("mode", "tower_group_creation");

      

      fetch(`${basepath()}/tower_analysis`, {
        method: "POST",
        body: towergroup_creation,
      })
        .then((res) => res.json())

        .then((data) => {
          final_result = data.response;
          console.log(final_result,"----final result----")
          final_result.forEach((item) => {
            if (!unique_providers.includes(item.provider)) {
              unique_providers.push(item.provider);
            }
            // if (!unique_states.includes(item.state[0])) {
            //   unique_states.push(item.state[0]);
            // }
          });
          show_providers = unique_providers;
          //   show_states = unique_states
          console.log(unique_providers);
          console.log(final_result);
          gotResult = true;
        })
        .catch((err) => {
          console.error("Fetch error:", err);
        });
    }

     

  }

  function getdata() {
    gotResult = false;
    showdata = mode;
    prob();
    gotResult = true;
  }

  onMount(() => {
    window.addEventListener("click", handleClickOutside);

    return () => {
      window.removeEventListener("click", handleClickOutside);
    };
  });

  function createtowerdict(type) {
    console.log(type, "-------");
    const towerExists = selectedValues.findIndex(
      (dict) => dict.towername === type
    );
    if (towerExists !== -1) {
      selectedValues.splice(towerExists, 1);
    } else {
      const newdict = { towername: type, cellid: [] };
      selectedValues = [...selectedValues, newdict];
    }

  }
  function prob(){
    propData = {}
    propData['selectedValues'] = selectedValues
    if (startDate) propData['startDate'] = startDate
    if (endDate) propData['endDate'] = endDate
    if (number) propData['number'] = number
    console.log(propData,"-----in page")
  }

  console.log(selectedValues,"--selected values");

  function addcellids(towername, cellid) {
    console.log(towername, cellid);
    const towerExists = selectedValues.findIndex(
      (dict) => dict.towername === towername
    );
    // console.log(towerExists)
    if (towerExists !== -1) {
      const cell_val = selectedValues[towerExists]["cellid"];
      // console.log(cell_val,"--")
      if (cell_val.length > 0) {
        const del_cell = cell_val.indexOf(cellid);
        if (del_cell !== -1) {
          console.log("exist");
          cell_val.splice(del_cell, 1);
        } else {
          console.log("nonexists added");
          cell_val.push(cellid);
        }
      } else {
        cell_val.push(cellid);
      }
      // const cellidecists = cell_val.some(dict => dict.cellid === cellid);
      // console.log(cellidecists)
      // if(cellidecists !== -1){
      //     cell_val.splice(cellidecists,1)
      // }
      // console.log(selectedValues[towerExists])
      // console.log(cell_val)
      // selectedValues[towerExists].cellid.push(cellid)
    }
    console.log(selectedValues);
  }

  function updateSelectedstates() {
    const statebox = Array.from(
      document.querySelectorAll(".checkstates:checked")
    ).map((checkbox1) => checkbox1.value);
    selectedstates = statebox;
    console.log(selectedstates);
    show_tower = final_result;
  }

  function updateSelectedprovider() {
    const providerbox = Array.from(
      document.querySelectorAll(".checkprovider:checked")
    ).map((checkbox1) => checkbox1.value);
    selectedprovider = providerbox;
    console.log(selectedprovider);
    show_tower = final_result;
  }

  function selectallCheckboxesproviders() {
    const providerallbox = document.querySelectorAll(".checkprovider");
    providerallbox.forEach((checkbox1) => {
      checkbox1.checked = true;
    });
    selectedprovider = providerallbox;
    // showDropdown1 = !showDropdown1;

    console.log(selectedprovider);
  }

  function updateSelectedCounttower(type) {
    const selectedtowerboxes = Array.from(
      document.querySelectorAll(".checktowername:checked")
    ).map((checkbox1) => checkbox1.value);
    towerSelection = selectedtowerboxes;
    console.log(
      towerSelection,
      "///////////////////////////////////////////////////////"
    );
    createtowerdict(type);
  }

  function updateSelectedcellid(towerName, cellIDs) {
    const selectedcellidboxes = Array.from(
      document.querySelectorAll(".checkcellid:checked")
    ).map((checkbox1) => checkbox1.value);
    // cellIDs = selectedcellidboxes;
    addcellids(towerName, cellIDs);
  }

  function selectallTowerboxes2() {
    const checkboxes = document.querySelectorAll(".checktowername");
    checkboxes.forEach((checkbox1) => {
      checkbox1.checked = true;
    });
    const allselectedtowerboxes = Array.from(
      document.querySelectorAll(".checktowername:checked")
    ).map((checkbox1) => checkbox1.value);
    towerSelection = allselectedtowerboxes;
    console.log(towerSelection, towerSelection.length);
    for (let i = 0; i < towerSelection.length; i++) {
      console.log(towerSelection[i]);
      createtowerdict(towerSelection[i]);
    }
    // console.log('Selected Towers:', JSON.stringify(selectedValues, null, 2));
  }

  function selectallCellid() {
    const checkboxes = document.querySelectorAll(".checkcellid");
    cellidSelection = [];
    checkboxes.forEach((checkbox) => {
      checkbox.checked = true;
      cellidSelection.push(checkbox.value);
    });
    console.log(
      "All Cell IDs selected:",
      JSON.stringify(cellidSelection, null, 2)
    );
  }

  function clearCheckboxes() {
    selectedprovider = [];
    // alert("");
    const checkboxes1 = document.querySelectorAll(".clear");

    checkboxes1.forEach((checkbox) => {
      checkbox.checked = false;
    });
  }

  function clearCheckboxes2() {
    towerSelection = [];

    const checkboxes1 = document.querySelectorAll(".clear");
    checkboxes1.forEach((checkbox1) => {
      checkbox1.checked = false;
    });
  }

  function clearCheckboxes3() {
    cellidSelection = [];

    const checkboxes1 = document.querySelectorAll(".clear");
    checkboxes1.forEach((checkbox1) => {
      checkbox1.checked = false;
    });
    // cellidSelection = [];
    console.log(cellidSelection);
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
      XLSX.writeFile(wb, `${mode}.xlsx`);
    } else {
      console.error("Invalid data format for XLSX export:", dataDownload);
    }
  }
</script>

<div class="input_container">
  <input
    type="text"
    id="latitude"
    name="latitude"
    style="width: 10%;"
    placeholder="e.g., 20.77616"
    bind:value={lat}
  />
  <input
    type="text"
    id="longitude"
    name="longitude"
    style="width: 10%;"
    placeholder="e.g., 80.74285"
    bind:value={long}
  />
  <input
    class="input"
    placeholder="Kilometer(radius)"
    style="width: 10%;"
    bind:value={radius}
  />
  <!-- <select class="form-select" id="towerdata" on:change={moveTo}>
    <option selected disabled>Tower</option>
    <option value="towergprs">Tower_GPRS</option>
    <option value="toweripdr">Tower_IPDR</option>
    <option value="towercdr">Tower_CDR</option>
  </select> -->

  <!-- Providers view -->

  <div class="dropdown">
    <input
      type="text"
      class="provider1 form-control"
      placeholder="Provider"
      readonly
      on:click={handleSubmit}
    />
    <div class="inerscroll">
      <div
        class="menu2 dropdown-menu ml-3"
        style="{showDropdown1 ? 'display: block;' : 'display: none;'};"
      >
        <button
          type="button"
          class="clear btn btn-outline-danger ml-1"
          on:click={clearCheckboxes}><i class="bi bi-x-square"></i></button
        >
        <button
          type="button"
          class="clear btn btn-outline-success ml-1"
          on:click={selectallCheckboxesproviders}
          ><i class="bi bi-check2-square"></i></button
        ><br />

        {#each show_providers as item, i}
          <div class="drop">
            <input
              class="checkprovider ml-2"
              type="checkbox"
              bind:value={item}
              id={i}
              on:change={updateSelectedprovider}
            />
            <label for="checkbox{i}">{item}</label><br />
          </div>
        {/each}
      </div>
    </div>
  </div>

  <div class="dropdown">
    <input
      type="text"
      class="provider1 form-control"
      placeholder="towername"
      readonly
      on:click={handleSubmit}
    />
    <div class="inerscroll">
      <div
        class="menu2 dropdown-menu ml-3"
        style="{showDropdown1 ? 'display: block;' : 'display: none;'};"
      >
        <button
          type="button"
          class="clear btn btn-outline-danger ml-1"
          on:click={clearCheckboxes2}><i class="bi bi-x-square"></i></button
        >
        <button
          type="button"
          class="clear btn btn-outline-success ml-1"
          on:click={selectallTowerboxes2}
          ><i class="bi bi-check2-square"></i></button
        ><br />

        {#each show_tower as item, i}
          {#each selectedprovider as pro}
            {#if item["provider"] === "AIRTEL_TOWER" && pro === "AIRTEL_TOWER"}
              <div class="drop">
                <input
                  class="checktowername ml-2"
                  type="checkbox"
                  bind:value={item["towername"]}
                  id={i}
                  on:change={() => {
                    updateSelectedCounttower(item["towername"]);
                  }}
                />
                <label for="checkbox{i}" style="color: red;"
                  >{item["towername"]}</label
                >
              </div>
            {:else if item["provider"] === "VODAFONE" && pro === "VODAFONE"}
              <div class="drop">
                <input
                  class="checktowername ml-2"
                  type="checkbox"
                  bind:value={item["towername"]}
                  id={i}
                  on:change={() => {
                    updateSelectedCounttower(item["towername"]);
                  }}
                />
                <label for="checkbox{i}" style="color: orange;"
                  >{item["towername"]}</label
                >
              </div>
            {:else if item["provider"] === "RJIL" && pro === "RJIL"}
              <div class="drop">
                <input
                  class="checktowername ml-2"
                  type="checkbox"
                  bind:value={item["towername"]}
                  id={i}
                  on:change={() => {
                    updateSelectedCounttower(item["towername"]);
                  }}
                />
                <label for="checkbox{i}" style="color: blue;"
                  >{item["towername"]}</label
                >
              </div>
            {:else if item["provider"] === "CELLONE" && pro === "CELLONE"}
              <div class="drop">
                <input
                  class="checktowername ml-2"
                  type="checkbox"
                  bind:value={item["towername"]}
                  id={i}
                  on:change={() => {
                    updateSelectedCounttower(item["towername"]);
                  }}
                />
                <label for="checkbox{i}" style="color: green;"
                  >{item["towername"]}</label
                >
              </div>
            {:else if item["provider"].toString() === pro}
              <div class="drop">
                <input
                  class="checktowername ml-2"
                  type="checkbox"
                  bind:value={item["towername"]}
                  id={i}
                  on:change={() => {
                    updateSelectedCounttower(item["towername"]);
                  }}
                />
                <label for="checkbox{i}" style="color: purple;"
                  >{item["towername"]}</label
                >
              </div>
            {/if}
          {/each}
        {/each}
      </div>
    </div>
  </div>

  <!--  For Cell id selection based on tower and provider -->

  <div class="dropdown">
    <input
      type="text"
      class="provider1 form-control"
      placeholder="CellIDs"
      readonly
      on:click={handleSubmit}
    />
    <div class="inerscroll">
      <div
        class="menu2 dropdown-menu ml-3"
        style="{showDropdown1 ? 'display: block;' : 'display: none;'};"
      >
        <button
          type="button"
          class="clear btn btn-outline-danger ml-1"
          on:click={clearCheckboxes3}><i class="bi bi-x-square"></i></button
        >
        <button
          type="button"
          class="clear btn btn-outline-success ml-1"
          on:click={selectallCellid}><i class="bi bi-check2-square"></i></button
        >

        {#each final_result as item, i}
          {#if towerSelection.includes(item["towername"]) && selectedprovider.includes(item["provider"])}
            {#each item["cellid"] as cellid}
              {#if item["towername"] && item["provider"] === "AIRTEL_TOWER"}
                <div class="drop">
                  <input
                    class="checkcellid ml-2"
                    type="checkbox"
                    bind:value={cellid}
                    id={i}
                    on:change={() => {
                      updateSelectedcellid(item["towername"], cellid);
                    }}
                  />
                  <label for="checkbox{i}" style="color: red">{cellid}</label>
                </div>
              {:else if item["towername"] && item["provider"] === "RJIL"}
                <div class="drop">
                  <input
                    class="checkcellid ml-2"
                    type="checkbox"
                    bind:value={cellid}
                    id={i}
                    on:change={() => {
                      updateSelectedcellid(item["towername"], cellid);
                    }}
                  />
                  <label for="checkbox{i}" style="color: blue">{cellid}</label>
                </div>
              {:else if item["towername"] && item["provider"] === "VODAFONE"}
                <div class="drop">
                  <input
                    class="checkcellid ml-2"
                    type="checkbox"
                    bind:value={cellid}
                    id={i}
                    on:change={() => {
                      updateSelectedcellid(item["towername"], cellid);
                    }}
                  />
                  <label for="checkbox{i}" style="color: orange">{cellid}</label
                  >
                </div>
              {:else if item["towername"] && item["provider"] === "CELLONE"}
                <div class="drop">
                  <input
                    class="checkcellid ml-2"
                    type="checkbox"
                    bind:value={cellid}
                    id={i}
                    on:change={() => {
                      updateSelectedcellid(item["towername"], cellid);
                    }}
                  />
                  <label for="checkbox{i}" style="color: green">{cellid}</label>
                </div>
              {/if}
            {/each}
          {/if}
        {/each}
      </div>
    </div>
  </div>

  <select class="form-select clown" id="tower_analysis" bind:value={mode} on:click={closeDropdown}>
    <option selected disabled>Tower Cdr Analysis</option>
    <option value="commonnumbersindifferenttower">Target Number</option>
    <option value="otherpartycommon">Destination Number</option>
    <option value="imei">Imei</option>
    <option value="internalcalling">Internal Calling</option>
    <option value="Callsundertower">Calls under tower</option>
    <option value="sameconvo">Same Convo</option>
    <option value="calldetails">call Details</option>
    <option value="summary">Summary</option>
    <option value="groupofnumbers">Group of Numbers</option>
    <option value="formulaone">Formulaone</option>
  </select>
  {#if mode === "formulaone" || mode === "commonnumbersindifferenttower" || mode === "otherpartycommon" || mode === "imei" || mode === "internalcalling" || mode === "Callsundertower" || mode === "sameconvo" || mode === "summary" || mode === "calldetails"}
  <label for="fromDate">From Date:</label>
        <input
          class="date-input"
          style=" width: 10%;"
          id="fromDate"
          type="datetime-local" step="1"
          bind:value={startDate}
        />

        <label for="toDate">To Date:</label>
        <input
          class="date-input"
          style=" width: 10%;"
          id="toDate"
          type="datetime-local" step="1"
          bind:value={endDate}
        />
  {/if}
  {#if mode === "groupofnumbers"}
  <input class="input-field" id="mobileNumber" type="text" placeholder="Mobile no" bind:value={number}/>
  <label for="fromDate">From Date:</label>
  <input
          class="date-input"
          style=" width: 10%;"
          id="fromDate"
          type="datetime-local" step="1"
          bind:value={startDate}
        />

        <label for="toDate">To Date:</label>
        <input
          class="date-input"
          style=" width: 10%;"
          id="toDate"
          type="datetime-local" step="1"
          bind:value={endDate}
        />
  
  {/if}

  <button class="btn-btn-primary" on:click={getdata}>Analyse</button>
  <button class="download-button" on:click={downloadData}><i class="bi bi-download"></i></button>
</div>
<div class="datacom">
  {#if showdata === "commonnumbersindifferenttower"}
    <Commonnumbers {propData} on:updateData={updateDataForDownload} />
  {/if}
  {#if showdata === "otherpartycommon"}
    <Commondest {propData} on:updateData={updateDataForDownload} />
  {/if}
  {#if showdata === "imei"}
    <Commonimei {propData} on:updateData={updateDataForDownload} />
  {/if}

  {#if showdata === "sameconvo"}
    <Sameconvo {propData} on:updateData={updateDataForDownload} />
  {/if}
  {#if showdata === "internalcalling"}
    <Internalcalling {propData} on:updateData={updateDataForDownload} />
  {/if}
  {#if showdata === "Callsundertower"}
    <Callsundertower {propData} on:updateData={updateDataForDownload} />
  {/if}
  {#if showdata === "summary"}
    <Numbersummary {propData} on:updateData={updateDataForDownload} />
  {/if}
  {#if showdata === "calldetails"}
    <Cdrtower {propData} on:updateData={updateDataForDownload} />
  {/if}
  {#if showdata === "groupofnumbers"}
    <Groupofnum {propData} on:updateData={updateDataForDownload} />
  {/if}
  {#if showdata === "formulaone"}
    <Towerformulaone {propData} on:updateData={updateDataForDownload} />
  {/if}

</div>

<style>
  .input_container {
    display: flex;
    align-items: center;
    margin-left: 3%;
    border: 1px solid whitesmoke;
    width: 100%;
    height: 5vh;
    padding-top: 2.5em;
    padding-bottom: 2.5em;
    padding-left: 1em;
    padding-right: 1em;
    border-radius: 4px;
    background-color: #d4ebf7;
    /* color: white; */
    color: #296b97;
    margin-top: 50px;
    gap: 0.5em;
  }
  .datacom{
    margin-left: 10rem;
  }


  .provider1 {
    width: 100%;
    text-wrap: wrap;
    border: 1px solid whitesmoke;
    height: 5vh;
    background-color: white;
    color: #296b97;
  }

  .drop {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 16px;
    margin-left: 7%;
    color: #296b97;
  }

  .drop:hover{
    background-color: #d0e4f1;
  }

  .menu2 {
    background-color: whitesmoke;
    width: 100%;
    height: 400px;
    overflow: scroll;
    color: #296b97;
  }

  .clear {
    width: 40px;
    border-radius: 10px;
    margin-bottom: 5px;
    margin-left: 5px;
    color: #296b97;
  }
  ::placeholder {
  color: #296b97;
  opacity: 1; /* Firefox */
}

::-ms-input-placeholder { /* Edge 12 -18 */
  color: #296b97;
}

  input {
    border: none;
    height: 5vh;
    color: #296b97;
    /* width: 10%; */
    border-radius: 4px;
  }
  .form-select {
    height: 5vh;
    width: 10%;
    color: #296b97;
  }
  button {
    height: 5vh;
    width: 10%;
    background-color: #3498db;
    border: #3498db;
    color: white;
    border-radius: 8px;
  }
  .dropdown {
    /* margin-left: -5em; */
    color: #296b97;
    /* background-color: whitesmoke; */
  }

  /* .clown { */
    /* margin-left: -5em; */
    /* width: 10em;
    color: #296b97;
  } */
  .download-button {
    background-color: #3498db;
    /* padding: 8px 15px; */
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
    width: 5%;
    /* position: absolute;
            right: 20px; */
    border-radius: 45%;
  }
 
</style>