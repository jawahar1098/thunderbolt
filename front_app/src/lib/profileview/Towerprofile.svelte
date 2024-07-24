<script>
  // @ts-nocheck

  import NumberSearch from "$lib/analysis/numberSearch.svelte";
  import { basepath } from "$lib/config";
    import { postRequest } from "$lib/req_utils";
  import { afterUpdate } from "svelte";

  let data;
  export let propData;
  $: number = propData.number;

  let showProgress = false;
  let gotResult = false;
  let datafound = "Not Data Yet";
  let showdata;

  function profile_num() {
    gotResult = false;
    // showProgress = true;
    console.log("tower number", number);

    const profile_num = new FormData();
    profile_num.append("number", number);
    profile_num.append("mode", "towerprofile");
    showProgress = true;
    const url = `${basepath()}/profile_num`
    postRequest(fetch,url,profile_num)
    .then((data) => {
        console.log(
          data,
          "---------------------------tower"
        );
        if (data.data_dict === "No data Matched") {
          gotResult = false;
          showProgress = false;
          datafound = "No Data Matched In Database";
          console.log(datafound,"----------------------------tower--------------")
        } else {
          showProgress = false;
          gotResult = true;
          showdata = data.data_dict;
        }
      })

      .catch((err) => {
        console.log(err);
      });
  }

  afterUpdate(() => {
    if (number != propData.number) {
      return;
    } else {
      profile_num();
      number = "";
    }
  });
</script>

<!-- <dialog id="my_modal_4" class="modal fixed inset-0 z-50 overflow-y-auto">
  <div class="modal-box w-11/12 max-w-7xl mx-auto bg-white shadow-lg rounded-md p-6">
    <h3 class="font-bold text-2xl mb-4">Hello!</h3>
    <p class="mb-4">Click the button below to close</p>
     <NumberSearch  {number}/>

    <div class="modal-action flex justify-end mt-4">
      
    </div>
  </div>
  <div>
      <form method="dialog">
          <button class="btn px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">Close</button>
        </form>
  </div>
