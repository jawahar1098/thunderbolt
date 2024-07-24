<script>
  // @ts-nocheck

  import { createEventDispatcher, afterUpdate } from "svelte";
  import { basepath } from "$lib/config";

  export let propData;
  console.log("Propdataaaaaaaaaaaaaaaaaa", propData);
  $: number = propData.number;
  $: startDate = propData.startdate;
  $: endDate = propData.enddate;
  let data = {};
  let data1 = {};
  let showProgress = false;
  let gotResult = false;
  let datafound = "Not Data Yet";
  let final_result = [];
  let final_result1 = [];
  let tableData;
  let tableHeader;
  let formattedData;
  let datad;

  const rows = [];
  const rowSize = 5;

  let columnFilters = {};
  let filteredResults = [];
  // const dispatch = createEventDispatcher();

  async function handset_analysis() {
    console.log("entered into handset");
    gotResult = false;
    showProgress = true;
    console.log("cdr number", number);
    const handset = new FormData();
    handset.append("number", number);
    handset.append("mode", "handset");
    handset.append("startDate", startDate);
    handset.append("endDate", endDate);

    try {
      // console.log(contacts_of_mobileNumber,"datas sent tobackend");
      const response = await fetch(`${basepath()}/call_details`, {
        method: "POST",
        body: handset,
      });

      if (response.ok) {
        data = await response.json();
        console.log(data);
        if (data.data_dict === "No data Matched") {
          showProgress = false;
          datafound = "No Data Matched In Database";
          console.log(datafound, "-----------------");
        } else {
          gotResult = true;
          showProgress = false;
          final_result = data.result;
          filteredResults = [...final_result];
        }
        showProgress = false;
      } else {
        console.error("Failed to submit form");
      }
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  }

  afterUpdate(() => {
    console.log("updated---------,", propData);
    if (number != propData.number) {
      return;
    } else {
      handset_analysis();
      number = "";
    }
  });
</script>

<div
  class="table-container"
>
  {#if gotResult}
    <table>
      <thead>
        <tr>
          <th>IMEI</th>
          <th>count</th>
          <th>source</th>
          <th>Source Number</th>
        </tr>
      </thead>
      <tbody>
        <!-- {#if final_result && Array.isArray(final_result)} -->

        {#each final_result as result, i}
          {#each result.source_numbers as site, j}
            <tr>
              {#if j === 0}
                <td rowspan={result.source_numbers.length}>{result.imei}</td>
                <td rowspan={result.source_numbers.length}>{result.count}</td>
                <td rowspan={result.source_numbers.length}>{result.from}</td>
              {/if}
              <td>{site}</td>
            </tr>
          {/each}
        {/each}

        <!-- {:else}
      <tr>
        <td colspan="4">No data available</td>
      </tr>
    {/if} -->
      </tbody>
    </table>
  {/if}
</div>

<style>
  table {
    width: 94%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    margin-top: 1%;
    /* margin-left: 5%; */
    /* box-shadow: 0 9px 10px 0 rgba(0, 0, 0, 0.2); */
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
    height: 5vh;
  }
  .table-container {
    width: 100%;
    max-height: 63vh;
    overflow-y: auto;
    overflow-x: auto;
    position: sticky;
    z-index: 1;
    /* margin-top: 2vh; */
    top: 0;
  }
  /* tbody {
        
      } */
  tbody td {
    border: 1px solid rgba(0, 0, 0, 0.1);
    word-break: break-word;
  }

  tbody tr:hover {
    background-color: #d0e4f1;
  }
  a {
    color: black;
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
  .heading {
    margin-left: 5%;
    color: #296b97;
  }
  .nodata {
    font-size: 1.2em;
    margin: 0;
  }
  img {
    width: 23%;
  }
</style>
