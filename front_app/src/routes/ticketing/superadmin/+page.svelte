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
    import * as XLSX from 'xlsx';
        // console.log("userDetailsStore",userDetailsStore)
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
        }
        else{
        goto('/');
        }
        })
   
  let rowCount = 0;
  let cases = []; // Initialize cases as an empty array
  let filteredData = []; // Initialize filteredData as an empty array
  let paginatedData = []; // Initialize paginatedData as an empty array
  let currentPage = 1; // Current page number
  const itemsPerPage = 6; // Number of items to display per page
  let totalPages = 0; // Total number of pages
  let Active_status = [];
  let design = [];
  let tm = [];
  let rol = [];
  async function allinONE() {
    try {
      const response = await fetch(basepath() + '/allinONE', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: userDetails.email })
      });
  
      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }
  
      cases = await response.json();
      console.log(cases,"=======================")
      // Define the custom order of designations
      const designationOrder = ['IG', 'DIG', 'SP', 'ADDLSP','ADDL-SP/DSP', 'DSP', 'INSPR', 'SI', 'ASI','HC', 'PC'];
  
      // Create a custom sorting function based on the order and then alphabetically by name
      cases.sort((a, b) => {
        const orderA = designationOrder.indexOf(a.designation);
        const orderB = designationOrder.indexOf(b.designation);
  
        if (orderA !== orderB) {
          return orderA - orderB;
        } else {
          // If the designations are the same, sort alphabetically by name
          return a.name.localeCompare(b.name);
        }
      });
      
      Active_status = cases.filter((user) => user);
      // console.log(Active_status);
  
      const uniqueDesignations = [...new Set(cases.map(user => user.designation))];
      design = uniqueDesignations;
      // console.log(design);

      const uniteams = [...new Set(cases.map(user => user.team))];
      tm = uniteams;
      // console.log(tm);
  
      const uniroles = [...new Set(cases.map(user => user.role))];
      rol = uniroles;
      // console.log(rol);
  
      filteredData = cases; // Set filteredData to all the fetched data
      rowCount = cases.length;
      totalPages = Math.ceil(filteredData.length / itemsPerPage);
      paginateData();
    } catch (error) {
      console.error('Error:', error);
    }
  }
  
  
  function designation(status) {
    if (status === 'All' || status === '') {
      filteredData = cases; // Display all data
      const checkboxes1 = document.querySelectorAll('.checkbox');
      checkboxes1.forEach((checkbox1) => {
        checkbox1.checked = false;
      });
    } else {
      const selectedCheckboxes = Array.from(document.querySelectorAll('.checkbox:checked')).map(checkbox => checkbox.value);
      console.log(selectedCheckboxes,selectedCheckboxes.length)
  
      if (selectedCheckboxes.length >= 1) {
        filteredData = cases.filter((user) => selectedCheckboxes.includes(user.designation));
      } else if (design.includes(status)){
          console.log(status)
        filteredData = cases.filter((user) => user.designation === status); // Filter data based on status
      }
      else if (selectedCheckboxes.length === 0){
        filteredData = cases; 
      }
    }
  
    totalPages = Math.ceil(filteredData.length / itemsPerPage); // Update the total number of pages
    currentPage = 1; // Reset the current page to the first page
    paginateData(); // Repopulate the paginatedData array
  }
  
  function Teams(status) {
    if (status === 'All' || status === '') {
      filteredData = cases; // Display all data
      const checkboxes1 = document.querySelectorAll('.checkbox');
      checkboxes1.forEach((checkbox1) => {
        checkbox1.checked = false;
      });
    } else {
      const selectedCheckboxes = Array.from(document.querySelectorAll('.checkbox:checked')).map(checkbox => checkbox.value);
      if (selectedCheckboxes.length > 0) {
        filteredData = cases.filter((user) => selectedCheckboxes.includes(user.team));
      } else if (tm.includes(status)){
          console.log(status)
        filteredData = cases.filter((user) => user.team === status); // Filter data based on status
      }
      else if (selectedCheckboxes.length === 0){
        filteredData = cases; 
      }
    }
  
    totalPages = Math.ceil(filteredData.length / itemsPerPage); // Update the total number of pages
    currentPage = 1; // Reset the current page to the first page
    paginateData(); // Repopulate the paginatedData array
  }
  
  function Roles(status) {
    if (status === 'All' || status === '') {
      filteredData = cases; // Display all data
      const checkboxes1 = document.querySelectorAll('.checkbox');
      checkboxes1.forEach((checkbox1) => {
        checkbox1.checked = false;
      });
    } else {
      const selectedCheckboxes = Array.from(document.querySelectorAll('.checkbox:checked')).map(checkbox => checkbox.value);
  
      if (selectedCheckboxes.length > 0) {
        filteredData = cases.filter((user) => selectedCheckboxes.includes(user.role));
      } else if (rol.includes(status)){
          console.log(status)
        filteredData = cases.filter((user) => user.role === status); // Filter data based on status
      }
      else if (selectedCheckboxes.length === 0){
        filteredData = cases; 
      }
    }
  
    totalPages = Math.ceil(filteredData.length / itemsPerPage); // Update the total number of pages
    currentPage = 1; // Reset the current page to the first page
    paginateData(); // Repopulate the paginatedData array
  }
  
  
  function paginateData() {
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    rowCount = filteredData.length;
    paginatedData = filteredData.slice(startIndex, endIndex);
  }
  // filterData('');
  
    onMount(() => {
      // beware of truthy and falsy values
      if (localStorage.getItem("userAuth") === "true") {
        // console.log('auth is passed')
        allinONE()
      } else {
        goto('/');
      }
    })
    // console.log(cases)
    async function logout() {
      await fetch(basepath() + '/logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      // Set the authentication to false
      localStorage.setItem("userAuth", false);
      // Redirect the user to the login page after logging out
      goto('/');
      window.location.reload();
  
    }
    
  let name = '';
  let email = '';
  let MobileNo ='';
  let password1='';
  let password2='';
  let value='';
  let question='';
  let answer='';
  let officername='';
  let team = '';
  let showIsotDetailsvalue ='';
  let showApDetailsvalue='';
  let showCatDetailsvalue='';
  let modules = "";
  let role='';
  let spteam = '';
  let spmodule = '';
  let addlspteam = '';
  let addlspmodule = '';
  let dspteam = "";
  let dspmodule = "";
  let insprteam = "";
  let insprmodule = "";
  let siteam = "";
  let simodule = "";
  let addApplication = [];

  // let selectedapplications = "";
  $: spteam = value + " " + team;
  $: spmodule = value + " " + modules;
  $: addlspteam = value + " " + team;
  $: addlspmodule = value + " " + modules;
  $: dspteam = value + " " + team;
  $: dspmodule = value + " " + modules;
  $: insprteam = value + " " + team;
  $: insprmodule = value + " " + modules;
  $: siteam = value + " " + team;
  $: simodule = value + " " + modules;
  // $: role = (spmodule||spteam||addlspmodule||addlspteam||dspteam||dspmodule||insprmodule||insprteam||siteam||simodule);
  
  $: modules = (showApDetailsvalue || showCatDetailsvalue || showIsotDetailsvalue);
  let superior = '';
  
  async function addNewUser() {
    if ( name === '' || email === '' || password1 === '' || 
    password2 === '' || officername === '') 
    {
        alert('Please fill in all the required fields.');
        return;
      }
  
    const selectedapp = getSelected(); 
    const response = await fetch(`${basepath()}/register`, {
      
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: name,
        email: email,
        password1:password1,
        password2:password2,
        mobilenumber:MobileNo,
        designation:value,
        officername:officername,
        question:question,
        answer:answer,
        team:team,
        modules:modules,
        superior:superior,
        role:role,
        status : "Active",
        Model: selectedapp
      })
    });
  
    if (!response.ok) {
      throw new Error('Failed to create new user');
    }
    // Refresh the user list by calling the allinONE function again
    window.location.reload();
  }
  
  
  function goToPage(page) {
    currentPage = page;
    paginateData();
  }
  
  function goToPreviousPage() {
    if (currentPage > 1) {
      currentPage--;
      paginateData();
    }
  }
  
  function goToNextPage() {
    if (currentPage < totalPages) {
      currentPage++;
      paginateData();
    }}
  
    async function deleteUser(user) {
      try{
      const response = await fetch(`${basepath()}/deleteuser`,{
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          id : `${user._id}`,
          email : `${user.email}`,
        })
      });
      console.log(user.email,"...................");

      if (response.ok) {
          const result = await response.json();
  
          console.log(result.message);
        } else {
          console.error('Delete failed');
        }
      } catch (error) {
        // Handle network or server error
        console.error('Delete failed', error);
      }
      
      window.location.reload();
    
    }
    function updateappacess(app,user){
      console.log(app, addApplication)
      if (!user.Application.includes(app)) {
        user.Application.push(app)

      }else{
        user.Application = user.Application.filter(a => a !== app); // Remove the app if it's already present
    }
    console.log(user.Application);
    }
    

  
  
    async function updateUser(user) {
      const selectedApps = addApplication // getSelected(user);
      console.log(user.Application,"------------0000000000000000000000")
      try {
        const response = await fetch(`${basepath()}/updateuser`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
        id : `${user._id}`,
        name: `${user.name}`,
        email: `${user.email}`,
        password1:`${user.password1}`,
        password2:`${user.password2}`,
        mobilenumber:`${user.mobilenumber}`,
        designation:`${user.designation}`,
        officername:`${user.officername}`,
        team:`${user.team}`,
        modules:`${user.modules}`,
        status : `${user.status}`,
        superior: `${user.superior}`,
        role: `${user.role}`,
        Application: user.Application,
  
      })
    });
  
        console.log(`Updating user: ${user.name}`);
        if (response.ok) {
          // Update successful, handle the response accordingly
          const result = await response.json();
          console.log(result.message);
          alert('updated')
        } else {
          // Handle error response
          console.error('Update failed');
        }
      } catch (error) {
        // Handle network or server error
        console.error('Update failed', error);
      }
      window.location.reload();
  
    }
  
    let showApDetails = false;
    let showIsotDetails = false;
  
    let showCatDetails = false;
   
    function handleModuleFirstDropdownChange() {
      if (team !== 'AP') {
        showApDetails = false;
      } else {
        showApDetails = true;
      }
      if (team !== 'ISOT') {
        showIsotDetails = false;
      } else {
        showIsotDetails = true;
      }
      if (team !== 'CAT') {
        showCatDetails = false;
      } else {
        showCatDetails = true;
      }
    }
    onMount(() => {
      // Call handleFirstDropdownChange initially to set the initial value of showSecondDropdown
      handleModuleFirstDropdownChange();
    });
  function close(){
    window.location.reload();
  }
  
  function for_isot() {
      showApDetailsvalue = '';
      showCatDetailsvalue = '';
    }
  
    function for_cat() {
      showApDetailsvalue = '';
      showIsotDetailsvalue = '';
    }
  
    function for_ap() {
      showCatDetailsvalue = '';
      showIsotDetailsvalue = '';
    }
    let checked = true; // Default value for the switch
  
  function toggleSwitch() {
    checked != checked; // Toggle the state
    localStorage.setItem('switchState', checked.toString()); // Save the state to localStorage
    console.log(checked)
  }
  
  onMount(() => {
    // Get the state from localStorage when the component mounts
    const storedState = localStorage.getItem('switchState');
    checked = storedState === 'true' ? true : false;
  });
  
  
  let alert_message = '';
  async function check_email() {
  
        const response = await fetch(basepath()+'/check_email',{
          method:'POST',
          headers: {
            'Content-Type' : 'application/json'
          },
          body: JSON.stringify({
            email: email
          })
        });
  
        const data = await response.json();
        alert_message = data
      }
    
  
  let columnNames = [];
  let records = [];
  let file;
  function upload_user_data(event){
    file = event.target.files[0];
    console.log(file)
    const reader = new FileReader();
  
    reader.onload = () => {
      const arrayBuffer = reader.result;
      const workbook = XLSX.read(arrayBuffer, { type: 'array' });
  
      const sheetName = workbook.SheetNames[0];
      const sheet = workbook.Sheets[sheetName];
  
      const range = XLSX.utils.decode_range(sheet['!ref']);
  
      // Extract column names
      for (let col = range.s.c; col <= range.e.c; col++) {
        const cellAddress = XLSX.utils.encode_cell({ r: range.s.r, c: col });
        const cell = sheet[cellAddress];
        if (cell && cell.t === 's') {
          // If the cell type is a string, use the string value
          columnNames.push(cell.v.trim());
        } else {
          // Otherwise, use the cell address as the column name
          columnNames.push(cellAddress);
        }
      }
  
      for (let row = range.s.r + 1; row <= range.e.r; row++) {
    const rowData = {};
    for (let col = range.s.c; col <= range.e.c; col++) {
      const columnName = columnNames[col];
      const cellAddress = XLSX.utils.encode_cell({ r: row, c: col });
      const cell = sheet[cellAddress];
      if (cell) {
        // Use utils.format_cell to preserve formatting
        const formattedValue = XLSX.utils.format_cell(cell);
        rowData[columnName] = formattedValue.trim();
      } else {
        // If the cell is empty, assign an empty string
        rowData[columnName] = '';
      }
    }
    records.push(rowData);
    
  }
  
  }
  reader.readAsArrayBuffer(file);
  
  }
  
  async function user_data_upload(){
    const response = await fetch(basepath()+'/user_data_upload',{
      method:'POST',
      headers: {
        'Content-Type' : 'application/json'
      },
      body: JSON.stringify({
        data: records
      })
    });
    if (response.ok){
      const data = await response.json();
      console.log(data)
      alert(data.messege)
      window.location.reload();
    }
  }
  
  let selectedModel = []; // Array to store selected fruits
    function getSelected() {
  
        // Get all checkboxes with name 'fruits' that are checked
        const checkboxes = [... new Set(Array.from(document.querySelectorAll('input[name="Model"]:checked')).map(checkbox => checkbox.value))];
        selectedModel = checkboxes;
        return selectedModel; // Return the array of selected fruits
    }
  
    
  
  </script>
  <style>
  table, th, td {
  border-collapse: collapse;
  text-align: center;
  vertical-align: middle;
  padding: 0.75rem;
  /* vertical-align: top; */
  border-top: 1px solid #dee2e6;
  }
  
  
  h2{
  margin-left: 50px;
  margin-top: 10px;
  }
  select,input,textarea{
    margin-bottom: 10px;
    border-radius: 5px;
  }
  .td{
    text-align:center;
    vertical-align: middle;
  }
  .side{
    background-color: white;
  }
  label{
    text-align: start;
  }
  .page{
    position: fixed;
    bottom: 0;
    right: 0;
    margin: 5px; /* Adjust the margin as needed */
  }
  
  .page_border{
    border: 4px solid #000000; /* Add a border around the container */
    box-sizing: border-box;
    height: 92.2%;
    margin: 0;
    padding: 0;
    border-radius: 5px;
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.2);
    background:linear-gradient(120deg, #e2e2e2, #78c3e4);
    background-repeat: no-repeat;
    background-size: cover;
  }
  
  .roles{
    height: 400px;
    overflow-x: hidden;
    overflow-y: scroll;
  }
  .checkbox{
    margin-top: 8px;
    margin-left: 8px;
  }
  .submit{
    margin-top: 15px;
    display: flex;
    margin-left: 160px;
  }
  .checkbox-group label {
      display: inline-block;
      margin-right: 19px;
  }
         
  .selected{
    background-color: rgb(40, 139, 196);
    color: white;
  }

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
  
  <nav class="navbar navbar-dark bg-dark">
    <div></div>
    <div class="pt-0 ">
    <div class="d-flex justify-content-end bd-highlight">
      <div class="p-2 bd-highlight">
        <div class="search-container">
        </div>
    </div>
  
  
    <div class="p-2 bd-highlight">
      <!-- <input accept="text/txt" bind:files id="avatar" name="avatar" type="file"/> -->
      <button class="btn  btn-outline-warning" data-bs-toggle="modal" data-bs-target="#myModal">
        <a href="" class="text-white">Import Bulk Users</a>
      </button>
      <div class="modal fade" id="myModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog" style="width: 25%;">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" style="font-size: 1.25rem;font-weight: 500;margin-bottom: 0; line-height: 1.5;font-family: sans-serif;" id="exampleModalLabel">Upload your File</h1>
              <button type="button" class="btn-close" on:click= {close} data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <!-- <input class="mt-3 form-control" style="font-family: sans-serif;color: #495057" accept=".csv,.xlsx, .xls" bind:files={file} type="file" /> -->
              <input class="mt-3 form-control" type="file" accept=".csv,.xlsx, .xls" on:change={upload_user_data} id="excel_file"/>
                          <!-- <input type="file" name="file" class="form-control" id="customFile" bind:value={files}/> -->
                          <button type="button" on:click={user_data_upload} class="submit btn btn-outline-success">Upload</button>
                           <!-- <button on:click={() => submitedRecord(user._id)} class="btn btn-dark">Approve</button> -->
                        
            </div>
          </div>
        </div>
      </div>
  </div>
    <div class="p-2 bd-highlight">
      <button class="ml-5 btn btn-outline-success text-white"  type="button" data-bs-toggle="modal" data-bs-target="#myModal{paginatedData._id}">
        Add New Officer
      </button>
      <div class="modal fade" id="myModal{paginatedData._id}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true" data-bs-backdrop="static">
        <div class="modal-dialog" style="width: 26%;">
          <div class="modal-content">
            <div class="modal-header">
              <h4 class="modal-title" id="exampleModalLabel" style="font-weight: bold;">Register New Officer</h4>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" on:click={close}></button>
            </div>
            <div class="modal-body">
              <div class="container">
                <div class="row">
                  <div class="col-12">
                    <div class="row">
                      <!-- Registration form inputs -->
                      <input type="text" placeholder="Officer Name" name="MobileNo" bind:value={officername}>
                  
                  <select aria-label="Default select example" bind:value={value}>
                    <option selected value="">Select Designation</option>
                    <option value="IG">IG</option>
                    <option value="DIG">DIG</option>
                    <option value="SP">SP</option>
                    <!-- <option value="ADDLSP">ADDLSP</option> -->
                    <option value="ADDL-SP/DSP">ADDL-SP/DSP</option>
                    <option value="INSPR">INSPR</option>
                    <option value="SI">SI</option>
                    <option value="ASI">ASI</option>
                    <option value="HC">HC</option>
                    <option value="PC">PC</option>
                  </select>
                  {#if value !=="IG" && value !=="DIG"}
                    <select aria-label="Default select example" bind:value={team} on:change={handleModuleFirstDropdownChange}>
                    <option selected value="" >Select Team Name</option>
                    <option value="AP">AP</option>
                    <option value="ISOT">ISOT</option>
                    <option value="CAT">CAT</option>
                    <option value="ADMIN">ADMIN</option>
                  </select>
                  <select aria-label="Default select example" hidden={!showApDetails} bind:value={showApDetailsvalue} on:change={for_ap}>
                    <option selected value="">Select Module</option>
                    <option value="AP">AP</option>
                    <!-- <option value="AOB">AOB</option> -->
                    <!-- <option value="OTHER">OTHER</option> -->
                  </select>
                   <select aria-label="Default select example" hidden={!showCatDetails}  bind:value={showCatDetailsvalue} on:change={for_cat}>
                    <option selected value="">Select Module</option>
                    <option value="CAT">CAT</option>
                    <!-- <option value="OTHER">OTHER</option> -->
                    </select>
                  <select aria-label="Default select example" hidden={!showIsotDetails} bind:value={showIsotDetailsvalue} on:change={for_isot} >
                    <option selected value="">Select Module</option>
                    <option value="ISOT">ISOT</option>
                    <option value="ISOT-M1">ISOT-M1</option>
                    <option value="ISOT-M2">ISOT-M2</option>
                    <option value="ISOT-M3">ISOT-M3</option>
                    <!-- <option value="OTHER">OTHER</option> -->
                  </select>
                  {:else}
                  <select aria-label="Default select example" bind:value={team}>
                    <option selected value="" >Select Team Name</option>
                    <option value="ADMIN">ADMIN</option>
                  </select>
                  {/if}
    
                  <select aria-label="Default select example" bind:value={role}>
                    <option selected value="">Select Role</option>
                  {#if value === "IG" && team === "ADMIN"}
                      <!-- <option value="IG">IG</option> -->
                      <option value="{value} ADMIN">{value} ADMIN</option>
                {/if}
                {#if value === "DIG" && team === "ADMIN"}
                      <!-- <option value="DIG">DIG</option> -->
                      <option value="{value} ADMIN">{value} ADMIN</option>
                {/if}
                {#if value === "SP"}
                {#if team === "SP" || team === "ISOT" || team === "CAT" || team === "AP"}
                      <option value={spteam}>{spteam}</option>
                      <!-- <option value={spmodule}>{spmodule}</option> -->
    
                {:else if value === "SP" && team === "ADMIN"}
                    <option value="{value} ADMIN">{value} ADMIN</option>
                {/if}
                {/if}
                {#if value === "ADDLSP"}
                      <option value={addlspteam}>{addlspteam}</option>
                      <!-- <option value={addlspmodule}>{addlspmodule}</option> -->
                {/if}
                {#if value === "ADDL-SP/DSP"}
                      <option value={dspteam}>{dspteam}</option>
                      <!-- <option value={dspmodule}>{dspmodule}</option> -->
                {/if}
                {#if value === "INSPR"}
                      <option value={insprteam}>{insprteam}</option>
                      <option value="Analyst">Analyst</option>
                      <option value="Logger">Logger</option>
                {/if}
                {#if value === "SI"}
                      <option value={siteam}>{siteam}</option>
                      <!-- <option value={simodule}>{simodule}</option> -->
                      <option value="Analyst">Analyst</option>
                    <option value="Logger">Logger</option>
  
                  {:else if value === "ASI" || value === "HC" || value=== "PC"}
                    <option value="Analyst">Analyst</option>
                    <option value="Logger">Logger</option>
                    <option value="Mailer">Mailer</option>
                {/if}
              </select>
              {#if value === "SP" || value === "IG" || value === "DIG" && team !== "" }
                    <input type="text" placeholder="Top Superior" name="Email" value="Top Superior" readonly>
              {:else if value === "ADDL-SP/DSP"}
                  <select aria-label="Default select example" bind:value={superior}>
                    <option disabled selected value="">Select Superior</option>
                    {#each Active_status as Super}
                    {#if Super.role !== role && Super.designation === "SP" || Super.designation === "ADDL-SP/DSP" || Super.designation==="DSP" } 
                  <option value={Super.officername}>{Super.officername} - {Super.designation}</option>
                  {/if}
                  {/each}
                </select>
              {:else}
                    <select aria-label="Default select example" bind:value={superior}>
                      <option disabled selected value="">Select Superior</option>
                      {#each Active_status as Super}
                      {#if Super.role !== role && Super.designation === "SP" || Super.designation === "ADDL-SP/DSP" || Super.designation==="INSPR" || Super.designation==="DSP"} 
                    <option value={Super.officername}>{Super.officername} - {Super.designation}</option>
                    {/if}
                    {/each}
                  </select>
              {/if}
              <input type="text" placeholder="Username" name="name" bind:value={name}>
              <input type="text" id="emailInput" bind:value={email} on:keyup={check_email} placeholder="Enter email and press Enter">
              {#if alert_message.message1}
              <p style="color: red;">{alert_message.message1}</p>
              {:else if alert_message.message2}
              <p style="color: green;">{alert_message.message2}</p>
              {/if}
              <input
                  type="text"
                  placeholder="Mobile No"
                  name="MobileNo"
                  bind:value={MobileNo}
                  maxlength="10"
                  on:input={() => {
                   if (!/^[0-9]*$/.test(MobileNo)) {
        MobileNo = MobileNo.replace(/[^0-9]/g, ''); // Remove non-digit characters
      }
    }}
  />
  
                {#if MobileNo.length < 10}
                  <p class="error-message" style="color: red;">Please enter 10 digits.</p>
                {/if}
  
              <input type="password" placeholder="Password" name="password" bind:value={password1}>
              <input type="password" placeholder="Re-enter Password" name="password" bind:value={password2}>
                    <div class="checkbox-group">
                      <input type="checkbox" id="apple" name="Model" value="VIGOR">
                      <label for="apple">VIGOR</label>
                  
                      <input type="checkbox" id="banana" name="Model" value="NEXUS">
                      <label for="banana">Nexus</label>
                  
                      <input type="checkbox" id="mango" name="Model" value="TICKETING">
                      <label for="mango">Ticketing</label> <br>
                  
                      <input type="checkbox" id="orange" name="Model" value="CDAT">
                      <label for="orange">cdat</label> 

                      <input type="checkbox" id="orange" name="Model" value="CDAT">
                      <label for="orange">Analysis</label> 
                      
                      <input type="checkbox" id="orange" name="Model" value="CDAT">
                      <label for="orange">Database</label>
                  </div>
                  
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button on:click={addNewUser} type="button" class="btn btn-outline-primary">Register</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
  
  </div>
  </nav>
  <div class="page_border">
  <main>
  <!-- <br> -->
  <div>
    <h2 style="font-weight: bold;">{userDetails.officername}</h2>
    <p style="margin-left: 50px;margin-top: 10px;">{userDetails.designation}</p>
</div>
  
      <div class="table-responsive text-nowrap">
          <table class="table table-striped table-hover" id="mytb">
              <thead class="table-dark" id="myhead">
                  <tr>
                      <th>Info</th>
                      <th>Superior</th>
                      <th>Officer Name</th>
                      <th><button class="btn btn-dark dropdown-toggle" type="button" id="statusFilterDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                          Designations
                      </button>
                      <ul class="dropdown-menu" aria-labelledby="statusFilterDropdown">
                        <li>
                          <a class="dropdown-item" href="#" on:click={() => designation('All')}>All</a>
                        </li>
                        {#each design as designations}
                        <li>
                          <div class="d-flex">
                          <input class="checkbox" type="checkbox" id="{designations}" name="{designations}" value="{designations}" on:change={designation}>
                          <a class="dropdown-item" href="#" on:click={() => designation(designations)}>{designations}</a>
                          </div>
                        </li>
                        {/each}
                      </ul>                  
                    </th>
                      <th><button class="btn btn-dark dropdown-toggle" type="button" id="statusFilterDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                        Teams
                      </button>
                      <ul class="dropdown-menu" aria-labelledby="statusFilterDropdown">
                        <li>
                          <a class="dropdown-item" href="#" on:click={() => Teams('All')}>All</a>
                        </li>
                        {#each tm as teams}
                        <li>
                          <div class="d-flex">
  
                            <input class="checkbox" type="checkbox" id="{teams}" name="{teams}" value="{teams}" on:change={Teams}>
                          <a class="dropdown-item" href="#" on:click={() => Teams(teams)}>{teams}</a>
                          </div>
                        </li>
                        {/each}
                      </ul>   
                    </th>
                      <th>Modules</th>
                      <th>Email</th>
                      <th><button class="btn btn-dark dropdown-toggle" type="button" id="statusFilterDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                        Roles
                      </button>
                      <ul class="roles dropdown-menu" aria-labelledby="statusFilterDropdown">
                        <li>
                          <a class="dropdown-item" href="#" on:click={() => Roles('All')}>All</a>
                        </li>
                        {#each rol as roll}
                        <li>
                          <div class="d-flex">
  
                            <input class="checkbox" type="checkbox" id="{roll}" name="{roll}" value="{roll}" on:change={Roles}>
                            <a class="dropdown-item" href="#" on:click={() => Roles(roll)}>{roll}</a>
                          </div>
                        </li>
                        {/each}
                      </ul>   
                    
                    </th>
                      <!-- <th>App</th> -->
                      <th>Status</th>               
                      <th>Action</th>
                  </tr>
              </thead>
        {#each paginatedData as user}
            <tr>
                <td>
                  <div class="p-2 bd-highlight">
                    <button class="btn btn-success" type="button" data-bs-toggle="offcanvas" data-bs-target="#myModal{user._id}" aria-controls="offcanvasRight">
                      <i class="bi bi-eye"></i>
                    </button>
                    <div class="side offcanvas offcanvas-end" tabindex="-1" id="myModal{user._id}" aria-labelledby="offcanvasRightLabel">
                    <div class="offcanvas-header">
                    <h5 id="offcanvasRightLabel">{user.designation} Details</h5>
                    <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                    </div>
                    <div class=" offcanvas-body text-left" style="text-align: left;">
                    <div class="container p-1">
                      <div class="row">
                        <div class="col-12">
                          <div class="row">                         
                                <p><b>User Name :</b> {user.name}</p>
                                <p><b>Email :</b> {user.email}</p>
                                <p><b>Password 1:</b> {user.password1}</p>
                                <p><b>Password 2:</b> {user.password2}</p>
                                <p><b>Mobile No. :</b> {user.mobilenumber}</p>
                                <p><b>Role :</b> {user.role}</p>
                                <p><b>officer Name :</b> {user.officername}</p>
                                <p><b>Team Name :</b> {user.team}</p>
                                <p><b>Modules Name :</b> {user.modules}</p>
                                <p><b>Role :</b> {user.role}</p>
                                <p><b>Status :</b> {user.status}</p>
  
                              </div>
                        </div>
                      </div>
                    </div>
                    </div>
                    </div>
                  </div>
                  </td>
                <td class="td">{user.superior}</td>
                <td class="td">{user.officername}</td>
                <td class="td">{user.designation}</td>
                <td class="td">{user.team}</td>
                <td class="td">{user.modules}</td>
                <td class="td">{user.email}</td>
                <td class="td">{user.role}</td>
                <!-- <td class="td">{user.Application}</td> -->
                <td class="td">
                  {#if (user.status === "Active")}
                      <span style="font-weight: bold; color: green;">{user.status}</span>
                  {:else}
                      <span style="font-weight: bold; color: red;">{user.status}</span>
                  {/if}
              </td>
                <td style="width: 398px;">
                  <button style="margin-left: 49.50px;" class="ml-5 btn btn-outline-warning text-dark {user.status === "Deactive" ? 'disabled' : ''}" type="button" data-bs-toggle="modal" data-bs-target="#myModal2{user._id}">
                    <i class="bi bi-pencil-square"></i> Update
                  </button>
                  <div class="modal fade" id="myModal2{user._id}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                    <div class="modal-dialog" style="width:26%">
                      <div class="modal-content">
                        <div class="modal-header">
                          <h4 id="offcanvasRightLabel" style="font-weight: bold;">Edit {user.designation} Details</h4>
                          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                          <div class="container">
                            <div class="row">
                              <div class="col-12">
                                <div class="row">
                                  <!-- Registration form inputs -->
                                  <label>User Name :</label>
                                  <input type="text" placeholder="Username" name="name1" bind:value={user.name}>
                                  <label>Email :</label>
                                  <input type="text" placeholder="Email" name="Email1" bind:value={user.email}>
                                  <label>Mobile Number :</label>
                                  <input type="text" placeholder="Mobile No" name="MobileNo1" bind:value={user.mobilenumber}>
                                  <label>Password 1 :</label>
                                  <input type="text" placeholder="Password" name="password1" bind:value={user.password1}>
                                  <label>Password 2 :</label>
                                  <input type="text" placeholder="Re-enter Password" name="password2" bind:value={user.password2}>
  
                                  <label>Superior :</label>
                                  {#if user.designation === "SP" || user.designation === "IG" || user.designation === "DIG" && team !== "" }
                                  <input type="text" placeholder="Top Superior" name="Email" value="Top Superior" readonly>
                                  {:else if user.designation === "ADDL-SP/DSP"}
                                  <select aria-label="Default select example" bind:value={user.superior}>
                                  <option disabled selected value="">Select Superior</option>
                                  {#each Active_status as Super}
                                  {#if Super.role !== user.role && Super.designation === "SP" || Super.role !== user.role && Super.designation === "ADDL-SP/DSP" ||  Super.role !== user.role && Super.designation==="DSP" } 
                                  <option value={Super.officername}>{Super.officername} - {Super.designation}</option>
                                  {/if}
                                  {/each}
                                  </select>
                                  {:else}
                                  <select aria-label="Default select example" bind:value={user.superior}>
                                  <option disabled selected value="">Select Superior</option>
                                  {#each Active_status as Super}
                                  {#if Super.role !== user.role && Super.designation === "SP" || Super.role !== user.role && Super.designation === "ADDL-SP/DSP" || Super.role !== user.role && Super.designation==="INSPR" || Super.role !== user.role && Super.designation==="DSP"} 
                                  <option value={Super.officername}>{Super.officername} - {Super.designation}</option>
                                  {/if}
                                  {/each}
                                  </select>
                                  {/if}
                                  <label>Role :</label>
                                  <select aria-label="Default select example" bind:value={user.role}>
                                    <option selected value="">Select Role</option>
                                  {#if user.designation === "IG" && user.team === "ADMIN"}
                                      <!-- <option value="IG">IG</option> -->
                                      <option value="{user.designation} ADMIN">{user.designation} ADMIN</option>
                                {/if}
                                {#if user.designation === "DIG" && user.team === "ADMIN"}
                                      <!-- <option value="DIG">DIG</option> -->
                                      <option value="{user.designation} ADMIN">{user.designation} ADMIN</option>
                                {/if}
                                {#if user.designation === "SP"}
                                {#if user.team === "CAT" || user.team === "AP"}
                                      <option value='{user.designation} {user.team}'>{user.designation} {user.team}</option>
                                      <!-- <option value='{user.designation} {user.modules}'>{user.designation} {user.modules}</option> -->
                                {:else if user.team === 'ISOT'}
                                <option value='{user.designation} {user.team}'>{user.designation} {user.team}</option>
                                <option value='{user.designation} {user.modules}'>{user.designation} {user.modules}</option>
  
                                {:else if user.designation === "SP" && user.team === "ADMIN"}
                                    <option value="{user.designation} ADMIN">{user.designation} ADMIN</option>
                                {/if}
                                {/if}
                                {#if user.designation === "ADDLSP"}
                                <option value='{user.designation} {user.team}'>{user.designation} {user.team}</option>
                                {#if user.team === "ISOT"}
                                <option value='{user.designation} {user.modules}'>{user.designation} {user.modules}</option>
                                {/if}
  
                                      <!-- <option value={addlspmodule}>{addlspmodule}</option> -->
                                {/if}
                                {#if user.designation === "ADDL-SP/DSP"}
                                        <option value='{user.designation} {user.team}'>{user.designation} {user.team}</option>
                                        {#if user.team === "ISOT"}
                                        <option value='{user.designation} {user.modules}'>{user.designation} {user.modules}</option>
                                        {/if}
                                      <!-- <option value={dspmodule}>{dspmodule}</option> -->
                                {/if}
                                {#if user.designation === "INSPR"}
                                    {#if user.team === "CAT" || user.team === "AP"}
                                      <option value='{user.designation} {user.team}'>{user.designation} {user.team}</option>
                                      <option value="Analyst">Analyst</option>
                                      <option value="Logger">Logger</option>
                                      <!-- <option value='{user.designation} {user.modules}'>{user.designation} {user.modules}</option> -->
                                    {:else if user.team === 'ISOT'}
                                      <option value='{user.designation} {user.team}'>{user.designation} {user.team}</option>
                                      <option value='{user.designation} {user.modules}'>{user.designation} {user.modules}</option>
                                      <option value="Analyst">Analyst</option>
                                      <option value="Logger">Logger</option>
                                    {/if}
                                {/if}
                                {#if user.designation === "SI"}
                                      <option value='{user.designation} {user.team}'>{user.designation} {user.team}</option>
                                      <option value="Analyst">Analyst</option>
                                      <option value="Logger">Logger</option>
  
                                  {:else if user.designation === "ASI" || user.designation === "HC" || user.designation=== "PC"}
                                    <option value="Analyst">Analyst</option>
                                    <option value="Logger">Logger</option>
                                    <option value="Mailer">Mailer</option>
                                {/if}
                              </select>
  
                                  <label>Designation :</label>
                                  <select aria-label="Default select example" name="designation1" bind:value={user.designation}>
                                    <option value="IG">IG</option>
                                    <option value="DIG">DIG</option>
                                    <option value="SP">SP</option>
                                    <!-- <option value="ADDLSP">ADDLSP</option> -->
                                    <option value="ADDL-SP/DSP">ADDL-SP/DSP</option>
                                    <option value="INSPR">INSPR</option>
                                    <option value="SI">SI</option>
                                    <option value="ASI">ASI</option>
                                    <option value="HC">HC</option>
                                    <option value="PC">PC</option>
                                  </select>
                                  <label>Officer Name :</label>
                                  <input type="text" placeholder="Officer Name/Team Name" name="officer1" bind:value={user.officername}>
                                  <label>Team Name :</label>
                                  <select aria-label="Default select example" name="team" bind:value={user.team}>
                                    <option selected value="" >Select Team Name</option>
                                    <option value="AP">AP</option>
                                    <option value="ISOT">ISOT</option>
                                    <option value="CAT">CAT</option>
                                    <option value="ADMIN">ADMIN</option>
  
                                  </select>
                                    {#if user.team === "AP"}
                                    <label>Modules Name :</label>
                                    <select aria-label="Default select example" name="modules" bind:value={user.modules}>
                                        <option selected value="">Select Module</option>
                                        <!-- <option value="AOB">AOB</option> -->
                                        <option value="AP">AP</option>
                                        <!-- <option value="OTHER">OTHER</option> -->
                                      </select>
                                    {:else if user.team === "CAT"}
                                    <label>Modules Name :</label>
                                       <select aria-label="Default select example" name="modules" bind:value={user.modules}>
                                        <option selected value="">Select Module</option>
                                        <option value="CAT">CAT</option>
                                        <!-- <option value="OTHER">OTHER</option> -->
                                      </select>
  
                                      {:else if user.team === "ISOT" || user.team === "ISOT -1" || user.team === "ISOT -2"}
                                      <label>Modules Name :</label>             
                                      <select aria-label="Default select example" name="modules" bind:value={user.modules} >
                                        <option selected value="">Select Module</option>
                                        <option value="ISOT-M1">ISOT-M1</option>
                                        <option value="ISOT-M2">ISOT-M2</option>
                                        <option value="ISOT-M3">ISOT-M3</option>
                                        <!-- <option value="OTHER">OTHER</option> -->
                                      </select>
                                    {/if}
                                  <label>Status :</label>
                                <select aria-label="Default select example" name="status" bind:value={user.status}>
                                    <option value="Active">Active</option>
                                    <option value="Deactive">Deactive</option>
                                  </select>
                               
                                  <div class="checkbox-group" style="display: flex; flex-wrap: wrap;"> 
                                      {#each user.Application as app}
                                      <div style="display: inline-flex; align-items: center; margin-right: 20px;">
                                          <input class="checking" type="checkbox" id="updatevigor" name="{app}" value="{app}" checked='true' on:change={() => updateappacess(app,user)}>
                                          <label for="">{app}</label>
                                      </div>
                                      {/each}
                                     
                                      {#each user.noaccess as noapp }
                                      <div style="display: inline-flex; align-items: center; margin-right: 20px;">
                                          <input type="checkbox" id="updatevigor" name="{noapp}" value="{noapp}" on:change={() => updateappacess(noapp,user)} >
                                          <label for="">{noapp}</label>
                                      </div>
                                      {/each}
                                  </div> 
                                
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div class="modal-footer">
                          <button type="button" class="btn btn-outline-primary" on:click={updateUser(user)}>Update</button>
                        </div>
                      </div>
                    </div>
                  </div>
  
  
                  <button style="margin-left: 0.2px;" class="btn btn-outline-danger {user.status === "Deactive" ? 'disabled' : ''}" type="button" data-bs-toggle="modal" data-bs-target="#myModal3{user._id}">
                    <i class="bi bi-trash"></i> Delete
                  </button>
                  <div class="modal fade" id="myModal3{user._id}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                    <div class="modal-dialog" style="width: 20%;">
                      <div class="modal-content">
                        <div class="modal-header" >
                          <h3 style="font-weight: bold;">Are you sure delete this User?</h3>
                        </div>
                        <div class="modal-body" style="text-align: left;">
                          <div class="container">
                            <div class="row">
                              <div class="col-12">
                                <div class="row">
                                <p><b>Email :</b> {user.email}</p>
                                <p><b>Designation :</b> {user.designation}</p>
                                <p><b>officer Name :</b> {user.officername}</p>
  
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div class="modal-footer">
                          <button type="button" class="btn btn-outline-danger" on:click={deleteUser(user)}>Yes</button>
                          <button type="button" class="btn btn-outline-primary" data-bs-dismiss="modal" aria-label="Close">No</button>
                        </div>
                      </div>
                    </div>
                  </div>
                </td>
            </tr>
        {/each}
      </table>
    </div>
  </main>
  <div class="page d-flex justify-content-end mr-5" style="margin-right:50px">
    <nav aria-label="Page navigation">
      <ul class="pagination d-flex justify-content-end">
        <p class="mr-3 mt-2" style="margin-right:15px">Showing {paginatedData.length} out of {rowCount} rows</p>
        <li class="page-item">
          <button class="page-link" aria-label="Previous" on:click={goToPreviousPage}>
            <span aria-hidden="true">&laquo;</span>
          </button>
        </li>
        {#each Array.from({ length: Math.min(totalPages, 5) }, (_, i) => i + 1 + (currentPage > 5 ? currentPage - 5 : 0)) as page}
            <li class="page-item">
              <button class="page-link {page === currentPage ? 'selected' : ''}" on:click={() => goToPage(page)}>{page}</button>
            </li>
          {/each}
        <li class="page-item">
          <button class="page-link" aria-label="Next" on:click={goToNextPage}>
            <span aria-hidden="true">&raquo;</span>
          </button>
        </li>
      </ul>
    </nav>
  </div>
  </div>

  