</dialog> -->
<main>
  <!-- <h1>Tower profile</h1> -->
  {#if gotResult}
    <div class="towerpro 4/13">
      <h1 class="header">Tower Profile</h1>
      {#each showdata as item}
        <div class="table-like-container">
          <div class="table-row">
            <div class="count_details">
              <label for="" class="font-bold">Imei</label>
              <!-- </div>
            <div class="table-cell"> -->
              <p class="info-item" id="caf">{item["imei"].length}</p>
            </div>
          </div>

          <div class="table-row">
            <div class="count_details">
              <label for="" class="font-bold">Valid Contacts</label>
              <!-- </div>
            <div class="table-cell px-10"> -->
              <p class="info-item" id="caf">
                {item["validUniqueCount"].length}
              </p>
            </div>
          </div>

          <div class="table-row">
            <div class="count_details">
              <label for="" class="font-bold">Invalid Contacts</label>
              <!-- </div>
            <div class="table-cell px-10"> -->
              <p class="info-item" id="caf">
                {item["notValidUniqueCount"].length}
              </p>
            </div>
          </div>

          <div class="table-row">
            <div class="count_details">
              <label for="" class="font-bold">Dates Present</label>
              <!-- </div>
            <div class="table-cell px-10"> -->
              <p class="info-item" id="caf">{item["dates_present"]}</p>
            </div>
          </div>

          <div class="table-row">
            <div class="count_details">
              <label for="" class="font-bold">Dates Difference</label>
              <!-- </div>
            <div class="table-cell px-10"> -->
              <p class="info-item" id="caf">{item["date_difference"]}</p>
            </div>
          </div>

          <div class="table-row">
            <div class="count_details">
              <label for="" class="font-bold">Other Number</label>
              <!-- </div>
            <div class="table-cell px-10"> -->
              <p class="info-item" id="caf">{item["other_number"]}</p>
            </div>
          </div>

          <div class="table-row">
            <div class="count_details">
              <label for="" class="font-bold">Tower Present</label>
              <!-- </div>
            <div class="has-tooltip table-cell px-10"> -->
              <p class="info-item" id="caf">{item["tower"].length}</p>
              <!-- <span
                class="tooltip rounded shadow-lg p-1 bg-gray-100 text-red-500 -mt-1 mx-2"
              >
                <div class="overflow-x-auto">
                  <table
                    class="min-w-full bg-white border border-neutral-300 dark:border-neutral-700"
                  >
                    <thead>
                      <tr class="bg-primary dark:bg-primary-dark text-white">
                        <th class="py-2 px-4">
                          <input type="checkbox" />
                        </th>
                        <th class="py-2 px-4">IP</th>
                      </tr>
                    </thead>
                    <tbody>
                      {#each item["tower"] as _t}
                        <tr
                          class="hover:bg-gray-100 text-r dark:hover:bg-gray-800"
                        >
                          <td class="py-2 px-4">
                            <input
                              type="checkbox"
                              name=""
                              id=""
                              bind:checked={_t.isSelected}
                            />
                          </td>
                          <td class="py-2 px-4 text-left">{_t}</td>
                        </tr>
                      {/each}
                    </tbody>
                  </table>
                </div>
                <button class="header"
                  >Analyse Selected Towers</button
                >
              </span> -->
            </div>
          </div>
          <div class="table-row">
            <div class="count_details">
              <label for="" class="font-bold">Sectors Availabels Number:</label>
              <!-- </div>
            <div class="table-cell px-10"> -->
              <p class="info-item" id="">{item["sector"].length}</p>
            </div>
          </div>

          <div class="table-row">
            <div class="count_details">
              <label for="" class="font-bold">Imei in CDR</label>
              <!-- </div>

            <div class="has-tooltip table-cell px-10"> -->
              <p class="info-item">
                {item["imei_count_cdr"].length}
              </p>
              <span
                class="tooltip rounded shadow-lg p-1 bg-gray-100 text-red-500 -mt-1 mr-80"
              >
                <div class="overflow-x-auto">
                  <table
                    class="min-w-full bg-white border border-neutral-300 dark:border-neutral-700"
                  >
                    <thead>
                      <tr class="bg-primary dark:bg-primary-dark text-white">
                        <th class="py-2 px-4">Imei</th>
                      </tr>
                    </thead>
                    <tbody>
                      {#each item["imei_count_cdr"] as _t}
                        <tr class="hover:bg-gray-100 dark:hover:bg-gray-800">
                          <td class="py-2 px-4">{_t}</td>
                        </tr>
                      {/each}
                    </tbody>
                  </table>
                </div>
                <!-- <button class="hover:bg-purple-300 mx-10">Analyse Selected Towers</button> -->
              </span>
            </div>
          </div>

          <div class="table-row">
            <div class="count_details">
              <label for="" class="font-bold">Total calls</label>
              <!-- </div>
            <div class="table-cell px-10"> -->
              <p class="info-item" id="caf">{item["total_call_count"]}</p>
            </div>
          </div>

          <div class="table-row">
            <div class="count_details">
              <label for="" class="font-bold">Ratio Call</label>
              <!-- </div>
            <div class="table-cell px-10"> -->
              <p class="info-item" id="caf">{item["ratio_call"]}</p>
            </div>
          </div>

          <div class="table-row">
            <div class="count_details">
              <label for="" class="font-bold">Sms Ratio</label>
              <!-- </div>
            <div class="table-cell px-10"> -->
              <p class="info-item" id="caf">{item["ratio_sms"]}</p>
            </div>
          </div>

          <div class="table-row">
            <div class="count_details">
              <label for="" class="font-bold">Total Ratio</label>
              <!-- </div>
            <div class="table-cell px-10"> -->
              <p class="info-item" id="caf">{item["ratio"]}</p>
            </div>
          </div>
        </div>
        <!-- <div class="table-row1">
          <div class="table-cell">
            <button
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
              onclick="my_modal_4.showModal()">Summary</button
            > -->

        <!-- <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"><a href="#my_modal_8" class="">Summary</a> -->
        <!-- </button> -->
        <!-- </div>
          <div class="table-cell px-4">
            <button
              class="bg-green-700 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
              on:click={() => renderdata("towercdr")}>Tower CDR</button
            >
          </div>
        </div> -->
      {/each}
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
      <p class="nodata">No data Found!!!!!!!!</p>
    </div>
  {/if}
</main>

<style>
  main {
    width: 100%;
  }
  .header {
    background-color: #3498db;
    color: #fff;
    padding: 5px;
    display: flex;
    width: 99%;
    justify-content: center;
    height: 6vh;
  }
  .count_details {
    display: flex;
    justify-content: space-between;
    margin: 1.6rem;
  }
  p {
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
  .nodata {
    font-size: 1.2em;
    margin: 0;
  }
  img {
    width: 23%;
  }
  /* .table-row{
    display: flex;
    justify-content: center;
    
  } */
  /* button{
    background-color: #3498db;
    border:#3498db;
  }
  button:hover{
    background-color: #91c6e9;
    border:#3498db;

  } */
</style>
