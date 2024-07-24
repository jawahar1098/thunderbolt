<script>
  // @ts-nocheck
    import '../global.css';
    import {
      onMount
    } from 'svelte';
    import {
      goto
    } from '$app/navigation';
    import {
      basepath
    } from "$lib/config"
    import { userDetailsStore } from '$lib/datastore.js';
    import flatpickr from 'flatpickr';
  import 'flatpickr/dist/flatpickr.css';
  
  let mindate;
  const today = new Date();
  
  const year = today.getFullYear(); // Get the four-digit year
  const month = String(today.getMonth() + 1).padStart(2, '0'); // Get the month (0-11) and add leading zero if necessary
  const day = String(today.getDate()).padStart(2, '0'); // Get the day of the month and add leading zero if necessary
  
  const formattedDate = `${day}/${month}/${year}`; // Create the formatted date string
  let dateString = '01/12/2023';
  let dayValue = dateString.split('/')[0];
  mindate = `${String(today.getDate() + 1).padStart(2, '0')}/${month}/${2021}`;
  
  let userDetails;
  
  userDetailsStore.subscribe(value => {
  userDetails = value;
  // console.log("value",value)
  });
  
  
  // console.log("demo",userDetails);
  onMount(() => {
  // beware of truthy and falsy values
  if (localStorage.getItem("userAuth")==="true"){
  // console.log("jsno",localStorage.getItem("userDetails"))
  // console.log('auth is passed')
  userDetailsStore.set(JSON.parse(localStorage.getItem("userDetails")))
  // console.log(userDetails)
  selected_period('');
  }
  else{
  goto('/');
  }
  })
  
  let cases =[];
  let types = 'All';
  let requesttype = '';
  let teams = '';
  let period_data = ''
  let ISP = ''
  let officer = ''
  let officers = []
  let status = 'All';



let date_range = ''
  // Add a loading state
let isLoading = false;

async function report() {
  try {
    // Set loading to true when starting the request
    isLoading = true;
    const response = await fetch(basepath() + '/report', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        team: userDetails.team,
        category:requesttype,
        designation: userDetails.designation,
        role: userDetails.role,
        email: userDetails.email,
        modules: userDetails.modules,
        types: types,
        teams: teams,
        period: period_data,
        date_range: date_range,
        ISP: ISP,
        officer:officer
      })
    });

    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }

    if (response.ok) {
      cases = await response.json();
      console.log(cases)
    }
  } catch (error) {
    console.error(error);
  } finally {
    // Set loading to false when the request is completed, regardless of success or failure
    isLoading = false;
    // Call your function to update the loading spinner state
    updateLoadingSpinner();
  }

}

function updateLoadingSpinner() {
  // Implement logic to show/hide loading spinner based on the isLoading state
  const loadingSpinner = document.getElementById('loadingSpinner'); // Replace 'loadingSpinner' with the actual ID or class of your loading spinner element
  if (isLoading) {
    loadingSpinner.style.display = 'block'; // Show the loading spinner
  } else {
    loadingSpinner.style.display = 'none'; // Hide the loading spinner
  }
}

  
  onMount(() => {
    // beware of truthy and falsy values
    if (localStorage.getItem("userAuth") === "true") {
      // console.log('auth is passed')
      // allinONE()
      report()
      // data_filters()
    } else {
      goto('/');
    }
  })
  
  async function fetch_officers(){
    const response = await fetch(basepath() + '/fetch_officers', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        team: userDetails.team,
        designation: userDetails.designation,
        role: userDetails.role,
        email: userDetails.email,
        modules: userDetails.modules,
      })
    });
    if (response.ok) {
      officers = await response.json();
      console.log(officers)
    }
  }
  

  function selected_period(period){
    startDate = ''
    endDate = ''
    const dateRangePickerInput = document.getElementById("dateRangePicker");
      if (dateRangePickerInput) {
        dateRangePickerInput.value = "";
      }
    if (period === 'All' || period === ''){
      period_data = 'All';
    }
    else{
      period_data = period;
      
    }
    selected_period1();
  }
  
  let startDate;
  let endDate;
    function selected_period1(){
      const originalDate1 = new Date(startDate);
    const date1 = originalDate1.toLocaleDateString('en-GB'); // Format to DD/MM/YYYY
  
    const originalDate2 = new Date(endDate);
    const date2 = originalDate2.toLocaleDateString('en-GB'); // Format to DD/MM/YYYY
  
    const rangeStartDate = date1;
    const rangeEndDate = date2;
    if (date1 !== 'Invalid Date' && date2 !== 'Invalid Date'){
      period_data = `${date1} to ${date2}`;
      date_range = 'Date Range';
  
      
    }
    }


    let currentPage = 1;
    let limit = 6; // Adjust this based on your backend configuration
    let pagination = '';
    let mainpage = '';
      async function fetchTickets(page) {
        mainpage = page;
        data_filters();
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
  let result = '';
  async function fetch_dash(user){
    const response = await fetch(basepath() + '/dashboardresult', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              id:`${user._id}`,
              reqt:`${user.requesttype}`,
              reqc:`${user.requestcategory}`,
              sub:`${user.subtypes}`,

              })
          });
          result = await response.json();
          console.log(result,'//////')
    }




  let filter_data = [];
  async function data_filters(){
    try {
      const response = await fetch(basepath() + '/data_filters', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          team : userDetails.team,
          category:requesttype,
          designation : userDetails.designation,
          role : userDetails.role,
          email : userDetails.email,
          module: userDetails.modules,
          types:types,
          teams:teams,
          officer:officer,
          status:status,
          page:mainpage,
          limit:limit,
          period:period_data,
          date_range:date_range
        })
      });
      if (response.ok){
            const result = await response.json();
              console.log(result,'///////////////////////');
              if (result.mytickets){
                filter_data = result.mytickets;
                pagination = result.pagination;
              }
          }

    } catch (error) {
      console.error(error);
    }
    report();
    isLoading = false;
  }
    async function download(){
      try {
      const response = await fetch(basepath() + '/dashexcel', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            cat : requesttype,
            reqtype : types,
            status : status,
            daterange : period_data,
            data:cases,
            tabledata:filter_data
        })
      });
          
      if (response.ok) {
        // Convert the response to a blob (binary data)
        const blob = await response.blob();
        
        // Create a URL for the blob data
        const url = window.URL.createObjectURL(blob);
  
        // Create a temporary anchor element to trigger the download
        const link = document.createElement('a');
        link.href = url;
        link.download = `${userDetails.officername}_${userDetails.team}_${userDetails.designation}_report.xlsx`; // Specify the desired filename
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
    let searchValue = "";
    let searchResults;
    async function search(type) {
      const response = await fetch(basepath()+"/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({type:type, value: searchValue ,email:userDetails.email}),
      });
      searchResults = await response.json();
      console.log(searchResults,'//////')
      filter_data = searchResults;
  
    }
  let selectedOption = 'Select';// Default selected option
  function handleOptionSelect(option) {
      selectedOption = option;
      // Perform any action based on the selected option here
  }

