<script>
  // @ts-nocheck

  import { onMount } from "svelte";
  import { basepath } from "$lib/config";
  import { createEventDispatcher, afterUpdate } from "svelte";
  import { postRequest } from "$lib/req_utils";
  export let propData;
  // export let selectedValues;
  $: selectedValues = propData.selectedValues;
  $: startDate = propData.startDate;
  $: endDate = propData.endDate;
  $: number = propData.number;
  let data = [];
  let final_result = [];
  let filteredResults = [];
  let columnFilters = [];
  let gotResult = false;
  let showProgress = true;
  console.log(propData);
  const dispatch = createEventDispatcher();

  function handleSubmit() {
    gotResult = false;
    showProgress = true;
    console.log(selectedValues);

    // fetch(`${basepath()}/tower_analysis_2`, {
    //   method: "POST",
    //   body: JSON.stringify({
    //     numbers: number,
    //     value: selectedValues,
    //     mode: "groupofnumbers",
    //     fromdate: startDate,
    //     todate: endDate,
    //   }),
    // })

    const url = `${basepath()}/tower_analysis_2`;
    postRequest(fetch,url,JSON.stringify({
        numbers: number,
        value: selectedValues,
        mode: "groupofnumbers",
        fromdate: startDate,
        todate: endDate,
      }))
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "success") {
          final_result = data.result_dict;
          filteredResults = [...final_result];
          console.log(final_result);
          gotResult = true;
          dispatch("updateData", filteredResults);
        } else {
          gotResult = false;
        }
      })
      .catch((err) => {
        console.error("Fetch error:", err);
      })
      .finally(() => {
        showProgress = false;
      });
  }

  function handleColumnSearch(column, event) {
    const filterValue = event.target.value.trim().toLowerCase();
    columnFilters[column] = filterValue;
    console.log("handle column search", columnFilters[column]);
    applyFilters();
  }

  function applyFilters() {
    console.log(columnFilters, "---------applyfilter------------");
    const filteredData = final_result.filter((item) => {
      for (const field in columnFilters) {
        const filterValue = columnFilters[field];
        // console.log(filterValue,"----------------------------");
        if (
          filterValue &&
          !item[field].toString().toLowerCase().includes(filterValue)
        ) {
          return false;
        }
      }
      return true;
    });
    filteredResults = filteredData;
    console.log(filteredResults, "------------------------------");
  }
  
  afterUpdate(() =>{
    if (selectedValues != propData.selectedValues || number != propData.number){
          return
        } else {
        handleSubmit();
          selectedValues = ""
          startDate = ""
          endDate = "" 
          number = "" 
        }
  })
  
</script>

{#if showProgress}
<div class="position-absolute top-50 start-50 translate-middle p-5">
  <div class="spinner-border text-primary" role="status">
    <span class="visually-hidden">Loading...</span>
  </div>
</div>
  {:else if gotResult}
    <div class="table-container">
     
        <table
        >
          <thead>
            <tr> <th>Available Phone Numbers</th>
              <th>Not Available Phone Numbers </th>
              <th> sitename </th>
              <th> Cellids </th>
            </tr>
            <tr>
              <th class="search">
                <input
                  placeholder="search"
                  on:input={(event) =>
                    handleColumnSearch("Available_Phone_Numbers", event)}
                />
              </th>
              <th class="search">
                <input
                  placeholder="search"
                  on:input={(event) =>
                    handleColumnSearch("Not_Available_Phone_Numbers", event)}
                />
              </th>
              <th class="search">
                <input
                  placeholder="search"
                  on:input={(event) => handleColumnSearch("sitename", event)}
                />
              </th>
              <th class="search">
                <input
                  placeholder="search"
                  on:input={(event) => handleColumnSearch("Cellids", event)}
                />
              </th>
            </tr>
          </thead>

          <tbody>
            {#each filteredResults as td}
              <tr>
                <td
                  class="border-r px-6 py-4 font-medium text-ellipsis dark:border-neutral-500"
                  >{td["Available_Phone_Numbers"]}</td
                >

                <td
                  class="border-r px-6 py-4 font-medium text-ellipsis dark:border-neutral-500"
                  >{td["Not_Available_Phone_Numbers"]}</td
                >
                <td
                  class="border-r px-6 py-4 font-medium text-ellipsis dark:border-neutral-500"
                  >{td["sitename"]}</td
                >
                <td
                  class="border-r px-6 py-4 font-medium text-ellipsis dark:border-neutral-500"
                  >{td["Cellids"]}</td
                >
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
   
   
  {:else}
    <div class="no_data">
      <img src="/nodata.png" alt="" />
      <p class="nodata">No data Matched in Data Base!!!!!!!!</p>
    </div>
  {/if}

<style>
  .table-container {
    margin-top: 2%;
    margin-bottom: 2%;
    margin-left: 2%;
    margin-right: 2%;
    overflow-x: auto;
    max-height: 700px;
    position: relative;
  }

  table {
    width: 100%;
    table-layout: fixed;
    border-color: rgb(40, 34, 126);
    text-align: center;
  }

  th,
  td {
    border: 1px solid black;
    padding: 8px;
    text-align: left;
    text-wrap: wrap;
    word-wrap: break-word;
    overflow-wrap: break-word;
    text-overflow: ellipsis;
    padding-top: 10px;
    padding-bottom: 20px;
    padding-left: 30px;
    padding-right: 40px;
  }

  th {
    background-color: #000000;
    color: white;
    text-align: center;
    position: sticky;
    top: 0;
    z-index: 1;
  }
  table,
  th,
  td {
    border: 1px solid black;
    border-collapse: collapse;
  }
  .search input {
    width: 80%;
    /* border: none; */
    border: 1px solid white;
    border-radius: 5px;
    height: 4vh;
    font-size: 0.8em;
  }

  .nodata {
    font-size: 1.2em;
    margin: 0;
  }

  .no_data {
    color: #161c2057;
    display: flex;
    width: 100%;
    flex-direction: column;
    align-items: center;
    height: 85vh;
    justify-content: center;
  }
</style>
