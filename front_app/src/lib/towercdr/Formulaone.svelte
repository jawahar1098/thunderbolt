<script>
      // @ts-nocheck

  import { basepath } from "$lib/config";
  import { userDetailsStore } from "$lib/datastore";
  import { onMount } from "svelte";
  import { postRequest } from "$lib/req_utils";


  // export let key_location;
  // export let sitename;
  // export let startDate;
  // export let endDate ;
  export let selectedValues;
  export let casename;
  export let casetype;
  export let user;
  let data = [];
  let final_result = [];
  let ind_num_val = [];
  let induval = false;
  let mode;
  let current_num;
  let columnFilters = {};
  let filteredResults = [];

  let gotResult = false;
  let data_found = "No data";
  let showprogress = false;
  let total_pages = 0;
  let page_count = 0;
  let currentPage = 0;
  let itemsPerPage = 50;
  let pagination = false;
  let downexcel = false;
  let userDetails = JSON.parse(localStorage.getItem("userDetails"));
  console.log(ind_num_val, "==============");

  function getcasedata() {
    gotResult = false;
    // fetch(`${basepath()}/getcasedata`, {
    //   method: "post",
    //   body: JSON.stringify({
    //     casename: casename,
    //     casetype: casetype,
    //     itemsper_page: 50,
    //     pagenumber: currentPage,
    //     mode: "singlecase",
    //     user: user,
    //   }),
    // })

    const url = `${basepath()}/getcasedata`;
    postRequest(fetch,url, JSON.stringify({
        casename: casename,
        casetype: casetype,
        itemsper_page: 50,
        pagenumber: currentPage,
        mode: "singlecase",
        user: user,
      }))

      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        final_result = [];
        data.formulaOne[0].forEach((element) => {
          final_result.push(element);
        });
        filteredResults = [...final_result];
        showprogress = false;
        console.log(final_result);
        total_pages = data.count_pages;
        if (total_pages > 50) {
          pagination = true;
          page_count = Math.ceil(total_pages / 50);
        }

        gotResult = true;
      });
  }
  

  function handleColumnSearch(column, event) {
    const filterValue = event.target.value.trim().toLowerCase();
    columnFilters[column] = filterValue;
    console.log("handle column search", columnFilters[column]);
    applyFilters();
  }

  function applyFilters() {
    const filteredData = final_result.filter((item) => {
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

  // async function exportdata() {
  //   downexcel = true;
  //   const currentDate = new Date();

  //   const filename = `FormulaOne${currentDate
  //     .toLocaleString()
  //     .replace(/[,\s]/g, "_")}`;

  //   const response = await fetch(`${basepath()}/formulaOneexport`, {
  //     method: "post",
  //     body: JSON.stringify({
  //       casename: casename,
  //       casetype: casetype,
  //       user: user,
  //     }),
  //   });
  //   if (response.ok) {
  //     // Trigger the download by creating an anchor element
  //     const blob = await response.blob();
  //     const url = window.URL.createObjectURL(blob);
  //     const a = document.createElement("a");
  //     a.href = url;
  //     a.download = filename;
  //     a.click();
  //     window.URL.revokeObjectURL(url);
  //   } else {
  //     // Handle the error
  //     console.error("File download failed.");
  //   }
  //   downexcel = false;
  // }

  function exportdata() {
  downexcel = true;
  const currentDate = new Date();
  const filename = `FormulaOne_${currentDate.toLocaleString().replace(/[,\s]/g, "_")}`;


  const url = `${basepath()}/formulaOneexport`;
    postRequest(fetch,url, JSON.stringify({
        casename: casename,
        casetype: casetype,
        user: user,
      }))


    .then((response) => {
      if (!response.ok) {
        throw new Error("File download failed.");
      }
      return response.blob();
    })
    .then((blob) => {
      // Trigger the download by creating an anchor element
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      a.click();
      window.URL.revokeObjectURL(url);
      downexcel = false;
    })
    .catch((error) => {
      console.error(error.message);
      downexcel = false;
    });
}


  function getvalue(num) {
    current_num = num;
    induval = false;

    // fetch(`${basepath()}/getvalue`, {
    //   method: "post",
    //   body: JSON.stringify({ number: num }),
    // })

    const url = `${basepath()}/getvalue`;
    postRequest(fetch,url,JSON.stringify({ number: num }))

      .then((res) => res.json())
      .then((val) => {
        console.log(val,"---val---");
        ind_num_val = [];
        if (val.status !== "failure") {
          induval = true;
          ind_num_val = val.data_dict

          console.log(ind_num_val, "------ind num val -------");
        }
        document.getElementById("my_modal_4").setAttribute("open", true);
      });
  }

  onMount(() => {
    showprogress = true;
    final_result = [];

    if (casename !== "") {
      getcasedata();
    }
  });

  function setPage(p) {
    showprogress = true;
    if (p >= 0 && p < page_count) {
      currentPage = p;
      itemsPerPage = 50;
      gotResult = false;
      getcasedata();
    }
  }
  function formatDate(dateString) {
    if (!dateString) {
      return "Invalid Date";
    }

    const date = new Date(dateString);

    // Check if the date is invalid (NaN)
    if (isNaN(date.getTime())) {
      return "Invalid Date";
    }

    const year = date.getUTCFullYear();
    const month = (date.getUTCMonth() + 1).toString().padStart(2, "0");
    const day = date.getUTCDate().toString().padStart(2, "0");
    // const hours = date.getUTCHours().toString().padStart(2, '0');
    // const minutes = date.getUTCMinutes().toString().padStart(2, '0');
    // const seconds = date.getUTCSeconds().toString().padStart(2, '0');

    return `${day}-${month}-${year}`; // ${hours}:${minutes}:${seconds}`;
  }
</script>

{#if showprogress}
  <div
    class="position-absolute top-500 start-50 translate-middle p-5"
    style="margin-top: 20%;"
  >
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
{/if}
<dialog id="my_modal_4">
  <div class="container">
    {#if induval}
      <h3>Overall Tower Data Profile</h3>
      <table class="overalltowertable">
        <thead>
          <tr>
            <th> Number </th>
            <th> Other </th>
            <th> Dates present </th>
            <th> Date Diff </th>
            <th> First call </th>
            <th> Last call </th>
            <th> Total calls </th>
            <!-- <th> valid Numbers </th> -->
            <!-- <th> Invalid Nimbers </th> -->
            <th> Call Ratio </th>
            <th> Sms Ratio </th>
            <th> Total Ratio </th>
            <th> Sector </th>
            <th> Tower </th>
            <th> Imei </th>
            <th> Imei CDR </th>
            <th> Nickname </th>
          </tr>
        </thead>
        <tbody>
          {#each ind_num_val as tblD}
            <tr>
              <td>{tblD["source_number"]}</td>
              <td>{tblD["other_number"]}</td>
              <td>{tblD["dates_present"]}</td>
              <td>{tblD["date_difference"]}</td>
              <td>{formatDate(tblD["max_date"])}</td>
              <td>{formatDate(tblD["min_date"])}</td>
              <td>{tblD["total_call_count"]}</td>
              <!-- <td>{tblD["notValidUniqueCount"].length}</td> -->
              <!-- <td>{tblD["validUniqueCount"].length}</td> -->
              <td>{tblD["ratio_call"]}</td>
              <td>{tblD["ratio_sms"]}</td>
              <td>{tblD["ratio"]}</td>
              <td>{tblD["sector"].length}</td>
              <td>{tblD["tower"].length}</td>
              <td>{tblD["imei"].length}</td>
              <td>{tblD["imei_count_cdr"][0].length}</td>
              <td>{tblD["nickname"]}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {:else}
      <p>No data</p>
    {/if}
    <div>
      {#if induval} 
      <a
        href="/cdat/hyperlink/?number={current_num}&mode=overallsummary "
        target="_blank">Overall Tower Summary</a
      >
      {/if}
      <a
        href="/cdat/hyperlink/?number={current_num}&mode=summary"
        target="_blank">CDR Summary</a
      >
    </div>
    <div>
      <form class="flex-end" method="dialog">
        <button>Close</button>
      </form>
    </div>
  </div>
</dialog>
{#if gotResult}
<div class="buttondiv text-end">
  <button class="btn1" on:click={exportdata}> Export</button>
  {#if downexcel}
  <div class="spinner-border text-success" role="status">
    <span class="sr-only">+</span>
  </div>
  {/if}
</div>

<div class="table-container">
    <table>
      <thead>
        <tr>
          <th style="width:9vw;"> Number </th>
          <th> provider </th>
          <th> Fullname </th>
          <th style="width:15vw;"> Address </th>
          <th> date of Activation </th>
          <th> Alternate Number </th>
          <th> Nickname </th>
          <th> First call </th>
          <th> Last call </th>
          <th> Dates present </th>
          <th> Date Diff </th>
          <th> Total calls </th>
          <th> Other </th>
          <th> valid Numbers </th>
          <th> Invalid Nimbers </th>
          <th> Callin </th>
          <th> Callout </th>
          <th> Sms_in </th>
          <th> Sms_out </th>
          <!-- <th> incoming </th> -->
          <!-- <th> Outgoing </th> -->
          <th> state </th>
          <th> Sector </th>
          <th> Tower </th>
          <th> Imei </th>
          <th> Only sms </th>
          <th> Only incoming </th>
          <th> Only outgoing </th>
          <th> Imei CDR </th>
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
              on:input={(event) => handleColumnSearch("nickname", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("fullname", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) =>
                handleColumnSearch("date_of_activation", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("local_address", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) =>
                handleColumnSearch("alternate_number", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("other_number", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("dates_present", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("date_difference", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("max_date", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("min_date", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) =>
                handleColumnSearch("total_call_count", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) =>
                handleColumnSearch("validUniqueCount", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) =>
                handleColumnSearch("notValidUniqueCount", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) =>
                handleColumnSearch("total_callin_count", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) =>
                handleColumnSearch("total_callout_count", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) =>
                handleColumnSearch("total_smsin_count", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) =>
                handleColumnSearch("total_smsout_count", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("total_in_count", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("total_out_count", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("provider", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("sector", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("tower", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("state", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("imei", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("imei_count_cdr", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("only_sms", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("only_incoming", event)}
            />
          </th>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("only_outgoing", event)}
            />
          </th>
        </tr>
      </thead>
      <tbody>
        {#each filteredResults as tblD}
          <tr class="border border-gray-100">
            {#if tblD["imei_count_cdr"][0].length > 0 || tblD["nickname"].length > 0}
              <td class="py-1">
                <img src="/redflag.png" alt="red">
                <button id = "blur"
                  class="btn btn-light border-0"
                  on:click={() => getvalue(tblD["source_number"])}
                >
                  {tblD["source_number"]}
                </button>
              </td>
            {:else}
              <td class="py-1">
                <button
                  class="btn btn-light border-0"
                  on:click={() => getvalue(tblD["source_number"])}
                  >{tblD["source_number"]}</button
                >
              </td>
            {/if}
            <td>{tblD["provider"]}</td>
            <td >{tblD["name"]}</td>
            <td >{tblD["address"]}</td>
            <td>{tblD["dateOfActivation"]}</td>
            <td >{tblD["alternatenumber"]}</td>
            <td >{tblD["nickname"]}</td>
            <td>{formatDate(tblD["min_date"])}</td>
            <td>{formatDate(tblD["max_date"])}</td>
            <td>{tblD["date_difference"]}</td>
            <td>{tblD["dates_present"]}</td>
            <td>{tblD["total_call_count"]}</td>
            <td>{tblD["other_number"]}</td>
            <td>{tblD["validUniqueCount"].length}</td>
            <td>{tblD["notValidUniqueCount"].length}</td>
            <td>{tblD["total_callin_count"]}</td>
            <td>{tblD["total_callout_count"]}</td>
            <td>{tblD["total_smsin_count"]}</td>
            <td>{tblD["total_smsout_count"]}</td>
            <!-- <td>{tblD["total_in_count"]}</td> -->
            <!-- <td>{tblD["total_out_count"]}</td> -->
            <td>{tblD["state"].length}</td>
            <td>{tblD["tower"].length}</td>
            <td>{tblD["sector"].length}</td>
            <td>{tblD["imei"].length}</td>
            <td>{tblD["only_sms"].length}</td>
            <td>{tblD["only_incoming"].length}</td>
            <td>{tblD["only_outgoing"].length}</td>
            <td>{tblD["imei_count_cdr"][0].length}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
  {/if}

{#if pagination}
  <div class="pagination">
    {#if page_count > 1}
      {#if currentPage > 0}
        <button
          type="button"
          class="btn btn-sm btn-secondary"
          on:click={() => setPage(0)}>FIRST</button
        >
        <button
          type="button"
          class="btn btn-sm btn-secondary"
          on:click={() => setPage(currentPage - 1)}>&lt;</button
        >
      {/if}
      {#each [currentPage - 2, currentPage - 1, currentPage, currentPage + 1, currentPage + 2] as i}
        {#if i > -1 && i < page_count}
          {#if currentPage !== i}
            <button
              type="button"
              class="btn btn-sm btn-dark"
              on:click={() => setPage(i)}>{i + 1}</button
            >
          {:else}
            <button type="button" class="btn btn-sm btn-dark bg-dark-600"
              >{i + 1}</button
            >
          {/if}
        {/if}
      {/each}
      {#if page_count > currentPage + 1}
        <button
          type="button"
          class="btn btn-sm btn-dark"
          on:click={() => setPage(currentPage + 1)}>&gt;</button
        >
        <button
          type="button"
          class="btn btn-sm btn-darek"
          on:click={() => setPage(page_count - 1)}>LAST</button
        >
      {/if}
    {/if}
  </div>
{/if}

<style>
  table {
    width: 100%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
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
  th{
    width: 6vw;
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
    width: 95vw;
    max-height: 90vh;
    overflow-y: auto;
    overflow-x: auto;
    position: sticky;
    /* z-index: 1; */
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
  .address {
    width: 15px;
  }

  tbody tr:hover {
    background-color: #d0e4f1;
  }

  .pagination {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 1rem;
    margin-left: 20%;
  }

  #my_modal_4 {
    margin-top: 4%;
    z-index: 1;
    background-color: rgb(255, 255, 255);
    width: 90vw;
    margin-left: 6%;
  }
  .buttondiv {
    margin-bottom: 1vh;
  }

  .container {
    width: 85%;
    padding-right: 15px;
    margin-left: 0;
  }
  .overalltowertable {
    width: 87vw;
    margin-bottom: 2vh;
  }
  .py-1{
    display: flex;
  }

  img {
    width: 30px;
    height: 40px;
  }

  .btn1{
    padding: 8px 15px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    width: 10vw;
  }


</style>
