<script>
  // @ts-nocheck

  import { basepath } from "$lib/config";
  import { getRequest,postRequest } from "$lib/req_utils";
  import {onMount,onDestroy} from 'svelte';
  import { writable } from 'svelte/store';

  
  // // Calculate the progress percentage
  // $: progressPercentage = (currentCount / totalCount) * 100;
  let processdata;
  let filetype = "";
  let res;
  let filestat = false;
  let fileup = "";
  let username = "test";
  let provider;
  let fileData;
  let showtable = false;
  let parsedfiles = [];
  let notparsed = [];
  let nil_data = [];
  let alredyexists = [];
  let startdate;
  let lastdate;
  let alreadyexists = [];
  let columnFilters = {};

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
  let getprogress = false;
  let fileupdates


  
  // const currentDate = new Date();
  // lastdate = currentDate.toISOString().split('T')[0];
  let undefined_files_count = 0;
  const undefinedFiles = writable([]);


  let current_page = 1;
  let loading = false;
  let allFilesLoaded = false;


  let scrollContainer;

  $: {
    if (scrollContainer) {
      console.log('Scroll container is now defined, adding event listener');
      scrollContainer.addEventListener('scroll', handleScroll);

      // Cleanup function to remove event listener when scrollContainer is no longer valid or component is destroyed
      onDestroy(() => {
        scrollContainer.removeEventListener('scroll', handleScroll);
        console.log('Event listener removed');
      });
    } else {
      console.log('Scroll container is still undefined');
    }
  }

  // onMount(() => {
  //   console.log('Component mounted');
  //   if (scrollContainer) {
  //     console.log('Scroll container is defined, adding event listener');
  //     scrollContainer.addEventListener('scroll', handleScroll);
  //   } else {
  //     console.log('Scroll container is undefined at mount');
  //   }
  // });

  // onDestroy(() => {
  //   if (scrollContainer) {
  //     scrollContainer.removeEventListener('scroll', handleScroll);
  //   }
  // });

  function handleScroll() {
    const { scrollTop, scrollHeight, clientHeight } = scrollContainer;
    console.log(`Scrolled: scrollTop=${scrollTop}, scrollHeight=${scrollHeight}, clientHeight=${clientHeight}`);
    if (scrollTop + clientHeight >= scrollHeight - 50) {
      console.log('Near bottom - implement logic to fetch more data here');
      fetchUndefinedFiles(); 
    }
  }

  function handlePageView() {
    page_view = true;
    pagination = true;
    currentPage = 1;
    itemsPerPage = 10;
    updateFileData("parsed");
  }

  function fileupdate(){

    // fetch(`${basepath()}/fileupdate`,{
    //   method:'get'
    // })

    const url = `${basepath()}/fileupdate`;
    getRequest(fetch,url)

    .then(res => res.json())
    .then(data => {
      console.log(data)
      getprogress =  data.showprogress

      fileupdates = data.data
      console.log(fileupdates)

    })
  }
  fileupdate()
  
  // function progresbr(){
  //   if(getprogress === 'true'){
  //     setInterval(fileupdate, 3000)
  //     // fileupdate()

  //   }
  // }

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
        formData.append("filetype", "zip");
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
          console.log(filestat);
          if (res === "success") {
            filestat = false;
            fileup = "Upload Success";
            updateFileData();
            fileupdate()
          } else {
            filestat = false;

            alert(res);
          }
        })
        .catch((err) => {
          console.log(err);
          alert(err);
        });
    }
  }

  function updateFileData(mode, currentPage) {
    // fetch(`${basepath()}/filestatus`, {
    //   method: "post",
    //   body: JSON.stringify({
    //     startdate: startdate,
    //     enddate: lastdate,
    //     mode: "automation",
    //     page_view: page_view,
    //     currentpage: currentPage,
    //     items: itemsPerPage,
    //   }),
    const body = {
        startdate: startdate,
        enddate: lastdate,
        mode: "automation",
        page_view: page_view,
        currentpage: currentPage,
        items: itemsPerPage,
      }
    const url = `${basepath()}/filestatus`;
    postRequest(fetch,url,body)
      .then((data) => {
        console.log(data, "status");
        if (data.status === "success") {
          if (data.data.parsed && data.data.parsed.data) {
            parsed_total = data.data.parsed.total_pages;
            parsedfiles = Object.values(data.data.parsed.data);
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
          // Update total pages
          console.log(data.data.total_pages, "total pages");

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
            fileData = notparsed;
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
    updateFileData("parsed");
  }

  //  setInterval(updateFileData, 3000)
  updateFileData("parsed");

 

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
      updateFileData(currentPage);
    }
  }

  function handleNextClick() {
    if (currentPage + 1 < page_count) {
      currentPage += 1;
      updateFileData(currentPage);
    }
  }

  function handlePrevClick() {
    if (currentPage - 1 >= 0) {
      currentPage -= 1;
      updateFileData(currentPage);
    }
  }

  






  // async function fetchUndefinedCount() {
  //   try {
  //     const response = await fetch(`${basepath()}/get_undefined_count`);
  //     if (!response.ok) {
  //       throw new Error('Failed to fetch count from backend');
  //     }
  //     const data = await response.json();
  //     undefined_files_count = data.count

  //   } catch (error) {
  //     console.error(error);
  //   }
  // }

  function fetchUndefinedCount() {
  // fetch(`${basepath()}/get_undefined_count`)
  const url = `${basepath()}/get_undefined_count`;
    getRequest(fetch,url)
    .then((data) => {
      undefined_files_count = data.count;
      console.log("Undefined files count:", undefined_files_count);
    })
    .catch((error) => {
      console.error("Error fetching undefined count:", error);
    });
}


  
  // async function fetchUndefinedFiles(){

  //   try {
  //     const response = await fetch(`${basepath()}/get_undefined_files`);
  //     if (!response.ok) {
  //       throw new Error('Failed to fetch count from backend');
  //     }
  //     const data = await response.json();
  //     undefinedFiles.set(data);

  //     console.log(data)
  //   } catch (error) {
  //     console.error(error);
  //   }
  // }


  // working with async fetch
//   async function fetchUndefinedFiles() {
//   if (loading || allFilesLoaded) return;

//   loading = true;
//   try {
//     const response = await fetch(`${basepath()}/get_undefined_files?page=${current_page}`);
//     if (!response.ok) {
//       throw new Error('Failed to fetch files from backend');
//     }
//     const newData = await response.json();
//     if (newData.length > 0) {
//       undefinedFiles.update(current => [...current, ...newData]);
//       // console.log($undefinedFiles.length,"oojojo")
//       current_page++;
//     } else {
//       allFilesLoaded = true;
//     }
//   } catch (error) {
//     console.error(error);
//   } finally {
//     loading = false;
//   }
// }

function fetchUndefinedFiles() {
  if (loading || allFilesLoaded) return;

  loading = true;

  // fetch(`${basepath()}/get_undefined_files?page=${current_page}`)
  const url = `${basepath()}/get_undefined_files?page=${current_page}`;
    getRequest(fetch,url)
    
    .then((newData) => {
      if (newData.length > 0) {
        undefinedFiles.update((current) => [...current, ...newData]);
        current_page++;
      } else {
        allFilesLoaded = true;
      }
    })
    .catch((error) => {
      console.error("Error fetching undefined files:", error);
    })
    .finally(() => {
      loading = false;
    });
}








  // function selectFileName(file) {
  //   const filename = file.filename;
  //   const filepath = file.file_path;

  //   fetch(`${basepath()}/getfile?filename=${filename}&filepath=${filepath}`)
  //     .then(response => {
  //       if (!response.ok) {
  //         throw new Error('Failed to get file from backend');
  //       }
  //     })
  //     .catch(error => {
  //       console.error(error);
  //     });
  // }


  function selectFileName(file) {
  const filename = file.filename;
  const filepath = file.file_path;

  const link = document.createElement('a');
  link.href = `${basepath()}/getfile?filename=${filename}&filepath=${filepath}`;
  link.download = filename;
  link.target = '_blank'; 
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link); 
}


function uploadSelectedFiles() {
    const selectedFiles = [];
    const selectElements = document.querySelectorAll('select');
    selectElements.forEach((select, index) => {
      const selectedValue = select.options[select.selectedIndex].value;
      if (selectedValue !== 'none') {
        const filename = $undefinedFiles[index].filename;
        const filepath = $undefinedFiles[index].file_path;
        const fuuid = $undefinedFiles[index].fuuid
        selectedFiles.push({ filename, filepath, fuuid, fileType: selectedValue });
      }
    });

    if (selectedFiles.length > 0) {
      console.log(selectedFiles)
      // fetch(`${basepath()}/upload_files`, {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json'
      //   },
      //   body: JSON.stringify(selectedFiles)
      // })
    const url = `${basepath()}/upload_files`;
    postRequest(fetch,url,JSON.stringify(selectedFiles))


      .then(response => {
        console.log(response)
        if (!response.ok) {
          throw new Error('Failed to upload files to backend');
        }
        // Handle success response
      })
      .catch(error => {
        console.error(error);
      });
    }
  }

  onMount(fetchUndefinedCount);
  
</script>

<main>
  <div class="row">
    <div class="col-10">

      <div class="container">
        <h3 class="mt-2">Upload Zip files here...</h3>
        <div class="file-upload">
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
      >Success files {parsed_total}
    </button>
    <button
    class="btn btn-danger"
    on:click={() => {
      updateFileData("not_parsed");
    }}
      >Failure files {(not_parsed_total, currentPage)}
    </button>
    <button
    class="btn btn-warning"
    on:click={() => {
      updateFileData("nil");
    }}>Empty files {(nil_total, currentPage)}</button
    >
    <button
      class="btn btn-info"
      on:click={() => {
        updateFileData("already_exists");
      }}>Dupilcate Files {(already_exist_total, currentPage)}</button
    >

    <!--  for undefined button -->

    <button class="btn btn-outline-danger" on:click = {fetchUndefinedFiles}>Undefined Files : { undefined_files_count } </button>

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
            on:click={() => handlePageClick(1)}
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
    </div>
    <!-- {#if getprogress}
    <div class="col-2">
      <div class="parsingstat">
        {#each fileupdates as fu}
        <p>{fu.filename}</p>
        <div class="progress-bar">
            <div class="progress " style="width: {fu.pendingcounts/ fu.filecounts * 100}%;">
                {fu.pendingcounts} / {fu.filecounts}
            </div>
        </div>
    {/each}
    
  </div>
</div>
{/if} -->
    </div>


    
    
    <!-- {#if $undefinedFiles.length > 0}
    
     <h1>Undefined Files</h1>
    <button on:click={uploadSelectedFiles} class="upload-button">Upload</button>

    <table id="undefined-files-table">
      <thead>
        <tr>
          <th>File Name</th>
          <th>File Type</th>
        </tr>
      </thead>
      <tbody>
        {#each $undefinedFiles as file}
          <tr>
            <td >
              <span class="downloadable" on:click={() => selectFileName(file)}>{file.filename}</span>
            </td>
              <td>
              <select>
                <option value = 'none'>Select Type</option>
                <option value="cdr">CDR</option>
                <option value="ipdr">IPDR</option>
                <option value="rh">RH</option>

              </select>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if} -->

<!-- for lazy loading -->



{#if $undefinedFiles.length > 0}
<h1>Undefined Files</h1>
<button on:click={uploadSelectedFiles} class="upload-button">Upload</button>

<div class="table-container">
  <table id="undefined-files-table">
    <thead>
      <tr>
        <th>File Name</th>
        <th>File Type</th>
      </tr>
    </thead>
    <tbody bind:this={scrollContainer}>
      {#each $undefinedFiles as file}
        <tr>
          <td>
            <span class="downloadable" on:click={() => selectFileName(file)}>{file.filename}</span>
          </td>
          <td>
            <select>
              <option value='none'>Select Type</option>
              <option value="cdr">CDR</option>
              <option value="ipdr">IPDR</option>
              <option value="rh">RH</option>
            </select>
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>
{/if}


    </main>
    
    <style>

.scroll-container {
    border: 1px solid #ccc; /* For visibility */
  }

.scroll-container {
  max-height: 500px; 
  overflow-y: auto;
}

.scroll-container {
    max-height: 500px; 
    overflow-y: auto;
    overflow-x: hidden;
  }

.upload-button{
  margin-left: 1130px;
}

.downloadable {
    color: rgb(58, 58, 176);
    cursor: pointer; /* Optional: Change cursor to pointer to indicate it's clickable */
  }

.container {
    max-height: 400px; 
    overflow-y: auto;
  }

#undefined-files-table {
    width: 100%;
    /* border-collapse: collapse; */
  }
  #undefined-files-table th, #undefined-files-table td {
    border: 1px solid black;
    padding: 8px;
    text-align: left;
  }
  #undefined-files-table th {
    background-color: #f2f2f2;
  }
  #undefined-files-table tr:nth-child(even) {
    background-color: #f2f2f2;
  }


      .btn {
    margin: 0rem 0.1rem !important;
  }
  .mt-4 {
    display: flex;
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
  main {
    /* margin-left: 4%; */
    align-items: center;
    margin-top: 16px;
    box-shadow: 10px;
    width: 70%;
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
  /* .file {
    height: 30px;
  } */
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
  .parsingstat{
    height: 80vh;
    width: 50vw;
    background-color: rgb(243, 245, 245);
  }
  .progress-bar {
    width: 90%;
    height: 20px;
    background-color: #ece6e6;
    border-radius: 4px;
    overflow: hidden;
  }

  .progress {
    height: 100%;
    background-color: #007bff;
    border-radius: 4px;
    transition: width 0.3s ease-in-out;
  }



  .table-container {
  width: 100%;
  overflow: hidden;
}

#undefined-files-table {
  width: 100%;
  table-layout: fixed;
  /* border-collapse: collapse; */
}

#undefined-files-table thead th {
  position: sticky;
  top: 0;
  background: white;
  z-index: 1;
}

#undefined-files-table tbody {
  display: block;
  max-height: 400px;
  overflow-y: scroll;
}

#undefined-files-table thead,
#undefined-files-table tbody tr {
  display: table;
  width: 100%;
  table-layout: fixed;
}

#undefined-files-table tbody td {
  word-break: break-word;
}


#undefined-files-table th,
#undefined-files-table td {
  border: 1px solid #dee2e6;
  padding: .75rem; 
}

#undefined-files-table th:last-child,
#undefined-files-table td:last-child {
  border-right: none; 
}




</style>
