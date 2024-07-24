
<script>
// @ts-nocheck
//search and style fixed
    import { basepath } from "$lib/config";
    import { createEventDispatcher, afterUpdate } from "svelte";
    import { postRequest } from "$lib/req_utils";
  
  export let propData;
  // export let selectedValues;
  $: selectedValues = propData.selectedValues
  $: startDate = propData.startDate
  $: endDate = propData.endDate
  let final_result = [];
  let columnFilters = {};
  let filteredResults = [];
  let showProgress = false;
  let gotResult = false;
  // let filteredResults = [];

  const dispatch = createEventDispatcher();
  
  
  function handleSubmit() {
    gotResult = false;
    showProgress = true
    console.log(selectedValues)
   
  
    // fetch(`${basepath()}/tower_analysis_2`, {
    //   method: "POST",
    //   body: JSON.stringify({'value':selectedValues,
    //   'mode':'internalcalling',
    //   'fromdate':startDate,
    //   'todate':endDate
    //   }),
    // })

    const url = `${basepath()}/tower_analysis_2`;
    postRequest(fetch,url,JSON.stringify({'value':selectedValues,
      'mode':'internalcalling',
      'fromdate':startDate,
      'todate':endDate
      }))

      .then((res) => res.json())
      .then((data) => {
        if (data.status !== "failure") {
          final_result = data.unique_results_list;
          filteredResults = [...final_result];
          console.log(final_result);
          gotResult = true;
          console.log("show progress", showProgress);
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
    console.log("handle column search",columnFilters[column])
    applyFilters();
  }

  function applyFilters() {
    console.log(columnFilters,"---------applyfilter------------");
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
    console.log(filteredResults,"------------------------------");
  }
  
  afterUpdate(() =>{
  if (selectedValues != propData.selectedValues){
        return
      } else {
      handleSubmit();
      selectedValues = "";
      startDate = "";
      endDate = "";
    }
  });
</script>

{#if showProgress}
<div class="position-absolute top-50 start-50 translate-middle p-5">
  <div class="spinner-border text-primary" role="status">
    <span class="visually-hidden">Loading...</span>
  </div>
</div>
{:else if gotResult}
<div class="table-container">
    <table>
      <thead>
        <tr>
          <th> Target Number </th>
          <th> Destination number </th>
          <th> Incoming </th>
          <th> Outgoing </th>
          <th> call Date </th>
          <th> call time </th>
          <th> sitename </th>
          <th> Cellid </th>
        </tr>
        <tr>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("phone", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("other", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("incoming", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("outgoing", event)}
            />
          </th>
          <th class="search"
            ><input
              class="input input-sm"
              placeholder="Search"
              on:input={(event) => handleColumnSearch("date", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("time", event)}
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
              on:input={(event) => handleColumnSearch("first_cellid", event)}
            />
          </th>
        </tr>
        </thead>
  
  
        <tbody>
          {#each filteredResults as td }
          <tr>
            <td>{td["phone"]}</td>

            <td>{td["other"]}</td>
            <td>{td["incoming"]}</td>
            <td>{td["outgoing"]}</td>
            <td>{td["date"]}</td>
            <td>{td["time"]}</td>
            <td>{td["sitename"]}</td>
            <td>{td["first_cellid"]}</td>
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
  table {
    width: 100%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    /* margin-top: 1%; */
    /* margin-left: 5%; */
  }

  th,
  td {
    border: 0.5px black;
    text-align: left;
    text-overflow: ellipsis;
    text-align: center;
    padding: 5px;
    text-wrap: wrap;
  }

  thead {
    position: sticky;
    top: 0;
    background-color: #5cb2eb;
    border-top: 1px solid #a5c2d5;
    border-right: 1px solid #a5c2d5;
    border-left: 1px solid #a5c2d5;
    border-bottom: 1px solid #5cb2eb;
    color: white;
    text-transform: uppercase;
  }
  tbody td {
    border: 1px solid rgba(0, 0, 0, 0.1);
    word-break: break-word;
  }
  .table-container {
    max-height: 80vh;
    margin-top: 4vh;
    overflow-y: auto;
    overflow-x: auto;
    position: sticky;
    z-index: 1;
    top: 0;
  }
  .search input {
    width: 80%;
    /* border: none; */
    border: 1px solid white;
    border-radius: 5px;
    height: 4vh;
    font-size: 0.8em;
  }

  thead tr {
    border: none;
  }

  tbody tr:hover {
    background-color: #d0e4f1;
  }
  /* a {
    color: black;
  } */
  .no_data {
    color: #161c2057;
    display: flex;
    width: 100%;
    flex-direction: column;
    align-items: center;
    height: 85vh;
    justify-content: center;
  }
  .nodata {
    font-size: 1.2em;
    margin: 0;
  }
  img {
    width: 23%;
  }
  .grid-container {
    width: 100%;
    height: 34vh;
    overflow-y: scroll;
  }

  .grid-container table {
    width: 100%;
    margin: 0;
  }
  .grid-container table tbody tr td {
    background: #d4ebf7;
    border-collapse: separate;
  }
</style>
