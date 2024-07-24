<script>
    import DateTarget from "$lib/analysis/dateTarget.svelte";
    import { basepath } from "$lib/config";
    import {afterUpdate} from "svelte";

  
  
  export let propData;
  $: number = propData.number;
  let showtable = false;
  let gotResult = false;
  let tabledata;
  let tabledata1;
  let showProgress = false;
  let datafound  = 'Not Data Yet'
  
  
  
  
  function searchNumber(){
  showProgress = true;
  const number_s = new FormData()
  number_s.append('number', number)
  fetch(`${basepath()}/numberserach`, {
    method : 'post',
    body: number_s
  })
  .then(res => res.json())
  .then(data => {
    console.log(data);
    tabledata = data.table;
    tabledata1 = data.table1;
    showProgress = false;
    // console.log(tabledata )
    showtable = true;
    console.log(showtable)
  })
  .catch(error => {
    console.error('Error:', error)
    showtable = false;
  });
  }
  afterUpdate(()=> {
    console.log("updated---------,",propData)
    if(number != propData.number){
    return
    }
    else{
      searchNumber()
      number =""
    }
  })
  // searchNumber()
</script>
  
  
<main>
  <h1 style="background-color: #3498db;">VIGOR</h1>
  <!-- <input type="text" bind:value={number}><button on:click={searchNumber}>Submit</button> -->
    {#if showtable}
    <div class="flex justify-center mt-3">
      <h4 style="margin-top: 1%; text-align:center; font-family:Verdana, Geneva, Tahoma, sans-serif">Data of {propData.number}</h4>
    </div>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>B-Party</th>
            <th>CellId_A</th>
            <th>Imei-A</th>
            <th>Imei-B</th>
            <th>Imsi-A</th>
            <th>Imsi-B</th>
            <th>Latitude</th>
            <th>Longitude</th>
          </tr>
        </thead>
        <tbody>
        {#if Array.isArray(tabledata) && tabledata.length > 0}
        {#each tabledata as tblD}
          <tr>
            <td>{tblD["B-party"]}</td>
            <td>{tblD["Cellid_A"]}</td>
            <td>{tblD["Imei-A"]}</td>
            <td>{tblD["Imei-B"]}</td>
            <td>{tblD["Imsi-A"]}</td>
            <td>{tblD["Imsi-B"]}</td>
            <td>{tblD["Lat"]}</td>
            <td>{tblD["Long"]}</td>
          </tr>
        {/each}
        {:else}
            <tr>
              <td colspan="8">No data available for tabledata.</td>
            </tr>
          {/if}
        </tbody>
      </table>
    </div>
    <div class="table-container1">
      <table>
        <thead>
          <tr>
            <th>City</th>
            <th>Company</th>
            <th>Country</th>
            <th>Domain</th>
            <th>Latitude</th>
            <th>Longitude</th>
            <th>Location</th>
            <th>Suspected List</th>
          </tr>
        </thead>
        <tbody>
        {#if Array.isArray(tabledata1) && tabledata1.length > 0}
        {#each tabledata1 as tblD}
          <tr>
            <td>{tblD["City"]}</td>
            <td>{tblD["Company"]}</td>
            <td>{tblD["Country"]}</td>
            <td>{tblD["Domain"]}</td>
            <td>{tblD["Latitude"]}</td>
            <td>{tblD["Longitude"]}</td>
            <td>{tblD["Location"]}</td>
            <td>{tblD["Suspected List"]}</td>
          </tr>
        {/each}
        {:else}
            <tr>
              <td colspan="8">No data available for tabledata1.</td>
            </tr>
          {/if}
        </tbody>
      </table>
    </div>
    {:else if showProgress}
    <div class="position-absolute top-50 start-50 translate-middle p-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    {:else}
    <div style="margin-top: 3%; text-align:center; font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif">
      <span>{datafound}</span>
    </div>
    {/if}
</main>
  
<style>
    main{
        margin-left: 3%;
        margin-top: 5px;
    }
  
    table {
      width: 96%;
      table-layout: fixed;
      text-align: center;
      border-collapse: collapse;
      margin-top: 2%;
      /* margin-left: 2%; */
      box-shadow: 0 9px 10px 0 rgba(0, 0, 0, 0.2);
      border: 0.5px;
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
  
    thead th {
      position: sticky;
      top: 0;
      background-color: black;
      border: 1px;
      color: rgb(118, 214, 57);
      height: 15px 10px;
    }
  
    .table-conatiner1 {
      margin-top: 100px;
    }

  
  </style>