async function generatePDF() {
  const date = document.getElementById(`date`)
  date.style.display = 'block';
  if(requesttype === 'Data Request'){
    const content1 = document.querySelector("#pdftable .table-container:nth-child(1)");
    const content2 = document.querySelector("#pdftable .table-container:nth-child(3)");
    // Combine contents into one container
    const combinedContent1 = document.createElement('div');
    combinedContent1.style.width = '80%';
    combinedContent1.style.height = '800px';
    combinedContent1.style.display = 'flex';
    combinedContent1.style.justifyContent = 'center';
    combinedContent1.style.marginLeft = '100px';
    combinedContent1.style.marginTop = '50px';

  
    combinedContent1.appendChild(content1.cloneNode(true));
  
    const combinedContent2 = document.createElement('div');
    combinedContent2.style.width = '80%';
    combinedContent2.style.display = 'flex';
    combinedContent2.style.justifyContent = 'center';
    combinedContent2.style.marginLeft = '100px';
    combinedContent2.appendChild(content2.cloneNode(true));
  
    const combinedContent3 = document.createElement('div');
    combinedContent3.appendChild(combinedContent1.cloneNode(true));
    combinedContent3.appendChild(combinedContent2.cloneNode(true));
  
    const pdfOptions = {
      margin: [0.2, 0.2, 0.2, 0.2], // [top, right, bottom, left] margins
      filename: `Data_request_report.pdf`,
      image: { type: "jpeg", quality: 190 },
      html2canvas: { scale: 1.0 },
      jsPDF: { unit: "cm", format: "a4", orientation: "landscape" },
    };
  
    await html2pdf().from(combinedContent3).set(pdfOptions).save();
  }
  else if (requesttype === 'Analysis Request'){
    const content1 = document.querySelector("#pdftable .table-container:nth-child(2)");
    // Combine contents into one container
    const combinedContent1 = document.createElement('div');
    combinedContent1.style.width = '80%';
    combinedContent1.style.height = '700px';
    combinedContent1.style.display = 'flex';
    combinedContent1.style.justifyContent = 'center';
    combinedContent1.style.marginLeft = '100px';
  
    combinedContent1.appendChild(content1.cloneNode(true));

    const combinedContent3 = document.createElement('div');
    combinedContent3.appendChild(combinedContent1.cloneNode(true));
  
    const pdfOptions = {
      margin: [0.2, 0.2, 0.2, 0.2], // [top, right, bottom, left] margins
      filename: `Analysis_request_report.pdf`,
      image: { type: "jpeg", quality: 190 },
      html2canvas: { scale: 1.0 },
      jsPDF: { unit: "cm", format: "a4", orientation: "landscape" },
    };
  
    await html2pdf().from(combinedContent3).set(pdfOptions).save();
  }
  date.style.display = 'none';
}
   </script>
  <style>
    
  h3{
  margin-left: 50px;
  margin-top: 10px;
  }
  
  
  .main_content{
    /* border: 1px solid lightgray; */
    border-top: none;
    background:linear-gradient(#EEEEEE, #FAF8F9, #FFFFFF);
    height: 80px
  }
  .inner_tab{
    border-top: none;
    margin-left: 20px;
    margin-bottom: 20px;
  }

  #mytb , tr{
    border-bottom: 1px solid lightgray;
    border-left: 1px solid lightgray;
    border-right: 1px solid lightgray;
  
  }
  #mytb1{
    box-shadow: 0 .5rem 3rem rgb(0, 0, 0)!important;    
    /* border-radius: 20px; */
    border-top-left-radius: 20px;
    margin-bottom: 50px;
  }
  table, th, td {
  border-collapse: collapse;
  text-align: center;
  padding: 0.75rem;
  border-top: 1px solid #dee2e6;
  }
  .types{
    background: white;
    border-radius:10px;
    width:200px;
    height:37px;
    margin-bottom:15px;
    margin-top:20px;
    /* margin-left: 150px; */
  }
  .Success {
      color: green;
      font-weight: 500;
      text-align: center;
      vertical-align: middle;
    }
  
    .Rejected {
      color: red;
      font-weight: 500;
      text-align: center;
    vertical-align: middle;
    }
    .scroll-table1 {
      height: 500px; 
      overflow: scroll;
  }
  main{
    background-image: url("../src/public/Images/rpt3.jpg");
    background-repeat: no-repeat;
    background-size: cover;
    background-color: aliceblue;
  
  }

  .table-container {
    margin-bottom: 50px;
  }
    #myhead1 th {
    /* background-color: #343a40; */
    color: #000000;
    /* width: 324px; */
  }

  #mytb1 td:nth-child(1) {
    background-color: #d2b3eb;
  }
  .selected{
      background-color: rgb(40, 139, 196);
      color: white;
    }

  #date {
    display: none; 
    margin-bottom: -28px;
  }
 
    .table_heading-2 {
        font-family: 'Arial', sans-serif; 
        font-size: 24px; 
        color: #ff4500; 
        text-transform: uppercase; 
        letter-spacing: 2px; 
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); 
        margin-bottom: 10px;
        margin-left: 240px; 
      }
      .table_heading {
        font-family: 'Arial', sans-serif; 
        font-size: 24px; 
        color: #ff4500; 
        text-transform: uppercase; 
        letter-spacing: 2px; 
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); 
        margin-bottom: 10px;
        margin-left: 80px;
      }
      .table_heading-3 {
        margin-left: 170px; 
        font-family: 'Arial', sans-serif; 
        font-size: 24px; 
        color: #ff4500; 
        text-transform: uppercase; 
        letter-spacing: 2px; 
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); 
        margin-bottom: 10px;
      }

  
  </style>
  <main>
    <div style="background-color: aliceblue; height:90px;">
      <h3 style="font-weight: bold;background:aliceblue;">{userDetails.officername}</h3>
      <p style="margin-left: 50px;margin-top: 10px;">{userDetails.team} Team, {userDetails.designation}</p>
  </div>
    <div class="main_content">
    <div class="inner_tab">
      <div class="tab-content" id="myTabContent">
        <!-- Data Requests Tab content -->
        <div class="filters">
              <div class="tab-pane fade show active" id="data-Requests" role="tabpanel" aria-labelledby="data-Requests-tab">
                <select class="types" bind:value={requesttype} on:change={()=> report()}>
                  <option selected value="" >Requests Category</option>
                  <option value="Data Request">Data Request</option>
                  <option value="Analysis Request">Analysis Request</option>
                </select>

                {#if userDetails.designation === 'SP' && userDetails.team === 'ADMIN'}
                  <select style="background: white;border-radius:10px;width:130px;height:37px" bind:value={teams}>
                    <option selected value="" >Teams</option>
                    <option value="All">All</option>
                    <option value="AP">AP</option>
                    <option value="CAT"> CAT</option>
                    <option value="ISOT"> ISOT</option>
                  </select>
                {/if}
                {#if userDetails.role !== 'Analyst' && userDetails.role !== 'Mailer' && userDetails.role !== 'Logger'}
                  <select style="background: white;border-radius:10px;width:200px;height:37px" on:mouseenter={fetch_officers} bind:value={officer}>
                    <option value="" >Officers</option>
                    <option selected value="All">All</option>
                      {#each officers as offi}
                      <option value="{offi}">{offi}</option>
                      {/each}
                  </select>
                {/if}
                {#if requesttype === 'Data Request'}
                  <select class="types" bind:value={types}>
                    <option  value="" >Request Types</option>
                    <option selected value="All">All</option>
                    <option value="SDR">SDR</option>
                    <option value="CAF">CAF</option>
                    <option value="CDR">CDR</option>
                    <option value="IMEI CDR">IMEI CDR</option>
                    <option value="GPRS">GPRS</option>
                    <option value="IPDR">IPDR</option>
                    <option value="RH">RH</option>
                    <option value="POA">POA</option>
                    <option value="TOWER CDR">TOWER_CDR</option>
                    <option value="TOWER GPRS">TOWER_GPRS</option>
                    <option value="TOWER IPDR">TOWER_IPDR</option>
                  </select>
                {:else if requesttype === 'Analysis Request'}
                  <select class="types" bind:value={types}>
                    <option value="" >Select Requests Type</option>
                    <option selected value="All">All Types</option>
                    <option value="All PARAMETERS">SDR</option>
                    <option value="CAF">CAF</option>
                    <option value="CDR">CDR</option>
                    <option value="IMEI">IMEI</option>
                    <option value="GPRS">GPRS</option>
                    <option value="IPDR">IPDR</option>
                    <option value="RH">RH</option>
                    <option value="POA">POA</option>
                    <option value="TOWER DATA">TOWER DATA</option>
                  </select>
                {/if}
                <select style="background: white;border-radius:10px;width:130px;height:37px" bind:value={ISP}>
                  <option selected value="" >Providers</option>
                  <option value="All">All</option>
                  <option value="Jio">Jio</option>
                  <option value="Airtel"> Airtel</option>
                  <option value="Vodafone"> Vodafone</option>
                  <option value="Cellone"> Cellone</option>
                  <option value="Others"> Others</option>
                </select>
                <select style="background: white;border-radius:10px;width:200px;height:37px" bind:value={status}>
                  <option value="" >Select Status</option>
                  <option selected value="All">All Ticket Status</option>
                  <option value="Total_raise">Raised Tickets</option>
                  <option value="Total_approval"> Approved Tickets</option>
                  <option value="Total_pending"> Pending Tickets</option>
                  <option value="Total_close"> Closed Tickets</option>
                  <option value="Total_under_process"> Under Process Tickets</option>
                </select>
                <button style="background: white;border-radius:10px;width:230px; text-align:left"  type="button" id="statusFilterDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                  <i class="bi bi-calendar3"></i> {period_data}
              </button>
              <ul class="dropdown-menu" aria-labelledby="statusFilterDropdown">
                <li>
                  <a class="dropdown-item" href="#" on:click={()=> selected_period('All')}>All</a>
                </li>
                <li>
                  <a class="dropdown-item" href="#" on:click={()=> selected_period('Today')}>Today</a>
                </li>
                <li>
                  <input class="border-0" style="text-align: left; margin-left:10px" use:flatpickr={{mode:'range', dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',onChange:(selectedDates) => {startDate = selectedDates[0];endDate = selectedDates[1];}}}  on:input={selected_period1(startDate,endDate)} placeholder="Select Range" id="dateRangePicker">
                </li>
                </ul>
                <button class="btn btn-outline-primary" on:click={()=> fetchTickets(currentPage)}>
                  <i class="bi bi-funnel-fill"></i><span> Filter </span>
                </button>
                <div style="display: flex; align-items: center; justify-content: flex-end;margin-top: -53px;margin-bottom: 20px;margin-right: 20px">
                  <input style="background: white; border-radius: 10px; width: 200px; text-align: left;" bind:value={searchValue} type="search" placeholder="Search" aria-label="Search">
                  <button class="btn btn-outline-success" type="submit" style="margin-right: 10px;" on:click={() => search('My_tickets')}><i class="bi bi-search"></i></button>
                  <div class="btn-group">
                      {#if selectedOption == 'excel'}
                          <button class="btn btn-outline-primary" on:click={()=> download()}><i class="bi bi-file-earmark-spreadsheet-fill"></i>Excel</button>
                      {:else if selectedOption == 'pdf'}
                          <button class="btn btn-outline-primary" on:click={()=> generatePDF()}><i class="bi bi-file-earmark-spreadsheet-fill"></i>PDF</button>
                      {:else}
                          <button type="button" class="btn btn-outline-primary" disabled>Download as</button>
                      {/if}
                      <button class="btn btn-outline-primary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                          <span class="sr-only"></span>
                      </button>
                      <div class="dropdown-menu">
                          <a class="dropdown-item" on:click={() => handleOptionSelect('excel')}>As Excel</a>
                          <a class="dropdown-item" on:click={() => handleOptionSelect('pdf')}>As PDF</a>
                      </div>
                  </div>
              </div>
              
                
        </div>

          <div class="table-responsive">
            <div id="loadingSpinner" style="display: none;">
              Loading...
            </div>
            {#if isLoading}
              <!-- Display the loading spinner when isLoading is true -->
                <div class="d-flex justify-content-center mb-3">
                  <div class="spinner-grow text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                  <div class="spinner-grow text-secondary" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                  <div class="spinner-grow text-success" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                  <div class="spinner-grow text-danger" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                  <div class="spinner-grow text-warning" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                  <div class="spinner-grow text-info" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                  <div class="spinner-grow text-dark" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </div>
            {/if}
            <div class="table-container" id="pdftable">
             
              <div class="d-flex justify-content-center" style="margin-top: 50px; margin-left: -120px;">
                <div style="margin-right: 10px;" class="table-container">
                  <div id="date">
                    <p>Date Range : {period_data}</p>
                  </div>
                  {#if requesttype === 'Data Request'}
                <h2 class="table_heading-2">Ticket's Information</h2>
                <table class="table table-striped table-hover" id="mytb1" style="padding: 10px !important;">
                  <thead class="table-primary" id="myhead1" style="font-weight: bold;">
                    <tr>
                      <th>Request Type</th>
                      <th>Raised</th>
                      <th>Approved</th>
                      <th>Approval Pending</th>
                      <th>Data Receival Pending</th>
                      <th>Closed</th>
                      <!-- <th>Total Pending</th> -->
                    </tr>
                  </thead>
                  {#each cases as data}
                    {#each data.reqtypes as req}
                      <tr>
                        <td>{req}</td>
                        <td style="background-color: #ebe6d7;font-weight:bold;">{data[req]['Raise']}</td>
                        <td style="background-color: #ddeef0;font-weight:bold;">{data[req]['Approval']}</td>
                        <td style="background-color: #f1dfe1;font-weight:bold;">{data[req]['Pending']}</td>
                        <td style="background-color: #dae2e6;font-weight:bold;">{data[req]['Under_Process']}</td>
                        <td style="background-color: #b3dbc7;font-weight:bold;">{data[req]['Ticket_closed']}</td>
                        <!-- <td style="background-color: #ecaeb3;font-weight:bold;">{data[req]['Total_Pending']}</td> -->
                      </tr>
                    {/each}
                  {/each}
                </table>
                {/if}
                </div>

                <!-- <div class="d-flex justify-content-center" style="margin-top: 50px; margin-left: -120px;"> -->
                  <div style="margin-right: 120px;" class="table-container"> 
                      {#if requesttype === 'Analysis Request'}
                      <h2 class="table_heading-3">Ticket's Information</h2>
                      <table class="table table-striped table-hover" id="mytb1" style="padding: 10px !important;">
                        <thead class="table-primary" id="myhead1" style="font-weight: bold;">
                          <tr>
                            <th>Request Type</th>
                            <th>Raised</th>
                            <th>Approved</th>
                            <th>Approval Pending</th>
                            <th>Assigned</th>
                            <th>Closed</th>
                          </tr>
                        </thead>
                        {#each cases as data}
                          {#each data.reqtypes as req}
                            <tr>
                              <td>{req}</td>
                              <td style="background-color: #ebe6d7;font-weight:bold;">{data[req]['Raise']}</td>
                              <td style="background-color: #ddeef0;font-weight:bold;">{data[req]['Approval']}</td>
                              <td style="background-color: #f1dfe1;font-weight:bold;">{data[req]['Pending']}</td>
                              <!-- change this column to assigned count -->
                              <td style="background-color: #dae2e6;font-weight:bold;">{data[req]['Assigned']}</td>  
                              <!-- End -->
                              <td style="background-color: #b3dbc7;font-weight:bold;">{data[req]['Ticket_closed']}</td>
                            </tr>
                          {/each}
                        {/each}
                      </table>
                      {/if}
                  </div>


              <div  style="margin-left: -100px;" class="table-container">
                {#if requesttype === 'Data Request'}
                <h2 class="table_heading">Providers Information</h2>
                <table class="table table-striped table-hover" id="mytb1" style="padding: 10px !important;">
                  <thead class="table-primary" id="myhead1" style="font-weight: bold; width:20px;">
                    <tr>
                      <th>Request Type</th>
                      {#if ISP === 'All' || ISP === ''}
                      <th>Jio</th>
                      <th>Airtel</th>
                      <th>Vodafone</th>
                      <th>Cellone</th>
                      <th>Others</th>
                      {:else if ISP === 'Jio'}
                      <th>Jio</th>
                      {:else if ISP === 'Airtel'}
                      <th>Airtel</th>
                      {:else if ISP === 'Vodafone'}
                      <th>Vodafone</th>
                      {:else if ISP === 'Cellone'}
                      <th>Cellone</th>
                      {:else if ISP === 'Others'}
                      <th>Others</th>
                      {/if}
                    </tr>
                  </thead>
                  {#each cases as data}
                    {#each data.reqtypes as req}
                      <tr>
                        <td>{req}</td>
                        {#if ISP === 'All' || ISP === ''}
                        <td style="font-weight: bold;">{data[req]['jo']}</td>
                        <td style="font-weight: bold;">{data[req]['at']}</td>
                        <td style="font-weight: bold;">{data[req]['vi']}</td>
                        <td style="font-weight: bold;">{data[req]['co']}</td>
                        <td style="font-weight: bold;">0</td>
                        {:else if ISP === 'Jio'}
                        <td style="font-weight: bold;">{data[req]['jo']}</td>
                        {:else if ISP === 'Airtel'}
                        <td style="font-weight: bold;">{data[req]['at']}</td>
                        {:else if ISP === 'Vodafone'}
                        <td style="font-weight: bold;">{data[req]['vi']}</td>
                        {:else if ISP === 'Cellone'}
                        <td style="font-weight: bold;">{data[req]['co']}</td>
                        {:else if ISP === 'Others'}
                        <td style="font-weight: bold;">0</td>
                        {/if}
                      </tr>
                    {/each}
                  {/each}
                </table>
                {/if}
              </div>
              </div>
          </div>
        </div>


      {#if filter_data.length}

          <div class="page d-flex justify-content-center" style="margin-top: -20px;">
            <nav aria-label="Page navigation">
              <ul class="pagination d-flex justify-content-end">
                <p class="mr-3 mt-2" style="margin-right:15px">Showing {filter_data.length} out of {pagination.total_tickets} rows</p>
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

          <div class="table-responsive text-nowrap">
            <table class="table table-striped table-hover" id="mytb">
              <thead class="table-dark" id="myhead" style="font-weight: bold;">
                <tr>
                  <td>Priority</td>
                  <td>Date</td>
                  <td>TickectID</td>
                  <td>Request Type</td>
                  <td>Approval Status</td>
                  <td>Pending Status</td>
                  <td>Category</td>
                  <td>Team</td>
                  <td>Officer</td>
                  <td>Total Data Received / Total Data</td>
                </tr>
              </thead>
              
              {#each filter_data as user}
              <tr>
                {#if user.priority === "Emergency"}
                  <td style="color: red;font-weight:bold">{user.priority}</td>
                {:else}
                  <td style="color: green;font-weight:bold">{user.priority}</td>
                {/if}
                <td>{user.date}</td>
                <td>
                  <button class="btn btn-link " type="button" data-bs-toggle="modal" data-bs-target="#records{user._id}" on:click={()=> fetch_dash(user)}>
                    {user.token}
                  </button>
                  <div class="modal fade bd-example-modal-lg" id="records{user._id}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true" data-bs-backdrop="static">
                    <div class="modal-dialog modal-dialog-centered modal-xl" >
                      <div class="modal-content" >
                        <div class="modal-header"><h5>{user.token}</h5></div>
                        <div class="modal-body" style="text-align: left;">
                          <div class="container">
                            <div class="row">
                              <div class="col-12">
                                <div class="row">
                                  <div class="table-responsive text-nowrap" style="overflow: auto; height:300px">

                              {#if result !== ''}
                                    {#if user.requesttype === "SDR" && (user.subtypes === "SDR" || user.subtypes === "SDR HISTORY")}
                                        <div class="col-auto scroll-table">
                                            <table class="table table-bordered">
                                                <tr>
                                                
                                                  <th>Phone NO.</th>                                     
                                                  <th>MNP</th>                            

                                                </tr>
                                                {#each result.newnumber as newno}
                                                  <tr>    
                                                    <td>{newno.Phno}</td>
                                                    {#if newno.hasOwnProperty('MNP')}
                                                      <td>{newno.MNP}</td>
                                                    {:else}
                                                      <td></td>
                                                    {/if}
                                                  </tr>
                                                {/each}
                                            </table>
                                        </div>
                                    {/if}
                                    {#if user.requesttype === "CDR" || user.requesttype === "GPRS" && user.subtypes === "Phone" || user.requesttype === "IPDR" && user.subtypes === "Phone"}
                                    <div class="col-auto scroll-table">
                                      <table class="table table-bordered">
                                        <tr>
                                          <th>Phone No.</th> 
                                          <th>NickName</th>   
                                          {#if user.requesttype === "GPRS" && user.subtypes === "Phone" || user.requesttype === "IPDR" && user.subtypes === "Phone"}
                                          <th>From Date</th>
                                          <th>From Time</th>
                                          <th>To Date</th>
                                          <th>To Time</th>
                                          {:else}
                                          <th>From Date</th>
                                          <th>To Date</th>
                                          <th>Status</th>
                                        {/if}
                                        </tr>
                                        {#each result.newnumber as newno}
                                        <tr>
                                          <td>{newno.Phno}</td>
                                          <td class = "text-wrap">{newno.Nickname}</td>
                                          {#if user.requesttype === "GPRS" && user.subtypes === "Phone" || user.requesttype === "IPDR" && user.subtypes === "Phone"}
                                          <td>{newno.From_Date}</td>
                                          <td>{newno.From_Time}</td>
                                          <td>{newno.To_Date}</td>
                                          <td>{newno.To_Time}</td>
                                          {:else}
                                          <td>{newno.From_Date}</td>
                                          <td>{newno.To_Date}</td>
                                          <td class="td {newno.status === "Data_Received" ? "Success" : "Rejected"}">{newno.status || ''}</td>
                                          {/if}
                                        </tr>
                                        {/each}
                                      </table>
                                    </div>
                                    {/if}
                                    {#if user.requestcategory === 'Analysis Request'}
                                    {#if !user.requesttypes.includes('IMEI') && user.subtypes !== "IMEI"}
                                    <div class="col-auto scroll-table">
                                      <table class="table table-bordered">
                                        <tr>
                                          <th>Phone No.</th> 
                                          <th>Provider</th>
                                          <th>From Date</th>
                                          <th>To Date</th>
                                      
                                        </tr>
                                        {#each result.newnumber as newno}
                                        <tr>
                                          <td>{newno.Phno}</td>
                                          <td>{newno.ISP}</td>
                                          <td>{newno.From_Date}</td>
                                          <td>{newno.To_Date}</td>                                
                                        </tr>
                                        {/each}
                                      </table>
                                    </div>
                                    {:else if user.requesttypes.includes('IMEI') && user.subtypes === "IMEI" || user.requesttypes.includes('ALL PARAMETERS') && user.subtypes === "IMEI"}
                                    <div class="col-auto scroll-table">
                                      <table class="table table-bordered">
                                        <tr>
                                          <th>IMEI</th> 
                                          <th>Provider</th>
                                          <th>From Date</th>
                                          <th>To Date</th>
                                      
                                        </tr>
                                        {#each result.newnumber as newno}
                                        <tr>
                                          <td>{newno.IMEI}</td>
                                          <td>{newno.ISP}</td>
                                          <td>{newno.From_Date}</td>
                                          <td>{newno.To_Date}</td>                                
                                        </tr>
                                        {/each}
                                      </table>
                                    </div>
                                    {/if}
                                    {/if}
                                    {#if user.requesttype === "CAF"}
                                    <div class="col-auto scroll-table">
                                      <table class="table table-bordered">
                                        <tr>
                                          <th>Phone No.</th> 
                                          <th>CAF No.</th>
                                        </tr>
                                        {#each result.newnumber as newno}
                                        <tr>
                                          <td>{newno.Phno}</td>
                                          <td>{newno.CAF}</td>                                
                                        </tr>
                                        {/each}
                                      </table>
                                    </div>
                                    {/if}
                                    
                                    {#if user.requesttype === "CAF/CDR"}
                                    <div class="col-auto scroll-table">
                                      <table class="table table-bordered">
                                        <tr>
                                          <th>Phone No./CAF No.</th> 
                                          <th>From Date</th>
                                          <th>To Date</th>
                                        </tr>
                                        {#each result.newnumber as newno}
                                        <tr>
                                          <td>{newno.Phno}</td>
                                          <td>{newno.From_Date}</td>
                                          <td>{newno.To_Date}</td>                          
                                        </tr>
                                        {/each}
                                      </table>
                                    </div>
                                    {/if}

                                    {#if user.requesttype === "GPRS" && user.subtypes === "IMEI" || user.requesttype === "IPDR" && user.subtypes === "IMEI" || user.requesttype === "IMEI CDR"}
                                      <div class="col-auto scroll-table">
                                        <table class="table table-bordered">
                                          <tr>
                                            <th>IMEI</th>     
                                            <th>Provider</th>
                                            {#if user.requesttype === "GPRS" && user.subtypes === "IMEI" || user.requesttype === "IPDR" && user.subtypes === "IMEI"}
                                            <th>From Date</th>
                                            <th>From Time</th>
                                            <th>To Date</th>
                                            <th>To Time</th>
                                            {:else}
                                            <th>From Date</th>
                                            <th>To Date</th>
                                            <th>Status</th>
                                            {/if}
                                          </tr>
                                          {#each result.newnumber as newno}
                                          <tr>
                                            <td>{newno.IMEI}</td>
                                            <td>{newno.ISP}</td>
                                            {#if user.requesttype === "GPRS" && user.subtypes === "IMEI" || user.requesttype === "IPDR" && user.subtypes === "IMEI"}
                                            <td>{newno.From_Date}</td>
                                          <td>{newno.From_Time}</td>
                                          <td>{newno.To_Date}</td>
                                          <td>{newno.To_Time}</td>
                                          {:else}
                                          <td>{newno.From_Date}</td>                      
                                          <td>{newno.To_Date}</td>     
                                          <td class="td {newno.status === "Data_Received" ? "Success" : "Rejected"}">{newno.status || ''}</td>
                                          {/if}
                                          </tr>
                                          {/each}
                                        </table>
                                      </div>
                                      {/if}
                                    {#if user.requesttype === "IPDR" && user.subtypes === "IPV6" || user.requesttype === "IPDR" && user.subtypes === "IPV4" || user.requesttype === "IPDR" && user.subtypes === ""}
                                    <div class="col-auto scroll-table">
                                      <table class="table table-bordered">
                                        <tr>
                                          {#if user.requesttype === "IPDR" && user.subtypes === "IPV6" }
                                          <th>IPV6</th>
                                          {:else if user.requesttype === "IPDR" && user.subtypes === "IPV4" }
                                          <th>IPV4</th>
                                          {:else if user.requesttype === "IPDR" && user.subtypes === ""}
                                          <th>IPV</th>
                                          {/if}                             
                                            <th>From Date</th>
                                            <th>From Time</th>
                                            <th>To Date</th>
                                            <th>To Time</th>
                                        </tr>
                                        {#each result.newnumber as newno}
                                        <tr>
                                          {#if user.subtypes === "IPV6" || user.subtypes === "IPV4"}
                                          <td>{newno.IP_Address}</td>                                
                                          {:else if user.requesttype === "IPDR" && user.subtypes === ""}
                                          <td>{newno.IP_Address}</td>
                                          {/if}
                                          <td>{newno.From_Date}</td>
                                          <td>{newno.From_Time}</td>
                                          <td>{newno.To_Date}</td>
                                          <td>{newno.To_Time}</td>
                                        </tr>
                                        {/each}
                                      </table>
                                    </div>
                                    {/if}
                                    {#if user.requesttype === "RECHARGE HISTORY (RH)" && user.subtypes === "Phone" || user.requesttype === "POINT OF ACTIVATION (POA)" && user.subtypes === "Phone"}
                                    <div class="col-auto scroll-table">
                                      <table class="table table-bordered">
                                        <tr>
                                          
                                          <th>Phone</th>
                                          <th>NickName</th>                                                          
                                            <th>From Date</th>
                                            <th>To Date</th>
                                        </tr>
                                        {#each result.newnumber as newno}
                                        <tr>
                                          {#if user.requesttype === "RECHARGE HISTORY (RH)"}
                                          <td>{newno.Phno}</td>
                                          <td class = "text-wrap">{newno.Nickname}</td>
                                          {:else if user.requesttype === "POINT OF ACTIVATION (POA)"}
                                          <td>{newno.Phno}</td>
                                          <td class = "text-wrap">{newno.Nickname}</td>
                                          {/if}
                                          <td>{newno.From_Date}</td>
                                          <td>{newno.To_Date}</td>
                                        </tr>
                                        {/each}
                                      </table>
                                    </div>
                                    {/if}

                                    {#if user.requesttype === "RECHARGE HISTORY (RH)" && user.subtypes === "Retailer/Dealer Details" || user.requesttype === "POINT OF ACTIVATION (POA)" && user.subtypes === "Retailer/Dealer Details"}
                                    <div class="col-auto scroll-table">
                                      <table class="table table-bordered">
                                        <tr>
                                          
                                          <th>Dealer Details</th>
                                          <th>Dealer Code</th>    
                                          <th>Provider</th>                                                     
                                            <th>From Date</th>
                                            <th>To Date</th>
                                        </tr>
                                        {#each result.newnumber as newno}
                                        <tr>
                                          {#if user.requesttype === "RECHARGE HISTORY (RH)"}
                                          <td>{newno.RH_Dealer}</td>
                                          <td>{newno.RH_code}</td>
                                          <td>{newno.Provider}</td>
                                          {:else if user.requesttype === "POINT OF ACTIVATION (POA)"}
                                          <td>{newno.POA_Dealer}</td>
                                          <td>{newno.POA_code}</td>
                                          <td>{newno.Provider}</td>
                                          {/if}
                                          <td>{newno.From_Date}</td>
                                          <td>{newno.To_Date}</td>
                                        </tr>
                                        {/each}
                                      </table>
                                    </div>
                                    {/if}
                                    {#if user.requesttype === "TOWER CDR" || user.requesttype === "TOWER GPRS"|| user.requesttype === "TOWER IPDR"}
                                    <div class="col-auto scroll-table">
                                      <table class="table table-bordered">
                                        <tr>
                                          {#if user.subtypes === "CGI"}
                                          <th>CGI ID</th>
                                        
                                          {:else if user.subtypes === "Phone"}
                                          <th>Phone</th>
                                          {:else if user.subtypes === "Area"}
                                          <th>Area</th>
                                          <th>Cell IDs</th>
                                          {:else if user.subtypes === "Co-Ordinates"}
                                          <th>Latitude</th>
                                          <th>Longitude</th>
                                          <th>Radius</th>
                                          <th>Cell IDs</th>
                                          <th>AreaDescription</th>
                                          <th>Provider</th>
                                          <th>State</th>
                                          {:else if user.subtypes === "Tower Name"}
                                          <th>Tower Name</th>
                                          {/if}                               
                                            <th>From Date</th>
                                            <th>To Date</th>
                                        </tr>
                                        {#each result.newnumber as newno}
                                        <tr>
                                          {#if user.subtypes === "CGI"}
                                          <td>{newno.CGI}</td>
                                          
                                          {:else if user.subtypes === "Phone"}
                                          <td>{newno.Phno}</td>
                                          {:else if user.subtypes === "Area"}
                                          <td>{newno.Area}</td>
                                          <td class="table table-bordered">
                                            <div style="max-height: 90px; overflow-y: scroll;">
                                            {#each newno.Cell_id as cell}
                                            <tr>
                                            {cell}
                                            </tr>
                                            {/each}
                                            </div>
                                          </td>
                                          {:else if user.subtypes === "Co-Ordinates"}
                                          <td>{newno.Latitude}</td>
                                          <td>{newno.Longitude}</td>
                                          <td>{newno.Rad}</td>                        
                                          <td class="table table-bordered">
                                            <div style="max-height: 85px; overflow-y: scroll;">
                                            {#each newno.Cell_id as cell}
                                            <tr>
                                            {cell}
                                            </tr>
                                            {/each}
                                            </div>
                                          </td>
                                          <td class="table table-bordered">
                                            <div  style="max-height: 85px; overflow-y: scroll;">
                                            {#each newno.AreaDescription as area}
                                            <tr style="text-align:center; vertical-align: middle;">
                                            {area}
                                            </tr>
                                            {/each}
                                            </div>
                                          </td>
                                          <td class="table table-bordered">
                                            <div style="max-height: 85px; overflow-y: scroll;">
                                            {#each newno.Operator as opt}
                                            <tr>
                                            {opt}
                                            </tr>
                                            {/each}
                                            </div>
                                          </td>
                                          <td class="table table-bordered">
                                            <div style="max-height: 85px; overflow-y: scroll;">
                                            {#each newno.State as sts}
                                            <tr>
                                            {sts}
                                            </tr>
                                            {/each}
                                            </div>
                                          </td>
                                          {/if}
                                          <td>{newno.From_Date}</td>
                                          <td>{newno.To_Date}</td>
                                        </tr>
                                        {/each}
                                      </table>
                                    </div>
                                    {/if}
                                {/if}
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div class="modal-footer">
                          <!-- <button type="button" class="btn btn-outline-danger">Yes</button> -->
                          <button type="button" class="btn btn-outline-danger" data-bs-dismiss="modal" aria-label="Close">Close</button>
                        </div>
                      </div>
                    </div>
                  </div>  
                </td>
                <td>{user.requesttype || user.requesttypes} {user.subtypes}</td>
                 <td class="{user.approval.includes('Approved') || user.approval.includes('Assigned') || user.approval === 'Data_Received' ? "Success" : "Rejected"}" >
                  {user.approval}
                </td>
                <td class={user.pending === "Mail Under Process"  ? "Rejected" : "Rejected"} >
                  {user.pending}
                </td>
                <td>{user.requestcategory}</td>
                <td>{user.team}</td>
                <td>{user.officername}</td>
                <td>
                  {#if user.pending === 'Mail Under Process' && (user.subtypes === 'Phone' || user.requesttype === 'CDR')}
                    {user.res_len}/{user.total_len}
                  {:else if user.pending === 'Ticket_Closed' && (user.subtypes === 'Phone' || user.requesttype === 'CDR')}
                    {user.status_count}/{user.total_len}

                  {:else if user.pending === 'Mail Under Process' && (user.subtypes === 'IMEI' || user.requesttype === 'IMEI CDR')}
                    {user.newno_len}/{user.total_len}
                  {:else if user.pending === 'Ticket_Closed' && (user.subtypes === 'IMEI' || user.requesttype === 'IMEI CDR')}
                    {user.status_count}/{user.total_len}
                  {:else}
                    <p style="font-weight: bold;color:red">--</p>
                  {/if}
                </td>
              </tr>
  
              {/each}
            </table>
            
          </div>
      {/if}
          </div>
          
    </div>
  </div>
  </div>
  </main>