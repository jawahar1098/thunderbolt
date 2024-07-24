<script>
  // @ts-nocheck

  import { createEventDispatcher,  afterUpdate } from "svelte";
  import { basepath } from "$lib/config";
  import { postRequest } from "$lib/req_utils";


  export let propData;
  $: number = propData.number;
  $: startDate = propData.startdate;
  $: endDate = propData.enddate;
  let data = {};
  let showProgress = false;
  let gotResult = false;
  let datafound = "Not Data Yet";
  let final_result = [];
  let columnFilters = {};
  let filteredResults = [];
  let data_dict;
  let data_2;
  const dispatch = createEventDispatcher();

  //PROFILE SECTION, refer profile_num flask endpoint, completed
  function summary_mobile() {
    gotResult = false;
    showProgress = true;
    const summary = new FormData();
    summary.append("number", number);
    if (startDate) {summary.append("fromdate", startDate)};
    if (endDate){ summary.append("todate", endDate)};
    summary.append("mode", "summary_total");
    showProgress = true;
    // try {
    //   const response = await fetch(`${basepath()}/summary_of_mobile`, {
    //     method: "POST",
    //     body: summary,
    //   });

    const url = `${basepath()}/summary_of_mobile`;
    postRequest(fetch,url,summary)
    .then(data => {

        data_dict = data.data_dict
        console.log(typeof(data_dict), typeof(data) , "type of")
        console.log("data 2 ",data.data_dict)
        console.log(data, data.data2);
        if (data.data2 === "Not data Matched") {
          showProgress = false;
          datafound = "No Data Matched In Database";
        } else {
          final_result = data.data2;
          filteredResults = [...final_result];
          gotResult = true;
          dispatch("updateData", filteredResults);
        }
        // showImage = true
      })
      console.log(data.data_dict," last")
  }

  afterUpdate(() => {
    if (number != propData.number) {
      return;
    } else {
      summary_mobile();
      number = "";
      startDate = "";
      endDate = "";
    }
  });

  function handleColumnSearch(column, event) {
    const filterValue = event.target.value.trim().toLowerCase();
    columnFilters[column] = filterValue;
    applyFilters();
  }

  function applyFilters() {
    const filteredData = Object.values(data.data2).filter((item) => {
      for (const field in columnFilters) {
        const filterValue = columnFilters[field];
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
  }

</script>

{#if gotResult}
<!-- Profile Data -->
  <div class="table-container1">
    <table>
      <thead>
        <tr>
         <th style="width: 5%;">PHONE</th>
         <th style="width: 212px;">NICKNAME</th>
         <th style="width: 212px;">ADDRESS</th>
         <th>provider</th>
         <th>cat</th>
          <th>module</th>
          <th>org</th>
          <th>io_name</th>

          <th>Total Contacts</th>
          <th>cdat count </th>
          <th style="width: 212px;">other states</th>
          <th>imei</th>
          <th>IMSI</th>
          <th>start_date</th>
          <th>end_date</th>
          
          <th>CDR last updated</th>
          <!-- <th>caf</th> -->
        </tr>
      </thead>
      <tbody>
        {#each Object.values(data_dict) as item}
        <tr>
            <td>{item['source_number']}</td>
            <td>{item['nickname']}</td>
            <td>{item['permanent_address']}</td>
            <td>{item['total_provider']}</td>
            <td>{item['cat']}</td>
            <td>{item['module']}</td>
            <td>{item['org']}</td>
            <td>{item['io_name']}</td>


            <td>{item['unique_destination_number_count'].length}</td>
            <td>{item['cdat_count'].length}</td>
            <td>{item['roaming_state']}</td>
            <td>{item['total_imei'].length}</td>
            <td>00</td>
            <td>{item['start_date']}</td>
            <td>{item['end_date']}</td>
            
            <td>{item['last_updated_date']}</td>
            <!-- <td>{item['caf']}</td> -->
        </tr>
        {/each}
      </tbody>
    </table>
  </div>


<!-- Actual Data  -->
  <div class="flex justify-center mt-3">
    <h4 class="heading">
      SUMMARY TOTAL - {propData.number}
    </h4>
  </div>
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th style="width: 6%;">PHONE</th>
          <th style="width: 6%;">OTHER</th>
          <th style="width: 4%;">OTHER NICKNAME</th>
          <th style="width: 4%;">OTHER ADDRESS</th>
          <th style="width: 4%;">INCOMING</th>
          <th style="width: 4%;">OUTGOING</th>
          <th style="width: 4%;">TOTAL CALLS</th>
          <th style="width: 4%;">DURATION</th>
          <th style="width: 4%;">FIRST CALL </th>
          <th style="width: 4%;">LAST CALL</th>
        </tr>
        <tr>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("source_number", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) =>
                handleColumnSearch("destination_number", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("nickname", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("address", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("call_in", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("call_out", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("total_calls", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("duration", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("first_call", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("last_call", event)}
            />
          </th>
        </tr>
      </thead>
      <tbody>
  
        {#each filteredResults as item}
          <tr class="border-b hover:bg-gray-100 dark:border-neutral-500">
            <td>{item["source_number"]}</td>
            <td>
              <a
                href="/cdat/profile?value={item['destination_number']}"
                target="_blank"
              >
                {item["destination_number"]}
              </a></td
            >
            <td>{item["nickname"]}</td>
            <td>{item["address"]}</td>
            <td
              ><a
                href="/cdat/hyperlink?dest_number={propData.number}&mode=call_in&number={item[
                  'destination_number'
                ]}&fromdate={propData.startdate}&todate={propData.enddate}&state="
                target="_blank">{item["call_in"]}</a
              ></td
            >
            <td
              ><a
                href="/cdat/hyperlink?dest_number={propData.number}&mode=call_out&number={item[
                  'destination_number'
                ]}&fromdate={propData.startdate}&todate={propData.enddate}&state="
                target="_blank">{item["call_out"]}</a
              ></td
            >
            <td
              ><a
                href="/cdat/hyperlink?dest_number={propData.number}&mode=total_calls&number={item[
                  'destination_number'
                ]}&fromdate={propData.startdate}&todate={propData.enddate}&state="
                target="_blank">{item["total_calls"]}</a
              ></td
            >
            <td>{item["duration"]}</td>
            <td>{item["first_call"]}</td>
            <td>{item["last_call"]}</td>
          </tr>
        {/each}
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
  <div class="no_data">
    <img src="/nodata.png" alt="" />
    <p class="nodata">{datafound}!!!!!!!!</p>
  </div>
{/if}

<style>

  .heading {
    /* margin-left: 5%; */
    color: #296b97;
    display: flex;
    justify-content: center;
    margin-top: 4vh;
  }
  .table-container1 {
    margin-top: 1%;
    height: 30vh;
    overflow-y: auto;
    overflow-x: scroll;
  }
  table {
    width: 94%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    margin-top: 1%;
    margin-left: 5%;
  }

  th,td {
    border: 0.5px black;
    text-align: left;
    text-overflow: ellipsis;
    text-align: center;
    padding: 5px;
    text-wrap: wrap;
  }

  thead{
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
    max-height: 50vh;
    overflow-y: auto;
    overflow-x: auto;
    position: sticky;
    /* margin-top: -1px; */
    z-index: 1;
    top: 0;
  }
  .search input {
    width: 80%;
    border: 1px solid white;
    border-radius: 5px;
    height: 4vh;
    font-size: 0.8em;
  }

  thead tr{
    border: none;
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
  .nodata {
    font-size: 1.2em;
    margin: 0;
  }
  img {
    width: 23%;
  }
</style>
