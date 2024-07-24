<script>
  import { basepath } from "$lib/config";
  import { postRequest } from "$lib/req_utils";

  export let casename;
  export let casetype;
  export let user;
  console.log(casename, casetype);
  let showprogress = false;
  let bparty = [];
  let gotResult = false;
  let data_found;
  let columnFilters = {};
  let filteredResults = [];
  // let showprogress = false;

  function getdata() {
    gotResult = false;
    showprogress = true;
    console.log(casename,casetype)
    // fetch(`${basepath()}/getcasedata`, {
    //   method: "post",
      // body: JSON.stringify({
      //   casename: casename,
      //   casetype: casetype,
      //   mode: "bparty",
      //   user: user,
      // }),
    // })
    const url = `${basepath()}/getcasedata`;
    postRequest(fetch,url,JSON.stringify({
        casename: casename,
        casetype: casetype,
        mode: "bparty",
        user: user,
      }))
      .then((res) => res.json())
      .then((data) => {
        console.log(data, "==============");
        if (data === "nodata") {
          data_found = "Not Match in Database";
          gotResult = false;
          showprogress = false;
        } else {
          bparty = data;
          filteredResults = [...bparty];
          console.log(bparty);
          gotResult = true;
          showprogress = false;
        }
      });
  }
  function handleColumnSearch(column, event) {
    const filterValue = event.target.value.trim().toLowerCase();
    columnFilters[column] = filterValue;
    console.log("handle column search", columnFilters[column]);
    applyFilters();
  }

  function applyFilters() {
    const filteredData = bparty.filter((item) => {
      console.log(item);
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
  getdata();
</script>

{#if gotResult}
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th>Numbers</th>
          <th>Nickname</th>
          <th>First Call</th>
          <th>Last Call</th>
          <th>Total Calls</th>
        </tr>
        <tr>
          <th class="search">
            <input
              placeholder="search"
              on:input={(event) => handleColumnSearch("number", event)}
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
              on:input={(event) => handleColumnSearch("min_date", event)}
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
              on:input={(event) => handleColumnSearch("count", event)}
            />
          </th>
        </tr>
      </thead>
      <tbody>
        {#each filteredResults as i}
          <tr>
            {#if i["source_true"] === "True" || i["nickname"] !== ""}
            <td class="py-1">
              <img src="/redflag.png" alt="red">
              
                {i["number"]}
            </td>
          {:else}
            <td class="py-1">
             
                {i["number"]}
            </td>
          {/if}
          <td>{i['nickname']}</td>
            <td>{i["min_date"]}</td>
            <td>{i["max_date"]}</td>
            <td>{i["count"]}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
{:else if showprogress}
  <div
    class="position-absolute top-500 start-50 translate-middle p-5"
    style="margin-top: 20%;"
  >
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  <!-- {/if} -->
{/if}

<style>
  table {
    width: 94%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    /* margin-top: 1%; */
    margin-left: 4%;
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
    font-size: 14px;
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
  /* tbody {
    
  } */
  tbody td {
    border: 1px solid rgba(0, 0, 0, 0.1);
    word-break: break-word;
  }
  .table-container {
    max-height: 80vh;
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
  tbody tr:hover {
    background-color: #d0e4f1;
  }

  img {
    width: 30px;
    height: 40px;
  }
</style>
