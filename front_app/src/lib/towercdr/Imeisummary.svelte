<script>
    // @ts-nocheck

  import { basepath } from "$lib/config";
  import { postRequest } from "$lib/req_utils";

  export let casename;
  export let casetype;
  export let user
  console.log(casename,casetype)
  let showprogress = false
  let caseimei = []
  let overallimei = []
  let gotResult = false
  let data_found = "";
  let columnFilters = {};
  let final_result = [];
  let filteredResults = [];


  function getdata(){
      showprogress = true
      gotResult = false
      // fetch(`${basepath()}/getcasedata`,{
      //     method:'post',
      //     body:JSON.stringify({'casename':casename, 'casetype':casetype,'mode':"imeisummary",'user':user})
      // })
      const url = `${basepath()}/getcasedata`;
      postRequest(fetch,url,JSON.stringify({'casename':casename, 'casetype':casetype,'mode':"imeisummary",'user':user}))
      .then(res => res.json())
      .then(data => {
          console.log(data)
          if(data.message === 'nodata'){
              data_found = "No Match in Database"
              gotResult = false
              showprogress = false
          }
          else{
              caseimei = data
              console.log(caseimei)
              gotResult = true
              showprogress = false

          }

      })
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
  getdata();
</script>

<div>
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
</div>

<!-- Imei summary  -->
{#if gotResult}
    <div class="table-container"> 
    <table>
      <thead>
        <tr>
          <th> Imei </th>
          <th> Tower
          <table class="min-w-full mt-2 divide-y divide-gray-200">
            <thead>
              <th>Number</th>
              <th>First Call</th>
              <th>Last Call</th>
              <th>calls</th>
            </thead>
          </table>
          </th>
          <th> CDR 
            <table>
              <thead>
                <th>Number</th>
                <th>First Call</th>
                <th>Last Call</th>
                <th>calls</th>
              </thead>
            </table>
          </th>
          <th> IPDR 
          <table>
            <thead>
              <th>Number</th>
              <th>First Call</th>
              <th>Last Call</th>
              <th>calls</th>
            </thead>
          </table>
          </th>
        </tr>
      </thead>
      <tbody>
        {#each Object.entries(caseimei) as [key, value]}
        <tr>
          <td> {key} </td>
              <!-- Tower -->
            <td>
              <table>
                <tbody>
                  {#each value['tower'] as a }
                    <tr>
                      <td>{a['tower_source_number']}</td>
                      <td>{a['tower_first_call']}</td>
                      <td>{a['tower_last_call']}</td>
                      <td>{a['tower_total_matches']}</td>
                    </tr>
                  {/each}
                </tbody>
              </table>
            </td>
              <!-- CDR -->
          <td>
            <table>
              <tbody>
                {#each value['cdr'] as a }
                  <tr>
                    <td>{a['cdr_source_number']}</td>
                    <td>{a['cdr_first_call']}</td>
                    <td>{a['cdr_last_call']}</td>
                    <td>{a['cdr_total_matches']}</td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </td>
              <!-- IPDR -->
          <td>
            <table>
              <tbody>
                {#each value['ipdr'] as a }
                  <tr>
                    <td>{a['ipdr_source_number']}</td>
                    <td>{a['ipdr_first_call']}</td>
                    <td>{a['ipdr_last_call']}</td>
                    <td>{a['ipdr_total_matches']}</td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </td>
        </tr>
        {/each}
      </tbody>
    </div>
{:else}
  {data_found}
{/if}



<style>
table {
  width: 94%;
  table-layout: fixed;
  text-align: center;
  border-collapse: collapse;
  /* margin-top: 2%; */
  margin-left: 5%;
  box-shadow: 0 9px 10px 0 rgba(0, 0, 0, 0.2);
}

th, td {
  border: 0.5px black;
  text-align: left;
  text-overflow: ellipsis;
  text-align: center;
  padding: 5px;
}

thead th {
  position: sticky;
  top: 0;
  background-color: black;
  border: 1px;
  color: rgb(118, 214, 57);
  height: 15px 10px;
}
tbody {
  width: 5%;
}
tbody td {
    border: 1px solid rgba(0, 0, 0, 0.1);
  }
.table-container {
  max-height: 90vh; 
  overflow-y: auto;
  overflow-x: auto;
  position: sticky ;
  z-index: 1;
  top: 0; 
  width: 100vw;
    margin-left: -7%;

}
.search input {
  width: 100%;
  box-sizing: border-box;
}

tbody tr:hover {
  background-color: rgb(236, 226, 226);
}
        



  table {
    width: 100%;
    table-layout: fixed;
    text-align: center;
    border-collapse: collapse;
    /* margin-top: 2%; */
    /* margin-left: 5%; */
    box-shadow: 0 9px 10px 0 rgba(0, 0, 0, 0.2);
  }

  th,
  td {
    border: 0.5px black;
    text-align: left;
    text-overflow: ellipsis;
    text-align: center;
    padding: 5px;
  }

  thead th {
    position: sticky;
    top: 0;
    background-color: #5cb2eb;
    border-top: 1px solid #a5c2d5;
    border-right: 1px solid #a5c2d5;
    border-left: 1px solid #a5c2d5;
    border-bottom: 1px solid #5cb2eb;
    border: 1px;
    color: white;
    height: 15px 10px;
  }
  tbody {
    width: 5%;
  }
  .search input {
    width: 80%;
    /* border: none; */
    border: 1px solid white;
    border-radius: 5px;
    height: 4vh;
    font-size: 0.8em;
  }
  tbody td {
    border: 1px solid rgba(0, 0, 0, 0.1);
  }
  .table-container {
    max-height: 83vh;
    overflow-y: auto;
    overflow-x: auto;
    position: sticky;
    z-index: 1;
    top: 0;
    /* width: 100vw;
    margin-left: -7%; */
  }
  .search input {
    width: 100%;
    box-sizing: border-box;
  }

  tbody tr:hover {
    background-color: #d0e4f1;
  }
</style>
