<script>
  // @ts-nocheck
  
    import '../global.css';
    import {onMount , onDestroy} from 'svelte';
    import {goto} from '$app/navigation';
    import {basepath} from "$lib/config"
    import { userDetailsStore } from '$lib/datastore.js';
    import flatpickr from 'flatpickr';
    // import 'flatpickr/dist/flatpickr.min.css';
    import 'flatpickr/dist/flatpickr.css';
    import { createEventDispatcher } from 'svelte';
  
    let userDetails;
    userDetailsStore.subscribe(value => {
    userDetails = value;
    });
    onMount(() => {
    // beware of truthy and falsy values
    if (localStorage.getItem("userAuth")==="true"){
    userDetailsStore.set(JSON.parse(localStorage.getItem("userDetails")))
    fetchTickets(currentPage);
    }
    else{
    goto('/');
    }
    });

  let mindate;
  let formattedDate;
  const today = new Date();
  const month = String(today.getMonth() + 1).padStart(2, '0'); // Get the month (0-11) and add leading zero if necessary

  function updateFormattedDate() {
    // Date Formater Function
    const today1 = new Date();
    formattedDate = `${today1.getDate()}-${today1.getMonth() + 1}-${today1.getFullYear()}_${today1.getHours()}${today1.getMinutes()}${today1.getSeconds()}${today1.getMilliseconds()}`;
    formattedDate = formattedDate
  }
  mindate = `${String(today.getDate() + 1).padStart(2, '0')}/${month}/${2021}`;
    let cases = [];
    let result = [];
    let pagination = [];
    let currentPage = 1;
    let limit = 20; 
    let mainpage = '';
    function fetchTickets(page) {
      mainpage = page;
      NickName_data();
    }
  
    function nextPage() {
      if (currentPage < pagination.total_pages) {
        currentPage++;
        fetchTickets(currentPage);
      }
    }
  
    function prevPage() {
      if (currentPage > 1) {
        currentPage--;
        fetchTickets(currentPage);
      }
    }
  
    async function NickName_data() {
      const response = await fetch(basepath()+"/NickName_data", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email:userDetails.email,
          page:mainpage,
          limit:limit,
        }),
      });
      if (response.ok){
        const result = await response.json();
          console.log(result);
          if (result.my_data){
            cases = result.my_data;
            pagination = result.pagination;
          }
      }
    }
  
  let formattedDate1;
  const today1 = new Date();
  formattedDate1 = `${today1.getDate()}-${today1.getMonth() + 1}-${today1.getFullYear()}_${today1.getHours()}${today1.getMinutes()}${today1.getSeconds()}${today1.getMilliseconds()}`;
  formattedDate1 = formattedDate1
    let searchValue = "";
    async function search() {

          if (searchValue.trim() === "") {
                    // Reload the page if search value is empty
                    location.reload();
                    return;
                  }

      const response = await fetch(basepath()+"/nickname_search2", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({value: searchValue ,email:userDetails.email}),
      });
      if (response.ok){
        const result = await response.json();
          console.log(result);
          if (result.my_data){
            cases = result.my_data;
            pagination = result.pagination;
          }
      }
    }
    let file;
    function clear(){
      const fileInput = document.getElementById('excel_file');
      fileInput.value = '';
      file = {};
      file_data = '';
    }
    let file_data = '';
    const handleFileUpload = async (event) => {  // Excel File Upload Handler
      file = event.target.files[0];  
      const formData = new FormData();
      console.log(file)
      formData.append('file', file);
      formData.append('time', formattedDate1);
      formData.append('email', `${userDetails.email}`);
      const response = await fetch(basepath()+'/nickname_upload', {
        method: 'POST',
        body: formData,
      });
      if (response.ok) {
          file_data = await response.json();
          console.log(file_data);
    }
    }
  
    async function data_update(){
      const response = await fetch(basepath()+"/nickdata_update", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          data:file_data,
          update_date : new Date(),
        }),
      });
      clear();
      fetchTickets(currentPage);
    }
  
    async function sample_excel(){
        try {
        const response = await fetch(basepath() + '/nickname_excel')
            
        if (response.ok) {
          // Convert the response to a blob (binary data)
          const blob = await response.blob();
          
          // Create a URL for the blob data
          const url = window.URL.createObjectURL(blob);
    
          // Create a temporary anchor element to trigger the download
          const link = document.createElement('a');
          link.href = url;
          link.download = `sample_file.xlsx`; // Specify the desired filename
          link.style.display = 'none';
          document.body.appendChild(link);
          
          // Trigger the download
          link.click();
    
          // Clean up the URL and anchor element
          window.URL.revokeObjectURL(url);
          document.body.removeChild(link);
        } else {
          console.error('Failed to download Excel file.');
        }
        
      } catch (error) {
        console.error(error);
      }
      
    }
  
    let startDate;
    let endDate;
    let from_date = '';
    let to_date = ''
    function selected_period1(){
        const originalDate1 = new Date(startDate);  
      const date1 = originalDate1.toLocaleDateString('en-GB'); // Format to DD/MM/YYYY
    
      const originalDate2 = new Date(endDate);
      const date2 = originalDate2.toLocaleDateString('en-GB'); // Format to DD/MM/YYYY
    
     from_date = date1;
    to_date = date2;
  
      }
      async function date_filter (){
        const response = await fetch(basepath() + '/nickname_filter',{
          method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          from_date : from_date,
          to_date : to_date,
          email:userDetails.email,
         }),
      });
      if(response.ok){
        const result = await response.json();
        console.log(result);
          if (result.my_data){
            cases = result.my_data;
            pagination = result.pagination;
          }
      }
      }
    async function download_excel(){
      updateFormattedDate();
      const response = await fetch(basepath() + '/nickname_excel_download',{
          method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          data : cases,
         }),
      });
      if (response.ok) {
        // Convert the response to a blob (binary data)
        const blob = await response.blob();
        // Create a URL for the blob data
        const url = window.URL.createObjectURL(blob);
        // Create a temporary anchor element to trigger the download
        const link = document.createElement('a');
        link.href = url;
        link.download = userDetails.officername + '_' +userDetails.designation + "_" +formattedDate+ '.xlsx'; // Specify the desired filename
        link.style.display = 'none';
        document.body.appendChild(link);
        // Trigger the download
        link.click();
        // Clean up the URL and anchor element
        window.URL.revokeObjectURL(url);
        document.body.removeChild(link);
      } else {
        console.error('Failed to download Excel file.');
      }
    }
    async function deleteCase(phone) {
      // Send the phone number to the backend
      const response = await fetch(basepath() + '/delete_case', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ phone }),
      });
      if(response.ok){
        const messa = await response.json();
          alert(messa.message);
          fetchTickets(currentPage);
      }      
      console.log(messa.message); // Print the response message in the console
    }
  
    // edit option
    
    async function nickname_save(data){
      const response = await fetch(basepath() + '/nickname_save', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          phone : `${data.phone}`,
          nickname : `${data.nickname}`,
          id : `${data._id}`,

        }),
      });
      if(response.ok){
        const msg = await response.json();
          alert(msg.messege);
          fetchTickets(currentPage);

      }
    }

