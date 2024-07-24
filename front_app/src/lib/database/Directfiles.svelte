<script>
  // @ts-nocheck

  import { basepath } from "$lib/config";
  import { postRequest } from "$lib/req_utils";
  import { createEventDispatcher } from "svelte";

  let processdata;
  let filetype = "";
  let parser_type = "";
  let res;
  let file;
  let filestat = false;
  let fileup = "";
  let username = "test";
  let provider;
  let fileData = [];
  let final_result = [];
  let columnFilters = {};
  let filteredResults = [];
  let options = [
    "cdr",
    "towercdr",
    "imeicdr",
    "ipdr",
    "caf",
    "rh",
    "poa",
    "gprs",
  ];
  let showtable = false;
  let parsedfiles = [];
  let parsed_file = [];
  let notparsed = [];
  let nil_data = [];
  let alreadyexists = [];
  let startdate;
  let lastdate;
  let page_view = false; // Initialize page_view as false
  let total_pages = 0;
  let page_count = 0;
  let currentPage = 1;
  let itemsPerPage = 10;
  let pagination = true;
  let filesData = [];
  let parsed_total = 0;
  let not_parsed_total = 0;
  let already_exist_total = 0;
  let nil_total = 0;
  let mode;

  function handlePageView() {
    page_view = true;
    pagination = true;
    currentPage = 1;
    itemsPerPage = 10;
    updateFileData();
  }

  function getjson() {
    filestat = true;
    processdata = "Processing";
    const fileInput = document.querySelector("#fileupload");

    if (fileInput && fileInput.files.length > 0) {
      let formData = new FormData();
      console.log(fileInput.files);
      for (let i = 0; i < fileInput.files.length; i++) {
        formData.append("files", fileInput.files[i]);
        formData.append("usename", username);
        formData.append("filetype", filetype);
        formData.append("provider", provider);
      }

      console.log("Sending fetch request...");

      console.log(formData);
      // fetch(`${basepath()}/zipupload`, {
      //   method: "post",
      //   body: formData,
      // })
      const url = `${basepath()}/zipupload`;
      postRequest(fetch,url,formData)
        .then((response) => {
          res = response.message;
          file = response.status;
          console.log(response);
          if (res === "success") {
            // Corrected "sucess" to "success"
            filestat = false;
            fileup = "Upload Success"; // Corrected "Sucess" to "Success"
          }
          if (response.invalidfiles.length > 0) {
            const invalidFilesMessage = response.invalidfiles.join("\n");
            alert(
              `These are invalid files for ${filetype}:\n${invalidFilesMessage}`
            );
          }
          updateFileData();
        })
        .catch((err) => {
          console.log(err);
        });
    }
  }

  function updateFileData(mode, currentPage) {
    console.log(mode, "mode");
    // fetch(`${basepath()}/filestatus`, {
    //   method: "post",
    //   body: JSON.stringify({
    //     startdate: startdate,
    //     enddate: lastdate,
    //     mode: "manual",
    //     parser_type: mode,
    //     page_view: page_view,
    //     currentpage: currentPage,
    //     items: itemsPerPage,
    //     type: mode,
    //   }),
    // })
    const body = {
        startdate: startdate,
        enddate: lastdate,
        mode: "manual",
        parser_type: mode,
        page_view: page_view,
        currentpage: currentPage,
        items: itemsPerPage,
        type: mode,
      }
    const url = `${basepath()}/filestatus`;
    postRequest(fetch,url,body)
      .then((data) => {
        console.log(data, "status");
        if (data.status === "success") {
          if (data.data.parsed && data.data.parsed.data) {
            parsed_total = data.data.parsed.total_pages;
            parsedfiles = Object.values(data.data.parsed.data);
            console.log(parsedfiles, "Parsed files");
          }
          if (data.data.not_parsed && data.data.not_parsed.data) {
            not_parsed_total = data.data.not_parsed.total_pages;
            notparsed = Object.values(data.data.not_parsed.data);
          }
          if (data.data.nil_data && data.data.nil_data.data) {
            nil_total = data.data.nil_data.total_pages;
            nil_data = Object.values(data.data.nil_data.data);
          }
          if (data.data.already_exists && data.data.already_exists.data) {
            already_exist_total = data.data.already_exists.total_pages;
            alreadyexists = Object.values(data.data.already_exists.data);
          }

          if (mode === "parsed") {
            fileData = parsedfiles;
            filesData = [...fileData];
            total_pages = parsed_total;
            showtable = true;
            page_count = Math.ceil(total_pages / 10) + 1;
          } else if (mode === "not_parsed") {
            fileData = notparsed;
            filesData = [...fileData];
            showtable = true;
            total_pages = not_parsed_total;
            page_count = Math.ceil(total_pages / 10) + 1;
          } else if (mode === "nil") {
            fileData = nil_data;
            filesData = [...fileData];
            showtable = true;
            total_pages = nil_data;
            page_count = Math.ceil(total_pages / 10) + 1;
          } else if (mode === "already_exists") {
            fileData = alreadyexists;
            filesData = [...fileData];
            showtable = true;
            total_pages = already_exist_total;
            page_count = Math.ceil(total_pages / 10) + 1;
          }

          // if (page_count >= 1) {
          //   pagination = true;
          //   console.log(page_count);
          // } else {
          //   pagination = false;
          // }
        }
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }

  function handleScrollView() {
    currentPage = false;
    itemsPerPage = false;
    pagination = false;
    if (mode === "parsed") {
      updateFileData("parsed", currentPage);
    }
  }
  updateFileData("parsed", currentPage);

  // function rendertable(mode) {
  //   mode = mode;
  //   total_pages = 0;
  //   page_count = 0;
  //   if (mode === "parsed") {
  //     fileData = parsedfiles;
  //     filesData = [...fileData];
  //     total_pages = parsed_total;
  //     showtable = true;
  //     page_count = Math.ceil(total_pages / 10);
  //   } else if (mode === "not_parsed") {
  //     fileData = notparsed;
  //     filesData = [...fileData];
  //     showtable = true;
  //     total_pages = not_parsed_total;
  //     page_count = Math.ceil(total_pages / 10);
  //   } else if (mode === "nil") {
  //     fileData = nil_data;
  //     filesData = [...fileData];
  //     showtable = true;
  //     total_pages = nil_data;
  //     page_count = Math.ceil(total_pages / 10);
  //   } else if (mode === "already_exists") {
  //     fileData = alreadyexists;
  //     filesData = [...fileData];
  //     showtable = true;
  //     total_pages = already_exist_total;
  //     page_count = Math.ceil(total_pages / 10);
  //   }

  //   if (page_count >= 1) {
  //     pagination = true;
  //     console.log(page_count);
  //   } else {
  //     pagination = false;
  //   }
  // }

  function changedateform(dateString) {
    // const dateString = "Mon, 10 Apr 2023 20:14:48 GMT";
    const dateObject = new Date(dateString);

    const formattedDate = `${padZero(dateObject.getDate())}-${padZero(
      dateObject.getMonth() + 1
    )}-${dateObject.getFullYear()} ${padZero(dateObject.getHours())}:${padZero(
      dateObject.getMinutes()
    )}:${padZero(dateObject.getSeconds())}`;

    console.log(formattedDate);

    // Helper function to pad single digits with a leading zero
    return formattedDate;
  }
  function padZero(num) {
    return num < 10 ? "0" + num : num;
  }

  function handleColumnSearch(column, event) {
    const filterValue = event.target.value.trim().toLowerCase();
    columnFilters[column] = filterValue;
    console.log(columnFilters[column], "Filtered Value");
    applyFilters();
  }

  function applyFilters() {
    const filteredData = filesData.filter((item) => {
      for (const field in columnFilters) {
        const filterValue = columnFilters[field];
        console.log(filterValue, "Filter Value");
        if (
          filterValue &&
          !item[field].toString().toLowerCase().includes(filterValue)
        ) {
          return false;
        }
      }
      return true;
    });
    console.log(filteredData, "Filtered Data");
    fileData = filteredData;

    console.log(fileData, "-------column searh-----");
  }
  function handlePageClick(newPage) {
    if (newPage >= 0 && newPage < page_count) {
      currentPage = newPage;
      itemsPerPage = 10;
      if ("parsed") {
        updateFileData("parsed", currentPage);
      } else if ("not_parsed") {
        updateFileData("not_parsed", currentPage);
      } else if ("nil") {
        updateFileData("nil", currentPage);
      } else {
        updateFileData("alerady_exists", currentPage);
      }
      // setActiveTab("parsed");
    }
  }

  function handleNextClick() {
    if (currentPage + 1 < page_count) {
      currentPage += 1;
      if ("parsed") {
        updateFileData("parsed", currentPage);
      } else if ("not_parsed") {
        updateFileData("not_parsed", currentPage);
      } else if ("nil") {
        updateFileData("nil", currentPage);
      } else {
        updateFileData("alerady_exists", currentPage);
      }
    }
  }

  // function setActiveTab(mode) {
  //   activeTab = mode;
  // }
  function handlePrevClick() {
    if (currentPage - 1 >= 0) {
      currentPage -= 1;
      if ("parsed") {
        updateFileData("parsed", currentPage);
      } else if ("not_parsed") {
        updateFileData("not_parsed", currentPage);
      } else if ("nil") {
        updateFileData("nil", currentPage);
      } else {
        updateFileData("alerady_exists", currentPage);
      }
    }
  }
</script>

<main>
  <div class="container">
    <h3 class="mt-2">Upload files here...</h3>
    <div class="file-upload">
      <!-- File Type Dropdown -->
      <label for="filetype">File Type</label>
      <select id="filetype" class="file" bind:value={filetype} name="filetype">
        {#each options as o}
          <option value={o}>{o}</option>
        {/each}
      </select>

      <!-- File Upload Section -->
      <input type="file" name="uploadFile" id="fileupload" multiple required />
    </div>
    <button id="searchButton" class="upload" on:click={getjson}>Upload</button>
    {#if filestat}
      <div class="file-status">
        <div class="spinner-border text-success" role="status">
          <span class="sr-only">+</span>
        </div>
      </div>
    {:else}
      <p>{fileup}</p>
    {/if}
  </div>
  <div class="mt-4">
    <button
      class="btn btn-success"
      on:click={() => {
        updateFileData("parsed", currentPage);
      }}
      >Success Files {parsed_total}
    </button>
    <button
      class="btn btn-danger"
      on:click={() => {
        updateFileData("not_parsed", currentPage);
      }}
      >Failure Files {not_parsed_total}
    </button>
    <button
      class="btn btn-warning"
      on:click={() => {
        updateFileData("nil", currentPage);
      }}>Empty Files {nil_total}</button
    >
    <button
      class="btn btn-info"
      on:click={() => {
        updateFileData("already_exists", currentPage);
      }}>Duplicate Files {already_exist_total}</button
    >
    <input class="btn" type="date" bind:value={startdate} />
    <input class="btn" type="date" bind:value={lastdate} />
    <button class="btn btn-dark" on:click={updateFileData}>show</button>
    <div class="end-btn">
      <button class="button" on:click={handlePageView}>Page View</button>
      <button class="button" on:click={handleScrollView}>Scroll View</button>
    </div>
  </div>
  {#if showtable}
    {#if fileData.length > 0}
      <div class="table-responsive">
        <table class="table table-striped table-bordered">
          <thead class="thead-dark">
            <tr>
              <th>Filename</th>
              <th>Filetype</th>
              <th>Number/imei/cellid</th>
              <th>from date</th>
              <th>to date</th>
              <th>Parsing Status</th>
              <th>Inserted Rows</th>
              <th>Duplicates Rows</th>
              <th>Total Rows</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="search">
                <input
                  placeholder="search"
                  on:input={(event) => handleColumnSearch("filename", event)}
                />
              </td>
              <td class="search">
                <input
                  placeholder="search"
                  on:input={(event) => handleColumnSearch("filetype", event)}
                />
              </td>
              <td class="search">
                <input
                  placeholder="search"
                  on:input={(event) =>
                    handleColumnSearch("source_number", event)}
                />
              </td>
              <td class="search">
                <input
                  placeholder="search"
                  on:input={(event) => handleColumnSearch("from_date", event)}
                />
              </td>
              <td class="search">
                <input
                  placeholder="search"
                  on:input={(event) => handleColumnSearch("to_date", event)}
                />
              </td>
              <td class="search">
                <input
                  placeholder="search"
                  on:input={(event) =>
                    handleColumnSearch("parsing_status", event)}
                />
              </td>
              <td class="search">
                <input
                  placeholder="search"
                  on:input={(event) =>
                    handleColumnSearch("inserted_doc", event)}
                />
              </td>
              <td class="search">
                <input
                  placeholder="search"
                  on:input={(event) => handleColumnSearch("duplicates", event)}
                />
              </td>
              <td class="search">
                <input
                  placeholder="search"
                  on:input={(event) => handleColumnSearch("total_doc", event)}
                />
              </td>
            </tr>
            {#each fileData as _f}
              <tr>
                <td>{_f["filename"]}</td>
                <td>{_f["filetype"]}</td>
                <td>{_f["source_number"]}</td>
                <!-- <td>{changedateform(_f['from_date'])}</td> 
          <td>{changedateform(_f['to_date'])}</td> -->
                <td
                  >{#if "from_date" in _f}{changedateform(
                      _f["from_date"]
                    )}{/if}</td
                >
                <td
                  >{#if "to_date" in _f}{changedateform(_f["to_date"])}{/if}</td
                >
                <td>{_f["parsing_status"]}</td>
                <td>{_f["inserted_doc"]}</td>
                <td>{_f["duplicates"]}</td>
                <td>{_f["total_doc"]}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {:else}
      <div class="text-center mt-5">No Data</div>
    {/if}
    {#if pagination}
      <div class="pagination">
        {#if page_count > 1}
          <div class="pagination">
            <div class="flex items-center space-x-2">
              <button
                type="button"
                class="btn btn-sm btn-secondary"
                on:click={() => handlePageClick(1, mode)}
                disabled={currentPage === 1}>FIRST</button
              >
              <button
                type="button"
                class="btn btn-sm btn-secondary"
                on:click={() => handlePrevClick()}
                disabled={currentPage === 1}>{currentPage}</button
              >
              <button
                type="button"
                class="btn btn-sm btn-secondary"
                on:click={() => handleNextClick()}
                disabled={currentPage + 1 >= page_count}
                >{currentPage + 1}</button
              >
              <button
                type="button"
                class="btn btn-sm btn-secondary"
                on:click={() => handlePageClick(page_count - 1)}
                disabled={currentPage - 1 >= page_count}>LAST</button
              >
            </div>
          </div>
        {/if}
      </div>
    {/if}
  {/if}
</main>

<style>
  .btn {
    margin: 0rem 0.1rem;
  }
  .button {
    border: none;
    margin: 0.2rem;
    border-radius: 3px;
    font-size: 1rem;
    width: 15%;
    background-color: #0d6efd;
    color: #f1f1f1;
    transition: all 0.4s ease;
  }
  .button:hover {
    color: #0d6efd;
    background-color: #f1f1f1;
  }
  .end-btn {
    width: 46%;
    display: flex;
    justify-content: end;
  }
  .mt-4 {
    display: flex;
  }
  main {
    /* margin-left: 4%; */
    align-items: center;
    margin-top: 16px;
    box-shadow: 10px;
    width: 100%;
  }
  .container {
    background-color: rgba(198, 216, 207, 0.445);
    padding: 10px;
    box-sizing: border-box;
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    border-radius: 8px;
    box-shadow: 0 9px 10px 0 rgba(0, 0, 0, 0.4);
    width: 100%;
  }
  .file {
    height: 30px;
  }
  .file-upload {
    margin-top: 10px;
  }
  .upload {
    background-color: rgb(39, 201, 34);
    padding: 8px 15px;
    color: white;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    transition-duration: 0.4s;
    cursor: pointer;
    border: none;
    border-radius: 4px;
    position: relative;
    right: 20px;
    border-radius: 50px;
  }
  .file-status {
    display: flex;
    align-items: center;
    text-align: center;
  }

  .table-responsive {
    margin-top: 2%;
    width: 100%;
    margin-left: 0%;
    overflow-y: scroll;
  }
</style>