// refresh the page 
    function close(){
    window.location.reload();
  }
  </script>
  
  <style>
      a {
          text-decoration: none;
          cursor: pointer;
      }
  
      
      table, th, td {
          border-collapse: collapse;
          text-align: center;
          padding: 0.75rem;
      }
      
      h3 {
          margin-left: 20px;
          margin-top: 10px;
      }
       
      button {
          font-family: sans-serif;
      }
      .search_bar {
          display: flex;
          justify-content: space-between;
      }
      
      .search {
          margin-top: 10px;
          margin-right: 50px;
          height: 40px;
      }
      .page {
        position: fixed;
        bottom: 0;
        right: 0;
        margin: 5px; /* Adjust the margin as needed */
      }
      .selected{
        background-color: rgb(40, 139, 196);
        color: white;
      }
      .submit {
        margin-top: 15px;
        display: flex;
        margin-left: 580px;
      }
      
      .scroll-table1 {
        height: 647px;
        overflow: scroll;
      }
      
      .sticky-header {
      position: sticky;
      top: 0;
      background-color: #563d7c;
      color: white;
      z-index: 1000;
    }
    


    /* modal class */
  .modal-content {
    border-radius: 10px;
  }

  .modal-header {
    background-color: #007bff; 
    color: #fff; 
    border-radius: 10px 10px 0 0;
    font-family: serif;
  }

  .modal-body {
    padding: 20px;
    text-align: left; 
  }

  .modal-footer {
    justify-content: center; 
    border-radius: 0 0 10px 10px;
  }
  .col-form-label {
    font-weight: bold;
  }

  .form-control {
    border-radius: 5px;
    border-color: #ced4da;
  }

  .btn-custom {
    padding: 8px 12px;
    border-radius: 5px;
    transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
  }

  </style>
  
  
  <nav class="navbar navbar-dark bg-dark" style="background-color: #343a40 !important;">
      <div class="d-flex mr-1">
        <div class="bd-highlight">
          <button class="btn  btn-outline-dark mt-1 mr-1" style="color: #343a40;border-color: #343a40">
            <a href="/ticketing/" class="text-white"><i class="bi bi-house-door-fill"></i> Home</a></button>
          </div>  
      </div>
      <div class="pt-0 ">
        <div class="d-flex justify-content-end bd-highlight">
          <div class="p-2 bd-highlight">
            <div class="search-container">
            </div>
          </div>
          {#if userDetails.designation === 'Administrator'}
          <div class="p-2 bd-highlight">
            <button class='btn btn-outline-primary text-white' data-bs-toggle="tooltip" data-bs-placement="top" title='Download Sample Excel File For all Types' on:click={sample_excel}><i class="bi bi-file-earmark-spreadsheet-fill"></i> Sample Excel</button>
          </div>
  
  
          <div class="p-2 bd-highlight">
            <!-- <input accept="text/txt" bind:files id="avatar" name="avatar" type="file"/> -->
            <button class="btn btn-outline-warning" data-bs-toggle="modal" data-bs-target="#myModal">
              <a href="#" class="text-white">Update NickNames</a>
            </button>
            <div class="modal fade" id="myModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
              <div class="modal-dialog" style="max-width: 1400px;margin-top:70px">
                <div class="modal-content">
                  <div class="modal-header">
                    <h1 class="modal-title fs-5" style="font-size: 1.25rem;font-weight: 500;margin-bottom: 0; line-height: 1.5;font-family: sans-serif;" id="exampleModalLabel">Upload your File</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" on:click={clear}></button>
                  </div>
                  <div class="modal-body">
                    <div class="btn-group">
                      <input class="form-control" style="border-radius: 40px 0 0 40px; width: 400px;margin-left: 440px;margin-bottom: 20px" type="file" accept=".csv,.xlsx, .xls" on:change={handleFileUpload} id="excel_file" />
                      <button class="btn btn-outline-danger" style="border-radius: 0 40px 40px 0;cursor: pointer;height: 40px;width: 64px;margin-bottom: 20px" type="button" on:click={clear}><i class="bi bi-x-circle"></i></button>
                  </div>
                  {#if file_data !== ''}
                  <div class="table-responsive text-nowrap scroll-table1">
                    <table class="table table-striped table-hover" id="mytb">
                      <thead class="table-dark" id="myhead">
                        <tr>
                          <td>Phone</td>
                          <td>Nickname</td>
                          <td>Officername</td>
                          <td>Team</td>
                        </tr>
                      </thead>
                      {#each file_data as data}
                      <tr>
                        <td>{data.phone}</td>
                        <td style="width: 100px !important;">{data.nickname}</td>
                        <td>{data.officername}</td>
                        <td>{data.team}</td>
                    </tr>
                      {/each}
                    </table>
                  </div>
                  {/if} 
                    <button type="button"  data-bs-dismiss="modal" on:click={data_update} class="submit btn btn-outline-success">Update</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          {/if}
      </nav>
  <main>
  
      <div>
          <h3 style="font-weight: bold;">{userDetails.officername}</h3>
          <p style="margin-left: 20px;margin-top: 10px;">{userDetails.designation}</p>
      </div>
      <div>
        <input class="border-0" style="text-align: left; margin-left:10px" use:flatpickr={{mode:'range', dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',onChange:(selectedDates) => {startDate = selectedDates[0];endDate = selectedDates[1];}}}  
        on:input={selected_period1(startDate,endDate)} placeholder="Select Range" id="dateRangePicker">
       <button class="btn btn-outline-warning" on:click={()=> date_filter()}><i class="bi bi-funnel-fill"></i></button> 
       <button class="btn btn-outline-success" on:click={()=> download_excel()}><i class="bi bi-file-earmark-spreadsheet-fill"></i>As Excel</button> 
  
      </div>
      <div class="search_bar">
          {#if userDetails.role !== "Logger" || userDetails.designation !== "SI" || userDetails.role === "Analyst"}
          <h2 style="font-size: 2rem;"></h2>
          {/if}
          <div class="search btn-group" style='margin-bottom: 10px;margin-right: 28px'>
            <input type="search" style="border-radius: 40px 0 0 40px" bind:value={searchValue} placeholder="Search Data">
            <button class="btn btn-outline-primary" style="border-radius: 0 40px 40px 0;cursor: pointer;height: 40px;width: 64px;margin: 0;" type="button" on:click={() => search()}><i class="bi bi-search"></i></button>
        </div>
      </div>
      <div class="table-responsive text-nowrap scroll-table1">
          <table class="table table-striped table-hover" id="mytb" style="border-collapse: collapse;">
              <thead class="table-dark" id="myhead">
                  <tr>
                      <th>Phone No.</th>
                      <th>Nickname</th>
                      <th>Officer Name</th>
                      <th>Team</th>
                      <th>Created on</th>
                      <th>Updated on</th>
                      {#if userDetails.designation === 'Administrator'}
                      <th>Action</th>
                      {/if}
                  </tr>
              </thead>
              {#each cases as data}
              <tr>
                  <td>{data.phone}</td>
                  <td style="width: 100px !important;">{data.nickname}</td>
                  <td>{data.officername}</td>
                  <td>{data.team}</td>
                  <td>{data.created_on}</td>
                  {#if data.hasOwnProperty('updated_on')}
                  <td>{data.updated_on}</td>
                  <!-- <td><button on:click={() => deleteCase(data.phone)}>Delete</button></td> -->
                  {#if userDetails.designation === 'Administrator'}
                  <td>
                    <button class="btn btn-outline-warning " type="button" data-bs-toggle="modal" data-bs-target="#records{data._id}">
                      Edit
                    </button>
                    <div class="modal fade bd-example-modal-lg" id="records{data._id}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                      <div class="modal-dialog modal-dialog-centered modal-xl" >
                        <div class="modal-content" >
                          <div class="modal-header"><h3 style="font-weight: bold;">Edit Nickname Details</h3>
                            <button type="button" class="cross btn-close" data-bs-dismiss="modal" aria-label="Close" on:click={close}></button>
                          </div>
                          <!-- <div class="modal-header"><h5>{data.phone}</h5></div> -->
                          <div class="modal-body" style="text-align: left;">
                            <div class="d-flex">
                                  <div>
                                    <label class="col-sm-3 col-form-label">Phone</label>
                                    <input class="col-sm border-0" bind:value={data.phone}>
                                  </div>
                                  <div>
                                    <label class="col-sm-3 col-form-label">Nickname</label>
                                    <input class="col-sm border-0" bind:value={data.nickname}>
                                  </div>
                            </div>
                            <div class="modal-footer">
                              <button class="btn btn-outline-success" data-bs-dismiss="modal" on:click={()=> nickname_save(data)} >Save</button>
                            </div>
                    </div>
                    </div>
                    </div>
                    </div>
                    <button class="btn btn-outline-danger" on:click={() => deleteCase(data.phone)}>Delete</button>
                  </td>
                  {/if}
                  <!-- <td><button>delete</button></td> -->
                  {:else}
                  <td>-</td>
                  {/if}
              </tr>
              {/each}
          </table>
        </div>

        <div class="page d-flex justify-content-end mr-5" style="margin-right:50px">
          <nav aria-label="Page navigation">
            <ul class="pagination d-flex justify-content-end">
              <p class="mr-3 mt-2" style="margin-right:15px">Showing {cases.length} out of {pagination.total_tickets} rows</p>
              <li class="page-item">
                <button class="page-link" on:click={() => fetchTickets(currentPage)}>First</button>
              </li>
              <li class="page-item">
                <button class="page-link" aria-label="Previous" on:click={prevPage} disabled={currentPage === 1}>
                  <span aria-hidden="true">&laquo;</span>
                </button>
              </li>
              {#each Array.from({ length: Math.min(pagination.total_pages, 5) }, (_, i) => i + 1 + (currentPage > 5 ? currentPage - 5 : 0)) as page}
                <li class="page-item">
                  <button class="page-link {page === currentPage ? 'selected' : ''}" on:click={() => fetchTickets(page)}>{page}</button>
                </li>
              {/each}
              <li class="page-item">
                <button class="page-link" aria-label="Next" on:click={nextPage} disabled={currentPage === pagination.total_pages}>
                  <span aria-hidden="true">&raquo;</span>
                </button>
              </li>
              <li class="page-item">
                <button class="page-link" on:click={() => fetchTickets(pagination.total_pages)}>Last</button>
              </li>
            </ul>
          </nav>
        </div>
  
              
  </main>
  