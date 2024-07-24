<script>
  // @ts-nocheck

  import '../global.css';
  import {onMount , onDestroy} from 'svelte';
  import {goto} from '$app/navigation';
  import {basepath} from "$lib/config"
  import { userDetailsStore } from '$lib/datastore.js';
  import flatpickr from 'flatpickr';
  import 'flatpickr/dist/flatpickr.css';

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
  let userDetails;
  userDetailsStore.subscribe(value => {
  userDetails = value;
  });
  onMount(() => {
  // beware of truthy and falsy values
  if (localStorage.getItem("userAuth")==="true"){
  userDetailsStore.set(JSON.parse(localStorage.getItem("userDetails")))
  }
  else{
  goto('/');
  }
  });
  // Function to trigger the download table data as Excel File
  async function fetchDataAndDownloadExcel(user) {
    const response = await fetch(basepath() +'/download-excel', {
      method: 'POST', // or 'GET' depending on your API endpoint
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        id: `${user._id}`, // Replace with the actual ID
        email: `${user.useremail}`, // Replace with the actual email
        type1:`${user.requesttype}`,
        type2: `${user.requesttypes}`,
        category: `${user.requestcategory}`,
        sub:`${user.subtypes}`
      }),
    });
    if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'excel_file.xlsx'; // Specify the desired filename
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(link);
      } else {
        console.error('Failed to download Excel file.');
      }
  };
    let rowCount = 0;
    let cases = []; // Initialize cases as an empty array
    let cases2 = []; // Initialize cases as an empty array
    let filteredData = [];
    let datareq = [];
    let analysisreq = [];
    let DPages = 0; // Total number of pages
    let APages = 0; // Total number of pages
    let data =[];
    let data2 =[];
    let insplist = [];
    let prio = ['Normal',"High",'Emergency'];
    let cats = [];
    let approval = [];
    let pending = [];
    let request_types = [];
// allinONE route connection funtion for fetch all Tickets as per Login Credentials


    let currentPage = 1;
    let currentPage1 = 1;

    let limit = 6; // Adjust this based on your backend configuration
    let pagination = '';
    let pagination2 = ''
    let type = '';
    let mainpage = '';
      async function fetchTickets(page) {
        type = 'My_tickets';
        mainpage = page;

        allinONE();
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

      async function fetchTickets1(page) {
        type = 'Others';
        mainpage = page;
        allinONE();
      }
      function nextPage1() {
        if (currentPage1 < pagination2.total_pages1) {
          currentPage1++;
          fetchTickets1(currentPage1);
        }
      }

      function prevPage1() {
        if (currentPage1 > 1) {
          currentPage1--;
          fetchTickets1(currentPage1);
        }
      }

      onMount(() => {
        fetchTickets(currentPage);
        fetchTickets1(currentPage1)
      });
    let result = '';
    let auto_result = '';
    async function collapse(user){
      auto_result = ''
      const response = await fetch(basepath() + '/newnoresult', {
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
    async function autoresult(id){
      const response = await fetch(basepath() + '/autoresult', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              id:id,
              })
          });
          auto_result = await response.json();
          console.log(auto_result)
    }

    function autoclose(){
      auto_result = '';
      showData1 = false;
    }
      async function allinONE() {
          const response = await fetch(basepath() + '/allinONE', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              type:type,
              email:userDetails.email, 
              team:userDetails.team, 
              modules:userDetails.modules,
              officername:userDetails.officername,
              page:mainpage,
              limit:limit
              })
          });
          if (response.ok){
            const result = await response.json();
              console.log(result);
              if (result.mytickets){
                cases = result.mytickets;
                pagination = result.pagination;
              } else if (result.others){
                cases2 = result.others;
                pagination2 = result.pagination1;
              }
          }
          if (userDetails.role === 'Mailer'){
            // Emergency_alert();
          }
      }


  async function raise_new_data(id,type) {
    // for Convert Analysis to Data Request Tickets
    if (type === 'convert'){
      const url = `/ticketing/raise_new?id=${id}`;
      window.location.href = url;
    }
    else{
      const url = `/ticketing/analysis_proforma?id=${id}`;
      window.location.href = url;
    }
  }


  let showData = false;
  let showData1 = false;

  let comments = '';

  function toggleData() {
    showData = !showData;
  }
  function toggleData1() {
    showData1 = !showData1;
  }

  async function handleSubmits(user) {
    const response = await fetch(basepath()+`/comments/${user._id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        comments_input: comments,
        commentor : `${userDetails.officername}`
      })
      });
      const data = await response.json(`${user._id}`);
      console.log(user);
      collapse(user);
      showData = false;
  }






  let selected1 = 'Select'; // Default selected option
  function handleSelect(option) {
    selected1 = option;
    // Perform any action based on the selected option here
  }
  let officer = '';
  async function asigntoCAT(user, status1, status2) {
    try {
      const response = await fetch(basepath() + `/asign`, {
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          id: `${user._id}`,
          officer: `${user.assign_Officer}`,
          pending: status1,
          approval: status2
        })
      });

      if (response.ok) {
        if (status1 === 'ADDL-SP/DSP Approval Pending' || status1 === 'SP Approval Pending' || status1 === "--") {
          alert('Ticket assigned successfully');
        } else {
          alert('Ticket Rejected!!!!!!!!!');
        }
        fetchTickets1(currentPage1)
      } else {
        // Handle error response
        const errorData = await response.json();
        console.error('Error:', errorData.message);
      }
    } catch (error) {
      console.error('Error occurred:', error.message);
    }
  }









// ============Header Filter Functions for both Tabes My Tickets and Other Tickets =============>>>>
      // My Tickets Filters==========>>>>>>>>>>
     async function header_filter(status,type) {
      console.log(status,type)
      const response = await fetch(basepath() + '/header_filter', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                  type:type,
                  status: status,
                  email: userDetails.email,
              })
          });

          if (response.ok){
            const result = await response.json();
              console.log(result,'//////////////////............../////');
              if (result.mytickets){
                cases = result.mytickets;
                pagination = result.pagination;
              }}
         
      }

      async function header_filter2(status,type) {
      const response = await fetch(basepath() + '/header_filter2', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                  type: type,
                  status: status,
                  designation: userDetails.designation,
                  role: userDetails.role,
                  email: userDetails.email,
                  team: userDetails.team,
                  modules: userDetails.modules,
                  officer: userDetails.officername,


              })
          });

          if (response.ok){
            const result = await response.json();
              console.log(result);
              if (result.mytickets){
                cases2 = result.mytickets;
                pagination2 = result.pagination;
              }}
         
      }

      async function fetch_status(type){
        const response = await fetch(basepath() + '/fetch_status', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                  type:type,
                  email: userDetails.email,
              })
          });
          const result = await response.json();
          data = result;
      }
      async function fetch_status2(type){
        const response = await fetch(basepath() + '/fetch_status2', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                  type: type,
                  designation: userDetails.designation,
                  role: userDetails.role,
                  email: userDetails.email,
                  team: userDetails.team,
                  modules: userDetails.modules,
                  officer: userDetails.officername,
              })
          });
          const result = await response.json();
          data2 = result;
      }
      

      let startDate;
      let endDate;
      async function Date_range(startDate, endDate) {

        // console.log(startDate,endDate)
        const originalDate1 = new Date(startDate);
        const date1 = originalDate1.toLocaleDateString('en-GB'); // Format to DD/MM/YYYY

        const originalDate2 = new Date(endDate);
        const date2 = originalDate2.toLocaleDateString('en-GB'); // Format to DD/MM/YYYY

        const rangeStartDate = date1;
        const rangeEndDate = date2;
        console.log(rangeStartDate,rangeEndDate)

        const response = await fetch(basepath() + '/date-filter', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                  fromdate: rangeStartDate,
                  todate:rangeEndDate,
                  email: userDetails.email,
              })
          });

          if (response.ok){
            const result = await response.json();
              console.log(result);
              if (result.mytickets){
                cases = result.mytickets;
                pagination = result.pagination;
              }}
         
      }
      

     async function Date_range1(startDate, endDate) {

        // console.log(startDate,endDate)
        const originalDate1 = new Date(startDate);
        const date1 = originalDate1.toLocaleDateString('en-GB'); // Format to DD/MM/YYYY

        const originalDate2 = new Date(endDate);
        const date2 = originalDate2.toLocaleDateString('en-GB'); // Format to DD/MM/YYYY

        const rangeStartDate = date1;
        const rangeEndDate = date2;
        
        const response = await fetch(basepath() + '/date-filter2', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                  fromdate: rangeStartDate,
                  todate:rangeEndDate,
                  designation: userDetails.designation,
                  role: userDetails.role,
                  email: userDetails.email,
                  team: userDetails.team,
                  modules: userDetails.modules,
                  officer: userDetails.officername,
              })
          });

          if (response.ok){
            const result = await response.json();
              console.log(result);
              if (result.mytickets){
                cases2 = result.mytickets;
                pagination2 = result.pagination;
              }}
      }
      
// ===================================================================================================================================

  function clear_range(){
    console.log("clear_range")
    startDate = ''
    endDate = ''
    const dateRangePickerInput = document.getElementById("dateRangePicker");
      if (dateRangePickerInput) {
        dateRangePickerInput.value = "";
      }
    Date_range(startDate,endDate)
    fetchTickets(currentPage)
  // console.log(startDate,endDate,'..............after clear...............')
  }

  function clear_range1(){
    console.log("clear_range")
    startDate = ''
    endDate = ''
    const dateRangePickerInput = document.getElementById("dateRangePicker11");
      if (dateRangePickerInput) {
        dateRangePickerInput.value = "";
      }
    Date_range1(startDate,endDate)
    fetchTickets1(currentPage1)
  // console.log(startDate,endDate,'..............after clear...............')
  }

  // Paginations Functions---------------------------->
  onMount(() => {
    // beware of truthy and falsy values
    if (localStorage.getItem("userAuth") === "true") {
      // console.log('auth is passed')
    } else {
      goto('/');
    }
  })


  async function deleteRow(id,msisdn) {
    // Delete Selected Rows Button of Table in View Sections
    await fetch(basepath() + '/delete_row', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `id=${id}&msisdn=${msisdn}`
    });
    // const message = await response.json();
    allinONE();
  }

  


  async function deleteSelectedRows() {
    // Delete Selected Rows of Table in View Sections
    const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    const rowsToDelete = [];

    checkboxes.forEach((checkbox) => {
      const rowId = checkbox.id.split("_")[1];
      const msisdn = checkbox.dataset.msisdn;
      if (rowId !== undefined && msisdn !== undefined){
        rowsToDelete.push({ id: rowId, msisdn: msisdn });
      }
    });

    if (rowsToDelete.length === 0) {
      return; // No rows selected, do nothing
    }
    const confirmation = confirm("Are you sure you want to delete the selected rows?");
    if (!confirmation) {
    allinONE();
      return; // User canceled the deletion
    }

    for (const { id, msisdn } of rowsToDelete) {
      await deleteRow(id, msisdn); // Call your existing deleteRow function for each selected row
    }

    alert("Selected rows deleted successfully");
    allinONE();
  }

  // Download Tickets Functions as per selected Conditions

      async function downloadDatapending() {
        updateFormattedDate()
        const response = await fetch(basepath() + '/statuspending', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ 
            team: userDetails.team, 
            email:userDetails.email
            })
        });
        const data = await response.json();
        // console.log(data);
        const text = JSON.stringify(data);
        const blob = new Blob([text], {
          type: 'text/plain'
        });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = userDetails.officername + "_FPD_"+ formattedDate + ".txt";
        link.click();
        URL.revokeObjectURL(url);
      }

      let selected_tickets = '';
      let excel_data=[];
      function clearCheckboxes() {
        selected_tickets = '';
        ids = '';
        console.log("requesttypes_updated: ", selected_tickets)
        const checkboxes1 = document.querySelectorAll('.mycheck');
        checkboxes1.forEach((checkbox1) => {
          checkbox1.checked = false;
        });
        fetchTickets(currentPage);
        fetchTickets1(currentPage1)
      }

      
      async function downloadDatasuccess(select) {
        updateFormattedDate()
        const response = await fetch(basepath() + '/statussuccess', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ 
            team: userDetails.team, 
            designation:userDetails.designation,
            role:userDetails.role,
            select:select
          })
        });
        console.log(select,"llllllllllllllllllllllllllll")
        const data = await response.json();
        console.log(data);
        const text = JSON.stringify(data);
        const blob = new Blob([text], {
          type: 'text/plain'
        });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = userDetails.officername + "_SD_"+ formattedDate +".txt";
        link.click();
        URL.revokeObjectURL(url);
        clearCheckboxes();
      }
      
      async function mytickets() {
        updateFormattedDate();
        const response = await fetch(basepath() + '/mytickets', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ 
            email: userDetails.email, 
            })
        });
        const data = await response.json();
        console.log(data);
        const text = JSON.stringify(data);
        const blob = new Blob([text], {
          type: 'text/plain'
        });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = userDetails.officername + "_MY_"+ formattedDate +".txt";
        link.click();
        URL.revokeObjectURL(url);
      }


      let ids = [];
      async function download(){
        updateFormattedDate();
        for (let i = 0; i < selected_tickets.length; i++) {
            ids.push(selected_tickets[i]);
        }
      try {
      const response = await fetch(basepath() + '/download_for_mailer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({id : ids})
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
    } catch (error) {
      console.error(error);
    }
    clearCheckboxes();
    ids = [];
  }
  
  //   import data
  let files = '';
  async function uploadfiles() {
    // Import Automation Files Function
    if (files === "") {
      alert('Please Upload File.....');
      return;
    }
    const response = await fetch(basepath() + '/uploadfiles', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        files: await files[0].text()
      })
    });

    allinONE();
  }

let insp = "";

  async function fetch_officers(type){
    const response = await fetch(basepath() + '/fetch_ins', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          type: type,
          team: userDetails.team,
          modules: userDetails.modules
        })
      });
      const data = await response.json();
      insplist = data;
    }








const today1 = new Date();
let day1 = today1.getDate();
let month1 = today1.getMonth() + 1;
let year1 = today1.getFullYear();
let hours = today1.getHours();
let minutes = today1.getMinutes();
let seconds = today1.getSeconds();
let milliseconds = today1.getMilliseconds();

// Add leading zero if needed
month1 = month1 < 10 ? `0${month1}` : month1;
day1 = day1 < 10 ? `0${day1}` : day1;
hours = hours < 10 ? `0${hours}` : hours;
minutes = minutes < 10 ? `0${minutes}` : minutes;
seconds = seconds < 10 ? `0${seconds}` : seconds;

let formattedDate2 = `${day1}-${month1}-${year1} ${hours}:${minutes}:${seconds}:${milliseconds}`;

  async function submitedRecord(user,status1,status2) {
      if (insp === `${userDetails.officername}` ) 
      {
        alert('Same Officer Can Not Be Selected.');
        return;
      }
      const response = await fetch(basepath() + '/submitedRecord', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          id: `${user._id}`,
          email: `${user.useremail}`,
          officername : `${userDetails.officername}`,
          role : `${userDetails.role}`,
          designation : `${userDetails.designation}`,
          newinspr: insp,
          pending:status1,
          approval:status2,
          sendDateTime : formattedDate2,
          options: selectedOption,
        })
      })
      const data = await response.json();
      if (data.user_creation_error){
        alert(data.user_creation_error)
        fetchTickets(currentPage);
        fetchTickets1(currentPage1)
      }
      else{
        if (data.length > 0){
          header_filter(`${user.pending}`,'pending')
        }
        else if (data2.length > 0){
          header_filter2(`${user.pending}`,'pending')
        }
        else{
          fetchTickets(currentPage);
          fetchTickets1(currentPage1)
        }
      }
    
  }

  let buttonDisabled = true;
  function handleCheckboxChange(event) {
    // Delete Rows of MSISDN one by one
    const checkboxId = event.target.id;
    const deleteButtonId = `button[data-id="${checkboxId.replace("checkbox_", "")}"]`; // Get the id of the corresponding delete button
    const deleteButton = document.querySelector(deleteButtonId);
    const searchButtonId = `button[data-id2="${checkboxId.replace("checkbox_", "")}"]`; // Get the id of the corresponding delete button
    const searchButton = document.querySelector(searchButtonId); // Find the corresponding delete button
    if (deleteButton) {
      deleteButton.disabled = !event.target.checked; 
    }
    if (searchButton) {
      searchButton.disabled = !event.target.checked;
      
    }
    
  }


  let editalert = "YES";
  async function updateField(userId, msisdn, field, value) {
    // Update fields editable inputs if edit edit field will be convert to YES in Red color text
    const response = await fetch(basepath() + '/updatefields', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        id: userId,
        msisdn: msisdn,
        field: field,
        value: value,
        edit : editalert
      })
    });

    updatedfielddata = await response.json();
    console.log(userId, msisdn, field, value);
  }
export async function updateRecord(id, status) {
      const response = await fetch(`http://127.0.0.1:5000/records/${id}`, {
          method: 'POST',
          body: JSON.stringify({ status }),
          headers: {
            'Content-Type': 'application/json'
          }
      });
      return await response.json();
  }



  async function deleteTicket(user) { 
      //For Delete Ticket
      try{
      const response = await fetch(`${basepath()}/delete_ticket`,{
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          id : `${user._id}`,
          token : `${user.token}`,
        })
      });
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
      
      fetchTickets(currentPage);
  }

  let selectedOption = 'Select';// Default selected option
  let uniqid = '';
  function handleOptionSelect(option,id) {
      selectedOption = option;
      uniqid  = id;
      // Perform any action based on the selected option here
  }

  let selected= 'Select'; // Default selected option
  function close(){
    window.location.reload();
  }
  let searchValue = "";
  async function search(type) {
    const response = await fetch(basepath()+"/Data_search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({type:type, value: searchValue ,email:userDetails.email}),
    });
    if (response.ok){
      const result = await response.json();
        console.log(result);
        if (result.mytickets){
          cases = result.mytickets;
          pagination = result.pagination;
        }
    }
  }
  let searchValue2 = "";

  async function search2(type) {
    const response = await fetch(basepath()+"/Data_search2", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        type:type, 
        value: searchValue2,
        designation:userDetails.designation,
        role:userDetails.role,
        team:userDetails.team,
        email:userDetails.email,
        modules:userDetails.modules,
        officer:userDetails.officername
      }),
    });
    if (response.ok){
      const result = await response.json();
        console.log(result);
        if (result.mytickets){
          cases2 = result.mytickets;
          pagination2 = result.pagination;
        }
    }
  }
  
  // async function Emergency_alert() {
  //   const fetchData = async () => {
  //     try {
  //       const response = await fetch(basepath() + "/emergency_alert", {
  //         method: "POST",
  //         headers: {
  //           "Content-Type": "application/json",
  //         },
  //         body: JSON.stringify({
  //           data: analysisreq,
  //         }),
  //       });
  //       if (!response.ok) {
  //         throw new Error(`Fetch failed with status ${response.status}`);
  //       }
  //       const count = await response.json();
  //       if (count.count) {
  //         showNotification(count.count);
  //       }
  //     } catch (error) {
  //       console.error("Error during emergency alert fetch:", error);
  //     }
  //   };
  //   const showNotification = (ticketCount) => {
  //     if ('Notification' in window) {
  //       Notification.requestPermission().then((permission) => {
  //         if (permission === 'granted') {
  //           new Notification('Emergency Ticket Alert', {
  //             'body': `You have ${ticketCount} Emergency Tickets in Other Tickets Tab!!!!`,
  //             'icon': '../src/public/Images/alert.png'
  //           });
  //         }
  //       });
  //     } else {
  //       console.error('This browser does not support notifications.');
  //     }
  //   };
  //   // Initial call
  //   fetchData();
  //   // Set up a time interval to call the function every 30 seconds
  //   setInterval(fetchData, 30000);
  // }


  let msisdn = [];
  let selectedOption2 = 'Select';// Default selected option
  let uniqid2 = '';
  function handleOptionSelect2(option,id) {
    selectedOption2 = option;
    uniqid2  = id;
    // Perform any action based on the selected option here
  }
  let mailer_remark = '';
  async function status_update(user,status) {
    // console.log(selectedrows)
    const response  = await fetch(basepath() + '/status_update', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 
        id: `${user._id}`, 
        number:msisdn,
        status:status,
        remark:mailer_remark,
        designation:`${userDetails.designation}`,
        team : `${userDetails.team}`
      })
    });
    console.log(`${user._id}`,msisdn,status)
    autoresult(`${user._id}`);
    showData1 = false;
    clearCheckboxes1();
  }
  function handleCheckboxChange1(){
    const checkboxes = Array.from(document.querySelectorAll('input[type="checkbox"]:checked')).map(checkbox => checkbox.value)
    msisdn = checkboxes;
  }

  function clearCheckboxes1() {
        msisdn = []
        const checkboxes1 = document.querySelectorAll('input[type="checkbox"]:checked');
        checkboxes1.forEach((checkbox1) => {
          checkbox1.checked = false;
        });
      }
  
  </script>
  <style>

.no-data {
    animation: bounce 1s infinite alternate; /* Example animation */
    font-size: xx-large;
    font-family: serif;
    font-weight: bold;
    text-shadow: 2px 15px 10px rgba(0, 0, 0, 0.692);
    -webkit-text-stroke: 2px rgba(148, 148, 148, 0.315); /* Webkit prefix */
    color: transparent;
    background: linear-gradient(to right, #1c92d2, #f2fcfe); /* Gradient colors */
    -webkit-background-clip: text; /* Webkit prefix */
    background-clip: text;
}

  @keyframes bounce {
    from {
      transform: translateY(0);
    }
    to {
      transform: translateY(60px);
    }
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
    form {
      box-shadow: 0 .5rem 1rem rgba(0, 0, 0, .15) !important;
      background-color: #dddddd;
      border-radius: 10px;
      margin-bottom: 50px;
    }
    a {
      text-decoration: none;
      cursor: pointer;
    }
    .checkbox-size {
      width: 20px;
      height: 20px;
    }
    .disabled {
      opacity: 0.5;
      pointer-events: none;
    }
    #hidden {
      display: none;
      overflow: hidden;
    }
    .mycol {
      cursor: pointer;
    margin: 18px;
    border-radius: 10px;
    margin-top: 10px;
    }
  
    table, th, td {
      border-collapse: collapse;
      text-align: center;
      padding: 0.75rem;
    }
  
    .divScroll {
      overflow: scroll;
      height: 50px;
      width: 190px;
    }
    .editable-cell {
      width: fit-content;
      text-align: center;
      background-color: lightcyan;
      width: 170px;
      outline: none;
    }
    h3 {
      margin-left: 20px;
      margin-top: 10px;
    }
    .mnp {
      width: 100px;
    }
    .td {
      text-align: center;
      vertical-align: middle;
    }
    #filter {
      margin-top: -50px;
    }
    .submit {
      margin-top: 15px;
      display: flex;
      margin-left: 160px;
    }
    .cq {
      margin-top: 11px;
      text-align: center;
    }
    .side {
      font-size: 15px;
      width: 30%;
    }
    .mnp1 {
      width: 102px;
      color: green;
      font-weight: bold;
    }
    #status {
      border-radius: 200px;
      width: 100px;
    }
    .eye {
      margin-top: 2px;
    }
    .mark1 {
      color: red;
      font-weight: bold;
    }
    .mark2 {
      color: green;
      font-weight: bold;
    }
    .scroll-table {
      max-height: 255px; /* Adjust the height as needed */
      overflow: scroll;
    }
    .scroll-table1 {
      height: 590px;
      overflow: scroll;
    }
    .scroll-table2 {
      height: 300px;
      overflow: scroll;
    }
    .nav-link {
      background-color: rgb(197, 197, 197);
    }
    .page {
      position: fixed;
      bottom: 0;
      right: 0;
      margin: 5px; /* Adjust the margin as needed */
    }
    .page_border {
      border: 4px solid #000000; /* Add a border around the container */
      box-sizing: border-box;
      height: 92.2%;
      margin: 0;
      padding: 0;
      border-radius: 5px;
      box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.2);
      /* position: relative; */
      background:linear-gradient(120deg, white, white);
    }
    .table-bordered th, .table-bordered td {
      border: 1px solid #dee2e6;
      padding: 0.75rem;
      border-collapse: collapse;
    }
    .fs-5 {
      font-size: 1.25rem!important;
      font-weight: 500;
    }
    .modal-title {
      margin-bottom: 0;
      line-height: 1.5;
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
    .sdr {
      width: 430px;
      height: 70px;
      text-wrap: wrap;
    }
    .td1 {
      border-collapse: collapse;
      text-align: center;
      vertical-align: middle;
      border: none;
      background-color: rgb(238, 238, 238) !important;
    }
    .tr1 {
      border-collapse: collapse;
      text-align: center;
      padding: 0 0 0 0;
    }
    .sticky-header {
      position: sticky;
      top: 0;
      background-color: #563d7c;
      color: white;
      z-index: 1000;
    }
    .selected{
      background-color: rgb(40, 139, 196);
      color: white;
    }
    .hide{
      display: none;
    }
  </style>
  
  <nav class="navbar navbar-dark bg-dark" style="background-color: #343a40 !important;">
  <div class="d-flex mr-1">
    <div class="bd-highlight">
      <button class="btn  btn-outline-dark mt-1 mr-1" style="color: #343a40;border-color: #343a40">
        <a href="#" class="text-white"><i class="bi bi-house-door-fill"></i> Home</a></button>
      </div>  
  <div class="bd-highlight">
    <button class="btn  btn-outline-primary mt-1 mr-1">
      <a href="/ticketing/Dashboard" class="text-white"><i class="bi bi-file-earmark-bar-graph"></i> Report</a></button>
    </div>
    <div class="bd-highlight">
      <button class="btn  btn-outline-primary mt-1" style="margin-left: 5px;">
        <a href="/ticketing/Nickname" class="text-white"><i class="bi bi-file-earmark-bar-graph"></i> Nickname</a></button>
      </div>
  </div>
  <div class="pt-0 ">
    <div class="d-flex justify-content-end bd-highlight">
      <div class="p-2 bd-highlight">
        <div class="search-container">
        </div>
    </div>
    {#if userDetails.role === "Mailer" || userDetails.team === 'ADMIN'}
      <div class="p-2 bd-highlight">
        <div class="dropdown">
          <button class="btn btn-outline-primary text-white dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false"> Export Data </button>
          <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
            <li>
              <a class="dropdown-item" on:click={mytickets}>Export My Tickets</a>
            </li>
            {#if userDetails.role === "Mailer"}
            <li>
              <a class="dropdown-item" on:click={()=> download('Excel')}>Export as Excel</a>
              </li>
              {/if}
               <li>
                <a class="dropdown-item" on:click={downloadDatasuccess(selected_tickets)}>Export Success Data</a>
              </li>
            </ul>
          </div>
        </div>
        {/if}
        <div class="p-2 bd-highlight">
        <!-- <input accept="text/txt" bind:files id="avatar" name="avatar" type="file"/> -->
        <button class="btn btn-outline-warning" data-bs-toggle="modal" data-bs-target="#myModal">
          <a href="" class="text-white">Import Data</a>
        </button>
        <div class="modal fade" id="myModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
          <div class="modal-dialog" style="width: 25%;margin-top:70px">
            <div class="modal-content">
              <div class="modal-header">
                <h1 class="modal-title fs-5" style="font-size: 1.25rem;font-weight: 500;margin-bottom: 0; line-height: 1.5;font-family: sans-serif;" id="exampleModalLabel">Upload your File</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <input class="mt-3 form-control" style="font-family: sans-serif;color: #495057" accept="text/txt" bind:files id="files" name="files" type="file" />
                <button type="button" on:click={uploadfiles}  data-bs-dismiss="modal" class="submit btn btn-outline-success">Upload</button>
    
              </div>
            </div>
          </div>
        </div>
    </div>
    <div class="p-2 bd-highlight">                                   
    <button class="btn  btn-outline-success text-white" on:click={()=> goto('/ticketing/newticket')}>
    <i class="bi bi-file-earmark-plus-fill"></i> New Request</button>
    </div>
  </nav>
  <div class="page_border">
    <main>
      <div>
        <h3 style="font-weight: bold;">{userDetails.officername}</h3>
        <p style="margin-left: 20px;margin-top: 10px;">{userDetails.team} Team, {userDetails.designation}</p>
    </div>
    {#if userDetails.role !== "Logger" && userDetails.designation !== "SI" || userDetails.designation === "SI" && userDetails.role === "Analyst"}
    <ul class="nav nav-pills nav-tabs" id="myTab" role="tablist">
      <li class="nav-item" role="presentation">
        <a class="nav-link active" id="data-request-tab" data-bs-toggle="tab" href="#data-request" on:click={()=> fetchTickets(currentPage)} role="tab" aria-controls="data-request" aria-selected="true">My Tickets {pagination.total_tickets}</a>
      </li>
      <li class="nav-item" role="presentation">
        <a class="nav-link" id="analysis-request-tab" data-bs-toggle="tab" href="#analysis-request" on:click={()=> fetchTickets1(currentPage1)} role="tab" aria-controls="analysis-request" aria-selected="false">Other Tickets {pagination2.total_tickets1}</a>
      </li>
    </ul>
    {/if}
    <!-- Tab content -->
    <div class="tab-content" id="myTabContent">
      <!-- Data Request Tab content -->
      <div class="tab-pane fade show active" id="data-request" role="tabpanel" aria-labelledby="data-request-tab">
        <div class="search_bar">
          {#if userDetails.role !== "Logger" || userDetails.designation !== "SI" || userDetails.role === "Analyst"}
          <h2 style="font-size: 2rem;"></h2>
          {/if}
          <div class="search btn-group" style='margin-bottom: 10px;margin-right: 28px'>
            <input type="search" style="border-radius: 40px 0 0 40px" bind:value={searchValue} placeholder="Search Data">
            <button class="btn btn-outline-primary" style="border-radius: 0 40px 40px 0;cursor: pointer;height: 40px;width: 64px;margin: 0;" type="button" on:click={() => search('My_tickets')}><i class="bi bi-search"></i></button>
        </div>
    </div>

        
{#if cases.length > 0}
    <div class="table-responsive text-nowrap scroll-table1">
    <table class="table table-striped table-hover" id="mytb">
    <thead class="table-dark" id="myhead">
      <tr>
      <th></th>
      <th>
        <button style="font-weight: bold;" class="btn btn-dark dropdown-toggle" type="button" id="statusFilterDropdown" data-bs-toggle="dropdown" aria-expanded="false">
          Priority
        </button>
        <ul class="dropdown-menu" aria-labelledby="statusFilterDropdown">
          <li>
            <a class="dropdown-item" href="#" on:click={() => fetchTickets(currentPage)}>All</a>
          </li>
          {#each prio as status}
          <li>
            <a class="dropdown-item" href="#" on:click={() => header_filter(status,'priority')}>{status}</a>
          </li>
          {/each}
        </ul>    
      </th>
      <th>
        <button style="font-weight: bold;" class="btn btn-dark dropdown-toggle" type="button" id="statusFilterDropdown" data-bs-toggle="dropdown" aria-expanded="false">
            Date
        </button>
        <ul class="dropdown-menu" aria-labelledby="statusFilterDropdown">
          <li>
            <a class="dropdown-item" href="#" on:click={clear_range}>Clear</a>
          </li>
          <li>
            <input class="border-0" use:flatpickr={{mode:'range', dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today', onChange:(selectedDates) => {startDate = selectedDates[0];endDate = selectedDates[1];}}} 
              placeholder="Select Range" id="dateRangePicker" on:input={Date_range(startDate,endDate)}>
          </li>
        </ul>
      </th>
      <th>TicketID</th>
      <th>
        <button style="font-weight: bold;" on:click={()=> fetch_status('approval')}  class="btn btn-dark dropdown-toggle" type="button" id="statusFilterDropdown" data-bs-toggle="dropdown" aria-expanded="false">
          Approval Status
        </button>
        <ul class="dropdown-menu" aria-labelledby="statusFilterDropdown">
          <li>
            <a class="dropdown-item" href="#" on:click={() => fetchTickets(currentPage)}>All</a>
          </li>
          {#each data as status}
          <li>
            <a class="dropdown-item" href="#" on:click={() => header_filter(status,'approval')}>{status}</a>
          </li>
          {/each}
        </ul> 
      </th>
      <th>
        <button style="font-weight: bold;" on:click={()=> fetch_status('pending')} class="btn btn-dark dropdown-toggle" type="button" id="statusFilterDropdown" data-bs-toggle="dropdown" aria-expanded="false">
          Pending Status
        </button>
        <ul class="dropdown-menu" aria-labelledby="statusFilterDropdown">
          <li>
            <a class="dropdown-item" href="#" on:click={() => fetchTickets(currentPage)}>All</a>
          </li>
          {#each data as status}
          <li>
            <a class="dropdown-item" href="#" on:click={() => header_filter(status,'pending')}>{status}</a>
          </li>
          {/each}
        </ul> 
      </th>
      <th>
        <button style="font-weight: bold;" on:click={()=> fetch_status('category')} class="btn btn-dark dropdown-toggle" type="button" id="statusFilterDropdown" data-bs-toggle="dropdown" aria-expanded="false">
          Category
        </button>
        <ul class="dropdown-menu" aria-labelledby="statusFilterDropdown">
          <li>
            <a class="dropdown-item" href="#" on:click={() => fetchTickets(currentPage)}>All</a>
          </li>
          {#each data as status}
          <li>
            <a class="dropdown-item" href="#" on:click={() => header_filter(status,'category')}>{status}</a>
          </li>
          {/each}
        </ul> 
      </th>
      <th>
        <button style="font-weight: bold;" on:click={()=> fetch_status('requesttype')} class="btn btn-dark dropdown-toggle" type="button" id="statusFilterDropdown" data-bs-toggle="dropdown" aria-expanded="false">
          Request Types - Subtypes
        </button>
        <ul class="dropdown-menu" aria-labelledby="statusFilterDropdown">
          <li>
            <a class="dropdown-item" href="#" on:click={() => fetchTickets(currentPage)}>All</a>
          </li>
          {#each data as status}
          <li>
            <a class="dropdown-item" href="#" on:click={() => header_filter(status,'requesttype')}>{status}</a>
          </li>
          {/each}
        </ul> 
      </th>
      <th>Tickets Details</th>
      </tr>
    </thead>
     {#each cases as user}
      <tr>
        <td>
          {#if userDetails.role === 'Analyst' && user.assign_Officer === userDetails.officername}
          <button class="btn btn-outline-primary" style="height: 36px;" on:click={()=> raise_new_data(user._id)}>
            <i class="bi bi-arrow-up-right-square" style="width: 50px; height:50px"></i>
          </button>
          {/if}

          {#if userDetails.role === "Mailer"}
          <input
          type="checkbox"
          class="mycheck checkbox-size mt-2 ml-5"
          style="text-align: center; vertical-align: middle;"
          bind:group={selected_tickets}
          value={user._id}/>
        {/if}

        {#if userDetails.role === 'Analyst' && userDetails.team === 'CAT' || userDetails.designation === 'SP' && userDetails.team === 'ADMIN' || userDetails.designation === 'ADDL-SP/DSP' && userDetails.team === 'CAT'}
          {#if user.requestcategory === 'Note'}
            <button class="btn btn-link dropdown-toggle mt-2" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false"><i class="bi bi-three-dots-vertical"></i></button>
              <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1" style="background-color: white;">
                <li>
                  <a class="dropdown-item" data-bs-toggle="tooltip" data-bs-placement="top" title='Fill Analysis Request Proforma' on:click={()=> raise_new_data(user._id,'proforma')}>
                    <i class="bi bi-file-text-fill"></i> Analysis Proforma</a>
                </li>
              </ul>
          {/if}
        {/if}
      {#if user.pending === 'Fetch_Pending_Data' || user.pending === 'Approval Pending' || user.pending === 'Analysis Note Raised'}
        <button class="btn btn-outline-danger mt-2 {user.pending === 'Fetch_Pending_Data' || user.pending === 'Approval Pending' || user.pending === 'Analysis Note Raised' || user.pending === 'Inspector Approval Pending' || user.pending === 'DSP Approval Pending'  || user.pending === 'SP Approval Pending' ? '' : 'hide'}" type="button" data-bs-toggle="modal" data-bs-target="#myModal3{user._id}">
              <i class="bi bi-trash"></i>
            </button>
            <div class="modal fade" id="myModal3{user._id}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
              <div class="modal-dialog" style="width: 30%;">
                <div class="modal-content">
                  <div class="modal-header">
                  </div>
                  <div class="modal-body" style="text-align: left;"> 
                    <div class="container">
                      <div class="row">
                        <div class="col-12">
                          <div class="row">
                          <h4>Are you sure to delete this Ticket?</h4>
                          <p><b>Tickect Token Id :</b> {user.token}</p>
                          <p><b>Ticket Type :</b> {user.requesttype}</p>
                      
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-outline-danger" data-bs-dismiss="modal" on:click={deleteTicket(user)}>Yes</button>
                    <button type="button" class="btn btn-outline-primary" data-bs-dismiss="modal" aria-label="Close">No</button>
                  </div>
                </div>
              </div> 
            </div>
          {#if userDetails.designation === "INSPR" && userDetails.role !== "Analyst"}
          <div class="btn-group mt-2">
            {#if selectedOption === "Send" && uniqid === user._id}
            <button data-bs-toggle="tooltip" data-bs-placement="top" title='Send to DSP' on:click={() => submitedRecord(user,`${userDetails.superior} Approval Pending`,"-")} type="button" class= "ml-2 btn btn-outline-success  {user.pending=== "Fetch_Pending_Datas" || user.pending=== "Ins Approval Pending" || user.pending === "Mail Sent" || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending" || user.pending === `${userDetails.superior} Approval Pending` ||user.pending === "Mail Under Process" ? 'hide' : ''}" >
                <i class="bi bi-send"></i> Send
              </button>
                {:else if selectedOption === "Self Approve" && uniqid === user._id} 
                {#if user.requestcategory === 'Analysis Request' && userDetails.team === "AP" || user.requestcategory === 'Analysis Request' && userDetails.team === "ISOT"}
                <button on:click={() => submitedRecord(user,"Assign to CAT Ins","Approved by Ins")} type="button" class= "ml-2 btn btn-outline-success {user.pending === "Mail Sent"   || user.pending === "SP Approval Pending"? 'hide' : ''}" >
                <i class="bi bi-send"></i> Approve
                </button>
                {:else if user.requestcategory === 'Analysis Request' && userDetails.team === "CAT" }
                <button on:click={() => submitedRecord(user,"--","Approved by Ins")} type="button" class= "ml-2 btn btn-outline-success {user.pending === "Mail Sent" ||user.pending=== "Fetch_Pending_Data" ||  user.pending === "SP Approval Pending" || user.pending === "--"? 'hide' : ''}" >
                <i class="bi bi-send"></i> Approve
                </button>
                {:else if userDetails.team === "CAT" && user.requestcategory === 'Data Request'}
                          {#if user.token.includes("_CO") && user.team === "AP" || user.token.includes("_CO") && user.team === "ISOT"}
                          <button data-bs-toggle="tooltip" data-bs-placement="top" title='Self Approve' on:click={() => submitedRecord(user,"Mail Under Process","Approved by CAT Ins")} type="button" class= "ml-2 btn btn-outline-success {user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" || user.pending === `${user.superior} Approval Pending`
                            || user.pending=== "Rejected by Ins" || user.pending === "Mail Sent" || user.pending=== "Rejected by DSP" || user.pending === "Rejected by SP"   || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                              Self
                            </button>
                            {:else}
                            <button data-bs-toggle="tooltip" data-bs-placement="top" title='Self Approve' on:click={() => submitedRecord(user,"Mail Under Process","Approved by Ins")} type="button" class= "ml-2 btn btn-outline-success {user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" 
                              || user.pending=== "Rejected by Ins" || user.pending === "Mail Sent" || user.pending=== "Rejected by DSP" || user.pending === "Rejected by SP"   || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                              Self
                              </button>
                          {/if}
                {:else}
                  <button data-bs-toggle="tooltip" data-bs-placement="top" title='Self Approve' on:click={() => submitedRecord(user,"Mail Under Process","Approved by Analyst")} type="button" class= "ml-2 btn btn-outline-success {user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" 
                    || user.pending=== "Rejected by Ins" || user.pending === "Mail Sent" || user.pending=== "Rejected by DSP" || user.pending === "Rejected by SP"   || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                    Self
                    </button>
                {/if}
             {:else}
            <button type="button" class="btn btn-outline-success {(user.requestcategory === 'Analysis Request' && userDetails.team === 'CAT') || user.pending=== "Ins Approval Pending" || user.pending === 'Assign to CAT Ins' || user.approval.includes('Assigned') || user.pending === "Mail Sent" || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" || user.pending === 'Ticket_Closed' ? 'hide' : ''}" disabled>Select</button>
            {/if}
            <button
            class="btn btn-outline-success dropdown-toggle {(user.requestcategory === 'Analysis Request' && userDetails.team === 'CAT') ||user.pending=== "Ins Approval Pending" || user.pending === 'Assign to CAT Ins' || user.approval.includes('Assigned') || user.pending === "Mail Sent" || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" || user.pending === 'Ticket_Closed' ? 'hide' : ''}" type="button" data-bs-toggle="dropdown" aria-expanded="false">
              <span class="sr-only"></span>
            </button>
            <div class="dropdown-menu">
              <a class="dropdown-item" on:click={() => handleOptionSelect('Send',user._id)}>Send</a>
            <a class="dropdown-item" on:click={() => handleOptionSelect('Self Approve',user._id)}>Self Approve</a>
            </div>
          </div>
          {:else if userDetails.designation === "ADDL-SP/DSP"}
          <div class="btn-group mt-2">
            {#if selectedOption === "Send" && uniqid === user._id}
            <button data-bs-toggle="tooltip" data-bs-placement="top" title='Send to SP' on:click={() => submitedRecord(user,`${userDetails.superior} Approval Pending`,"-")} type="button" class= "ml-2 btn btn-outline-success  {user.pending=== "Ins Approval Pending" || user.pending === "Mail Sent"   || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending" || user.pending === `${userDetails.superior} Approval Pending` || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                <i class="bi bi-send"></i> Send
              </button>
            {:else if selectedOption === "Self Approve" && uniqid === user._id}
            {#if user.requestcategory === 'Analysis Request' && userDetails.team === "AP" || user.requestcategory === 'Analysis Request' && userDetails.team === "ISOT"}
                  <button on:click={() => submitedRecord(user,"Assign to CAT Ins","Approved by ADDL-SP/DSP")} type="button" class= "ml-2 btn btn-outline-success {user.pending === "Mail Sent"   || user.pending === "SP Approval Pending" || user.approval.includes('Approved')? 'hide' : ''}" >
                    <i class="bi bi-send"></i> Self Approve
                  </button>
                {:else if user.requestcategory === 'Analysis Request' && userDetails.team === "CAT" }
                <button on:click={() => submitedRecord(user,"--","Approved by ADDL-SP/DSP")} type="button" class= "ml-2 btn btn-outline-success {user.pending === "Mail Sent"   || user.pending === "SP Approval Pending" || user.pending === "--"? 'hide' : ''}" >
                  <i class="bi bi-send"></i> Self Approve
                </button>
                {:else}
                <button on:click={() => submitedRecord(user,"Mail Under Process","Approved by ADDL-SP/DSP")} type="button" class= "ml-2 btn btn-outline-success  {user.pending === "SP Approval Pending"   || user.pending === "Mail Sent" || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                    <i class="bi bi-send"></i> Self Approve
                  </button>
                {/if}
            {:else}
            <button type="button" class="btn btn-outline-success {(user.requestcategory === 'Analysis Request' && userDetails.team === 'CAT') || user.pending === "SP ADMIN Approval Pending" || user.pending === 'Ticket_Closed' 
            || user.pending=== "Ins Approval Pending"|| user.pending === 'Assign to CAT Ins' || user.approval.includes('Assigned')  
            || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" ? 'hide' : ''}" disabled>Select</button>
            {/if}
            <button
          class="btn btn-outline-success dropdown-toggle { (user.requestcategory === 'Analysis Request' && userDetails.team === 'CAT') || user.pending === "SP ADMIN Approval Pending" || user.pending === 'Ticket_Closed' 
          || user.pending=== "Ins Approval Pending"|| user.pending === 'Assign to CAT Ins' || user.approval.includes('Assigned')   
          || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" ? 'hide' : ''}" type="button" data-bs-toggle="dropdown" aria-expanded="false">
            <span class="sr-only"></span>
          </button>
          <div class="dropdown-menu">
            <a class="dropdown-item" on:click={() => handleOptionSelect('Send',user._id)}>Send</a>
            <a class="dropdown-item" on:click={() => handleOptionSelect('Self Approve',user._id)}>Self Approve</a>
          </div>
        </div>
          {:else if userDetails.designation === "SP"}
                {#if user.requestcategory === 'Analysis Request' && userDetails.team === "AP" || user.requestcategory === 'Analysis Request' && userDetails.team === "ISOT"}
                  <button on:click={() => submitedRecord(user,"Assign to CAT Ins","Approved by SP")} type="button" class= "ml-2 mt-2 btn btn-outline-success {(user.requestcategory === 'Analysis Request' && userDetails.team === 'ADMIN') || user.pending=== "Ins Approval Pending" || user.pending === 'Ticket_Closed'   || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "Mail Sent" || user.pending === "SP Approval Pending" || user.approval.includes('Approved')? 'hide' : ''}" >
                    <i class="bi bi-send"></i> Self Approve
                  </button>
                {:else if user.requestcategory === 'Note' && userDetails.team === "CAT"}
                <button on:click={() => submitedRecord(user,"--","Note Approved by SP")} type="button" class= "ml-2 mt-2 btn btn-outline-success {(user.requestcategory === 'Analysis Request' && userDetails.team === 'ADMIN') || user.pending=== "Ins Approval Pending" || user.pending === 'Ticket_Closed'   || user.requestcategory === 'Analysis Request' || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "Mail Sent" || user.pending === "SP Approval Pending" || user.pending === "--"? 'hide' : ''}" >
                  <i class="bi bi-send"></i> Self Approve
                </button>
                
                {:else if user.requestcategory === 'Analysis Request' && userDetails.team === "CAT" }
                <button on:click={() => submitedRecord(user,"--","Approved by SP")} type="button" class= "ml-2 mt-2 btn btn-outline-success {(user.requestcategory === 'Analysis Request' && userDetails.team === 'ADMIN') ||user.pending=== "Ins Approval Pending" || user.pending === 'Ticket_Closed'   || user.requestcategory === 'Analysis Request' || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "Mail Sent" || user.pending === "SP Approval Pending" || user.pending === "--"? 'hide' : ''}" >
                  <i class="bi bi-send"></i> Self Approve
                </button>
                {:else}
                <button on:click={() => submitedRecord(user,"Mail Under Process","Approved by SP")} type="button" class= "ml-2 mt-2 btn btn-outline-success {(user.requestcategory === 'Analysis Request' && userDetails.team === 'ADMIN') ||user.pending=== "Ins Approval Pending" || user.pending === 'Ticket_Closed'   || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "Mail Sent" || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process"? 'hide' : ''}" >
                  <i class="bi bi-send"></i> Self Approve
                </button>
                {/if}
          {:else if userDetails.designation === "ADDLSP"}
          <div class="btn-group mt-2">
            {#if selectedOption === "Send" && uniqid === user._id}
            <button data-bs-toggle="tooltip" data-bs-placement="top" title='Send to SP' on:click={() => submitedRecord(user,`${userDetails.superior} Approval Pending`,"-")} type="button" class= "ml-2 btn btn-outline-success  {user.pending === `${userDetails.superior} Approval Pending` ||user.pending=== "Ins Approval Pending"   || user.pending === "Mail Sent" || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                <i class="bi bi-send"></i> Send
              </button>
            {:else if selectedOption === "Self Approve" && uniqid === user._id}
            {#if user.requestcategory === 'Analysis Request' && userDetails.team === "AP" || user.requestcategory === 'Analysis Request' && userDetails.team === "ISOT"}
                  <button on:click={() => submitedRecord(user,"Assign to CAT Ins","Approved by ADDLSP")} type="button" class= "ml-2 btn btn-outline-success {user.pending === "Mail Sent"   || user.pending === "SP Approval Pending" || user.approval.includes('Approved')? 'hide' : ''}" >
                    <i class="bi bi-send"></i> Self Approve
                  </button>
                {:else if user.requestcategory === 'Analysis Request' && userDetails.team === "CAT" }
                <button on:click={() => submitedRecord(user,"--","Approved by ADDLSP")} type="button" class= "ml-2 btn btn-outline-success {user.pending === "Mail Sent" || user.pending === "SP ADMIN Approval Pending"    || user.pending === "SP Approval Pending" || user.pending === "--"? 'hide' : ''}" >
                  <i class="bi bi-send"></i> Self Approve
                </button>
                {:else}
                <button on:click={() => submitedRecord(user,"Mail Under Process","Approved by ADDLSP")} type="button" class= "ml-2 btn btn-outline-success  {user.pending === "SP Approval Pending"   || user.pending === "Mail Sent" || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                    <i class="bi bi-send"></i> Self Approve
                  </button>
                {/if}
            {:else}
            <button type="button" class="btn btn-outline-success {(user.requestcategory === 'Analysis Request' && userDetails.team === 'CAT') || user.approval === 'Note Approved by SP' || user.pending=== "Ins Approval Pending" || user.approval.includes('Assigned') || user.pending.includes('Rejected')   || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" ? 'hide' : ''}" disabled>Select</button>
            {/if}
              <button
            class="btn btn-outline-success dropdown-toggle {(user.requestcategory === 'Analysis Request' && userDetails.team === 'CAT') || user.approval === 'Note Approved by SP' || user.pending=== "Ins Approval Pending"|| user.approval.includes('Assigned')   || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" ? 'hide' : ''}" type="button" data-bs-toggle="dropdown" aria-expanded="false">
              <span class="sr-only"></span>
            </button>
          <div class="dropdown-menu">
            <a class="dropdown-item" on:click={() => handleOptionSelect('Send',user._id)}>Send</a>
            <a class="dropdown-item" on:click={() => handleOptionSelect('Self Approve',user._id)}>Self Approve</a>
          </div>
        </div>
          {:else if userDetails.role === "Analyst" && userDetails.team === "AP" || userDetails.role === "Analyst" && userDetails.team === "ISOT"}
          <div class="btn-group mt-2">
            {#if selectedOption === "DSP" && uniqid === user._id}
            <button on:click={()=> fetch_officers('dsp')} data-bs-placement="top" title='Send to DSP' class= "ml-2 btn btn-outline-success {user.pending=== "Ins Approval Pending" 
                || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "Mail Sent" || user.pending === "SP Approval Pending" 
                || user.pending === "Mail Under Process" ? 'hide' : ''}" type="button" data-bs-toggle="modal" data-bs-target="#myModal4{user._id}">
                 <i class="bi bi-send"></i> DSP
                </button>
                <div class="modal fade" id="myModal4{user._id}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true" data-bs-backdrop="static">
                  <div class="modal-dialog" style="width: 30%;">
                    <div class="modal-content">
                      <div class="modal-header">
                      </div>
                      <div class="modal-body text-left"> 
                        <div class="container">
                          <div class="row">
                            <div class="col-12">
                              <div class="row">
                              <h4 class="text-wrap">Are you sure to Send this ticket to Other Superior?</h4>
                              <select bind:value = {insp} >
                              <option disabled selected value="">Select Other Ins</option>
                              {#each insplist as ins}
                              <option value={ins.officername}>{ins.officername}</option>
                              {/each}
                              </select>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="modal-footer">
                        <button type="button" class="btn btn-outline-success" data-bs-dismiss="modal" on:click={() => submitedRecord(user,"ADDL-SP/DSP Approval Pending","-")}>Yes</button>
                        <button type="button" class="btn btn-outline-primary" data-bs-dismiss="modal" on:click={()=> fetchTickets(currentPage)} aria-label="Close">No</button>
                      </div>
                    </div>
                  </div> 
                </div>
             {:else if selectedOption === "INSPR" && uniqid === user._id}
                <button on:click={()=> fetch_officers('ins')} data-bs-placement="top" title='Send to Ins' class= "ml-2 btn btn-outline-success {user.pending=== "Ins Approval Pending" 
                || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "Mail Sent" || user.pending === "SP Approval Pending" 
                || user.pending === "Mail Under Process" ? 'hide' : ''}" type="button" data-bs-toggle="modal" data-bs-target="#myModal4{user._id}">
                  <i class="bi bi-send"></i> INSPR
                </button>
                <div class="modal fade" id="myModal4{user._id}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true" data-bs-backdrop="static">
                  <div class="modal-dialog" style="width: 30%;">
                    <div class="modal-content">
                      <div class="modal-header">
                      </div>
                      <div class="modal-body text-left"> 
                        <div class="container">
                          <div class="row">
                            <div class="col-12">
                              <div class="row">
                              <h4 class="text-wrap">Are you sure to Send this ticket to Other Superior?</h4>
                              <select bind:value = {insp} >
                              <option disabled selected value="">Select Other Ins</option>
                              {#each insplist as ins}
                              <option value={ins.officername}>{ins.officername}</option>
                              {/each}
                              </select>
                            </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="modal-footer">
                        <button type="button" class="btn btn-outline-success" data-bs-dismiss="modal" on:click={() => submitedRecord(user,`Ins Approval Pending`,"-")}>Yes</button>
                        <button type="button" class="btn btn-outline-primary" data-bs-dismiss="modal" on:click={()=> fetchTickets(currentPage)} aria-label="Close">No</button>
                      </div>
                    </div>
                  </div> 
                </div>
                {:else if selectedOption === "SP" && uniqid === user._id}
                <button on:click={()=> fetch_officers('sp')} data-bs-placement="top" title='Send to Ins' class= "ml-2 btn btn-outline-success {user.pending=== "Ins Approval Pending" 
                || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "Mail Sent" || user.pending === "SP Approval Pending" 
                || user.pending === "Mail Under Process" ? 'hide' : ''}" type="button" data-bs-toggle="modal" data-bs-target="#myModal4{user._id}">
                  <i class="bi bi-send"></i> SP
                </button>
                <div class="modal fade" id="myModal4{user._id}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true" data-bs-backdrop="static">
                  <div class="modal-dialog" style="width: 30%;">
                    <div class="modal-content">
                      <div class="modal-header">
                      </div>
                      <div class="modal-body text-left"> 
                        <div class="container">
                          <div class="row">
                            <div class="col-12">
                              <div class="row">
                              <h4 class="text-wrap">Are you sure to Send this ticket to Other Superior?</h4>
                              <select bind:value = {insp}>
                              <option disabled selected value="">Select Other Ins</option>
                              {#each insplist as ins}
                              <option value={ins.officername}>{ins.officername}</option>
                              {/each}
                              </select>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="modal-footer">
                        <button type="button" class="btn btn-outline-success" data-bs-dismiss="modal" on:click={() => submitedRecord(user,`SP Approval Pending`,"-")}>Yes</button>
                        <button type="button" class="btn btn-outline-primary" data-bs-dismiss="modal" on:click={()=> fetchTickets(currentPage)} aria-label="Close">No</button>
                      </div>
                    </div>
                  </div> 
                </div>
                {:else if selectedOption === 'Self' && uniqid === user._id}
                {#if user.requestcategory === 'Analysis Request' && userDetails.team === "AP" || user.requestcategory === 'Analysis Request' && userDetails.team === "ISOT"}
                  <button on:click={() => submitedRecord(user,"Assign to CAT Ins","Approved by Analyst")} type="button" class= "ml-2 btn btn-outline-success {user.pending === "Mail Sent" || user.pending === "SP Approval Pending" || user.approval.includes('Approved')? 'hide' : ''}" >
                    <i class="bi bi-send"></i> Self Approve
                  </button>
                {:else}
                <button on:click={() => submitedRecord(user,"Mail Under Process","Approved by Analyst")} type="button" class= "ml-2 btn btn-outline-success  {user.pending === "SP Approval Pending" || user.pending === "Mail Sent" || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                    <i class="bi bi-send"></i> Self Approve
                  </button>
                {/if}
                {:else}
                <button data-bs-toggle="tooltip" data-bs-placement="top" title='Select options from Dropdown' type="button" class="btn btn-outline-success {user.pending=== `${userDetails.superior} Approval Pending` || user.pending === 'Ticket_Closed'|| user.pending === 'Assign to CAT Ins' || user.approval.includes('Assigned')
                || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending.includes('Rejected') || user.pending === "Mail Sent" || user.pending === "SP Approval Pending" 
                || user.pending === "Mail Under Process" ? 'hide' : ''}" disabled>Select</button>
                {/if}
            <button
            class="btn btn-outline-success dropdown-toggle {user.pending=== `${userDetails.superior} Approval Pending` || user.pending === 'Ticket_Closed'|| user.pending === 'Assign to CAT Ins' || user.approval.includes('Assigned')
            || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending.includes('Rejected') || user.pending === "Mail Sent" || user.pending === "SP Approval Pending" 
            || user.pending === "Mail Under Process" ? 'hide' : ''}" type="button" data-bs-toggle="dropdown" aria-expanded="false">
              <span class="sr-only"></span>
            </button>
            <div class="dropdown-menu">
              <a class="dropdown-item" on:click={() => handleOptionSelect("INSPR",user._id)}>Send to Ins</a>
              <a class="dropdown-item" on:click={() => handleOptionSelect('DSP',user._id)}>Send to DSP</a>
              <a class="dropdown-item" on:click={() => handleOptionSelect('SP',user._id)}>Send to SP</a>
              <a class="dropdown-item" on:click={() => handleOptionSelect('Self',user._id)}>Self Approve</a>
    
            </div>
          </div>
          {:else if userDetails.role === "Analyst" && userDetails.team === "CAT"}
          <div class="btn-group mt-2">
            {#if selectedOption === "Send to DSP" && uniqid === user._id}
            <button on:click={() => submitedRecord(user,"ADDL-SP/DSP Approval Pending","-")} type="button" class="ml-2 btn btn-outline-success {user.pending=== "Ins Approval Pending" 
              || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "Mail Sent"   || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                <i class="bi bi-send"></i> DSP
              </button>
            {:else if selectedOption === "Send" && uniqid === user._id}
            <button on:click={() => submitedRecord(user,"Ins Approval Pending","-")} type="button" class="ml-2  btn btn-outline-success {user.pending=== "Ins Approval Pending" 
              || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "Mail Sent"   || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                <i class="bi bi-send"></i> Send
              </button>
            {:else}
            <button type="button" class="btn btn-outline-success {user.pending=== "Ins Approval Pending" || user.approval === 'Note Approved by SP' || user.pending === 'Ticket_Closed' || user.pending=== "ADDL-SP/DSP Approval Pending" 
            || user.pending === "Mail Sent"  || user.pending.includes('Rejected')  || user.pending === "SP Approval Pending" 
            || user.pending === "Mail Under Process" ? 'hide' : ''}" disabled>Select</button>
            {/if}
            <button
              class="btn btn-outline-success dropdown-toggle {user.pending=== "Ins Approval Pending" || user.approval === 'Note Approved by SP' || user.pending === 'Ticket_Closed' || user.pending=== "ADDL-SP/DSP Approval Pending" 
              || user.pending === "Mail Sent"  || user.pending.includes('Rejected')  || user.pending === "SP Approval Pending" 
              || user.pending === "Mail Under Process" ? 'hide' : ''}" type="button" data-bs-toggle="dropdown" aria-expanded="false">
              <span class="sr-only"></span>
            </button>
            <div class="dropdown-menu">
              <a class="dropdown-item" on:click={() => handleOptionSelect('Select',user._id)}>Select</a>
              <a class="dropdown-item" on:click={() => handleOptionSelect('Send',user._id)}>Send to {userDetails.superior}</a>
              <a class="dropdown-item" on:click={() => handleOptionSelect('Send to DSP',user._id)}>Send to DSP</a>
            </div>
          </div>
          {:else if userDetails.role === "Mailer" && userDetails.team === "CAT"}
            <button on:click={() => submitedRecord(user,"Ins Approval Pending","-")} type="button" class="ml-2 mt-2 btn btn-outline-success {user.pending=== "Ins Approval Pending" 
              || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "Mail Sent" || user.pending === 'Ticket_Closed'   || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                <i class="bi bi-send"></i> Send to Ins
              </button>
          {:else if userDetails.role === "Logger" || userDetails.designation === "SI"}
                   <div class="btn-group mt-2">
                    {#if selectedOption === "Send to DSP" && uniqid === user._id}
                    <button on:click={() => submitedRecord(user,"ADDL-SP/DSP Approval Pending","-")} type="button" class= "ml-2 btn btn-outline-success {user.pending=== "Ins Approval Pending" 
                      || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending" || user.pending === 'Ticket_Closed'   || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                       Send to DSP
                      </button>
                      
                      {:else if selectedOption === "Send" && uniqid === user._id}
                      <button on:click={() => submitedRecord(user,`${userDetails.superior} Approval Pending`,"-")} type="button" class= "ml-2  btn btn-outline-success {user.pending=== `${userDetails.superior} Approval Pending` 
                      || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending"   || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                          Send
                        </button>
                      {:else}
                      <button type="button" class="btn btn-outline-success" disabled>Select</button>
                      {/if}
                      <button
                    class="btn btn-outline-success dropdown-toggle {user.pending=== "Ins Approval Pending" || user.pending === 'Ticket_Closed' || user.pending=== "ADDL-SP/DSP Approval Pending" 
                    || user.pending === "Mail Sent"   || user.pending === "SP Approval Pending" 
                    || user.pending === "Mail Under Process" ? 'hide' : ''}" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                      <span class="sr-only"></span>
                    </button>
                    <div class="dropdown-menu">
                      <a class="dropdown-item"  on:click={() => handleOptionSelect('Select',user._id)}>Select</a>
                      <a class="dropdown-item"  on:click={() => handleOptionSelect('Send',user._id)}>Send to {userDetails.superior}</a>
                      <a class="dropdown-item"  on:click={() => handleOptionSelect('Send to DSP',user._id)}>Send to DSP</a>
                    </div>
                  </div>
              {/if}
          {/if}
        </td>
        {#if user.priority === "Emergency"}
        <td style="color: red;font-weight:bold">{user.priority}</td>
        {:else}
        <td style="color: green;font-weight:bold">{user.priority}</td>
        {/if}
        <td>{user.date}</td>
        <td>
          {user.token}
      </td>
      <td class="{user.approval.includes('Approved') || user.approval.includes('Assigned') || user.approval === 'Data_Received' ? "Success" : "Rejected"}" >
        {user.approval}
      </td>
      <td class={user.pending.includes("Mail") ? "Rejected" : "Rejected"} >

        {#if user.pending === 'Mail Under Process' && (user.subtypes === 'Phone' || user.requesttype === 'CDR')}
        {user.pending} ({user.res_len}/{user.total_len})
        {:else if user.pending === 'Mail Under Process' && (user.subtypes === 'IMEI' || user.requesttype === 'IMEI CDR')}
        {user.pending} ({user.newno_len}/{user.total_len})
        {:else}
        {user.pending}
        {/if}
      </td>
      <td>
        {user.requestcategory}
      </td>
      {#if user.requestcategory === 'Data Request'}
      <td class="td">{user.requesttype} - {user.subtypes}</td>
      {:else if user.requestcategory === 'Analysis Request'}
      <td class="td">{user.requesttypes} - {user.subtypes}</td>
      {:else}
      <td class="td">{user.requesttype}</td>
      {/if}
      <!-- Button trigger modal -->
    <button type="button" on:click={()=> collapse(user)} class="mycol btn btn-info" data-bs-toggle="modal" data-bs-target="#mymodal{user._id}">
      View
    </button>
    <div class="modal fade" id="mymodal{user._id}" aria-hidden="true" aria-labelledby="exampleModalToggleLabel" tabindex="-1">
      <div class="modal-dialog modal-fullscreen" style="max-width: 2174px;">
        <div class="modal-content">
          <div class="modal-header">
            <h3 class="modal-title" id="exampleModalToggleLabel">
              Ticket Details
            </h3>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
              <div class="d-flex" style="text-align: left;">
                <p style="margin-left: 25px;"><b>Request Category : </b>{user.requestcategory}</p>
                <p style="margin-left: 25px;"><b>Request Type : </b>{user.requesttype || user.requesttypes}</p>
                <p style="margin-left: 25px;"><b>Subtype : </b>{user.subtypes}</p>
                <p style="margin-left: 25px;"><b>Officer : </b>{result.officername}</p>
                <p style="margin-left: 25px;"><b>Assigned To Others : </b>{result.others}</p>

                </div>
                <div class="d-flex" style="text-align: left;">
                {#if user.requestcategory === "Data Request"}
                <p style="margin-left: 25px;"><b>Nickname :</b> {result.nickname}</p>
                {/if}
                <p style="margin-left: 25px;"><b>Reason For Obtaining :</b> {result.reason}</p>                      
                <p style="margin-left: 25px;"><b>Ref No :</b> {result.refno}</p>
                {#if result.hasOwnProperty('Comments')}
                <p style="margin-left: 25px;"><b>Comments :</b> {result.Comments}</p>
                {/if}
                {#if result.hasOwnProperty('assign_Officer')}
                <p style="margin-left: 25px;"><b>Assigned To :</b> {result.assign_Officer}</p>
                {/if}
                <p style="margin-left: 25px;"><b>Remarks :</b></p> <textarea readonly style="margin-left: 10px;"> {result.remarks}</textarea>
              </div>
              <div  class="d-flex" style="text-align: left;margin-top: 10px;">
              {#if userDetails.email === user.useremail}
                {#if result.raise_time && result.raise_time.length > 0 }
                  <p style="margin-left: 25px;"><b>Raise Date and Time :</b> {result.raise_time}</p>
                {/if}
                {#if result.hasOwnProperty('Analyst_Approval')}
                  <p style="margin-left: 25px;" class="text-wrap"><b>Analyst Approved on :</b> {result.Analyst_Approval}</p>
                {/if}
                {#if result.hasOwnProperty('SP_Approval')}
                  <p style="margin-left: 25px;" class="text-wrap"><b>SP Approved on :</b> {result.SP_Approval}</p>            
                {/if}
                {#if result.hasOwnProperty('DSP_Approval')}
                  <p style="margin-left: 25px;" class="text-wrap"><b>DSP Approved on :</b> {result.DSP_Approval}</p>       
                {/if}
                {#if result.hasOwnProperty('INSPR_Approval')}
                  <p style="margin-left: 25px;" class="text-wrap"><b>INS Approved on :</b> {result.INSPR_Approval}</p>
                {/if}
                {#if result.hasOwnProperty('DSP_Reject')}
                  <p style="margin-left: 25px;" class="text-wrap"><b>DSP Rejected on :</b> {result.DSP_Reject}</p>       
                {/if}
                {#if result.hasOwnProperty('SP_Reject')}
                  <p style="margin-left: 25px;" class="text-wrap"><b>SP Rejected on :</b> {result.SP_Reject}</p>       
                {/if}
                {#if result.hasOwnProperty('INS_Reject')}
                  <p style="margin-left: 25px;" class="text-wrap"><b>INS Rejected on :</b> {result.INS_Reject}</p>       
                {/if}
              {/if}
              </div>
            {#if result !== ''}
              {#if result.requestcategory === 'Analysis Request'}
                  {#if userDetails.designation === 'INSPR' && userDetails.team === 'CAT'}
                  <div style="margin-top: 20px;">
                    <div>
                    {#if result.team === "AP" || result.team === "ISOT" || result.team === "CAT"}
                    <select bind:value={result.assign_Officer} style="width:130px !important;height:38px;margin-bottom:5px">
                      <option disabled selected value = "">Assign Officer</option>
                      {#each userDetails.ALL as alladmin}
                        <option value={alladmin.officername}>{alladmin.officername}</option>
                      {/each}
                    </select>    
                    <button on:click={toggleData} class="btn btn-outline-dark {result.pending=== "ADDL-SP/DSP Approval Pending" || result.pending === "SP Approval Pending" || result.pending === '--'
                                    || user.pending=== "Rejected by CAT Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.approval === "Assigned by CAT SP" || result.Comments  ? 'disabled' : ''}">Add Comments</button>                              
                        <div class="btn-group">
                          {#if selected1 === "Send to DSP"}
                          <button on:click={() => asigntoCAT(result,'ADDL-SP/DSP Approval Pending',"Assigned by CAT Ins")} class="btn btn-outline-success {result.pending=== "ADDL-SP/DSP Approval Pending" || result.pending === "SP Approval Pending"
                            || result.pending=== "Rejected by Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.approval === "Assigned by CAT SP" ? 'disabled' : ''}">{selected1}</button>
                            {/if}
                            {#if selected1 === "Self Approve"}
                          <button on:click={() => asigntoCAT(result,'--',"Assigned by CAT Ins")} class="btn btn-outline-success {result.pending=== "--" || result.pending === "SP Approval Pending"
                            || result.pending=== "Rejected by Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.approval === "Assigned by CAT SP" ? 'disabled' : ''}">{selected1}</button>
                            {/if}
                            {#if selected1 === 'Select'}
                          <button type="button" class="btn btn-outline-success" disabled>{selected1}</button>
                          {/if}
                          <button
                          class="btn btn-outline-success dropdown-toggle {result.pending=== "ADDL-SP/DSP Approval Pending" || result.pending === "SP Approval Pending" || result.pending === '--'
                          || result.pending=== "Rejected by CAT Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.approval === "Assigned by CAT SP" ? 'disabled' : ''}" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <span class="sr-only"></span>
                          </button>
                          <div class="dropdown-menu">
                            <a class="dropdown-item" on:click={() => handleSelect('Send to DSP')}>Send to DSP</a>
                            <a class="dropdown-item" on:click={() => handleSelect('Self Approve')}>Self Approve</a>
                          </div>
                        </div>
                        {/if}
                        </div>
                        </div>
                        {/if}
                        {#if userDetails.designation === "DSP" && userDetails.team === "CAT" || userDetails.designation === "ADDL-SP/DSP" && userDetails.team === "CAT"}
                                         <div>
                                           <div>
                                             {#if result.team === "AP" || result.team === "ISOT" ||result.team === "CAT" }
                                             
                                             <select bind:value={result.assign_Officer} style="width:130px !important;height:38px">
                                               <option disabled selected value = "">Assign Officer</option>
                                               {#each userDetails.ALL as alladmin}
                                                 <option value={alladmin.officername}>{alladmin.officername}</option>
                                               {/each}
                                             </select>
                                             <button on:click={toggleData} class="btn btn-outline-dark {result.pending === "SP Approval Pending" || result.pending === "--" 
                                                || result.pending=== "Rejected by Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.pending === "Mail Under Process" || result.approval === "Assigned by CAT SP" ? 'disabled' : ''}">Add Comments</button>                      
                                             <div class="btn-group">
                                               {#if selected1 === "Send"}
                                               <button on:click={() => asigntoCAT(result, "SP Approval Pending","Assigned by CAT DSP")} class="btn btn-outline-success {result.pending === "SP Approval Pending" || result.pending === "Mail Under Process" 
                                                 || result.pending=== "Rejected by Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.pending === "Mail Under Process" || result.approval === "Assigned by CAT SP" ? 'disabled' : ''}">{selected1}</button>
                                                 {/if}
                                                 {#if selected1 === "Self Approve"}
                                               <button on:click={() => asigntoCAT(result,'--',"Assigned by CAT DSP")} class="btn btn-outline-success {result.pending === "SP Approval Pending" || result.pending === "--" 
                                                 || result.pending=== "Rejected by Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.pending === "Mail Under Process" || result.approval === "Assigned by CAT SP" ? 'disabled' : ''}">{selected1}</button>
                                                 {/if}
                                                 {#if selected1 === 'Select'}
                                           <button type="button" class="btn btn-outline-success" disabled>{selected1}</button>
                                           {/if}
                                               <button
                                               class="btn btn-outline-success dropdown-toggle {result.pending === "SP Approval Pending" || result.pending === "--" 
                                               || result.pending=== "Rejected by Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.pending === "Mail Under Process" || result.approval === "Assigned by CAT SP" ? 'disabled' : ''}"  type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                                 <span class="sr-only"></span>
                                               </button>
                                               <div class="dropdown-menu">
                                                 <a class="dropdown-item" on:click={() => handleSelect('Send')}>Send to SP</a>
                                                 <a class="dropdown-item" on:click={() => handleSelect('Self Approve')}>Self Approve</a>
                                                </div>
                                             </div>                                        
                                             <button on:click={() => asigntoCAT(result, "Rejected by DSP","-")} class="btn btn-outline-danger {result.pending === "SP Approval Pending" || result.pending === "--" 
                                              || result.pending=== "Rejected by Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.pending === "Mail Under Process" || result.approval === "Assigned by CAT SP" ? 'disabled' : ''}">Reject</button>
                                             {/if}
                                           </div>
                                         </div>
                                         <div>
                                         </div>
                        {/if}

                        {#if userDetails.designation === "SP" && userDetails.team === "CAT" || userDetails.designation === "SP" && userDetails.team === "ADMIN"}
                                      <div>
                                       <div>
                                        {#if result.team === "AP" || result.team === "ISOT" ||result.team === "CAT" ||result.team === "ADMIN" }                                    
                                        <select bind:value={result.assign_Officer} style="width:130px !important;height:38px">
                                          <option disabled selected value = "">Assign Officer</option>
                                          {#each userDetails.ALL as alladmin}
                                            <option value={alladmin.officername}>{alladmin.officername}</option>
                                          {/each}
                                        </select>
                                        <button on:click={toggleData} class="btn btn-outline-dark {result.pending === "--" || result.pending=== "Rejected by Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.pending === "Mail Under Process"? 'disabled' : ''}">Add Comments</button>                      
                                        <button on:click={() => asigntoCAT(result,"--","Assigned by CAT SP")} class="btn btn-outline-success {result.pending === "--" || result.pending=== "Rejected by Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.pending === "Mail Under Process"? 'disabled' : ''}">Approve</button>
                                        <button on:click={() => asigntoCAT(result,"Rejected by SP", "-")} class="btn btn-outline-danger {result.pending === "--" || result.pending=== "Rejected by Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.pending === "Mail Under Process"? 'disabled' : ''}">Reject</button>
                                        {/if}
                                      </div>
                                    </div>
                                    <div>
                                </div>
                        {/if}
                        {#if showData}
                        <div class="row mb-3">
                            <div class="col-sm-3">
                                <label for="inputPassword3" class="col-sm-3 col-form-label">Comments</label>
                            </div>
                            <div class="col-sm-9">
                                <textarea name="comments" placeholder="Add Comment" id="comments" row="3" style='width: 1052px; margin-left: -494px ' aria-label="With textarea" bind:value={comments}></textarea>
                            </div>
                        </div>                   
                        <div class="row mb-3 justify-content-center text-center">
                            <div class="col-12">
                            <button type="button" on:click={() => handleSubmits(result)}  class="btn btn-success">submit</button>
                        </div>
                        </div>                                    
                            {/if}
                    
              {/if}
            <div class="d-flex justify-content-start">  
              <button on:click={fetchDataAndDownloadExcel(user)} type="button" class ="btn btn-outline-success" style="border-radius: 10px;margin-bottom:10px">
                <i class="bi bi-cloud-arrow-down"></i>                   
            </button>
            </div>
            
              {#if user.requesttype === "SDR" && (user.subtypes === "SDR" || user.subtypes === "SDR HISTORY") || user.requesttype === 'Analysis Note'}
              <div class="col-auto scroll-table">
                  <table class="table table-bordered">
                    <thead class="table-dark" id="myhead">
                      <tr>
                        <th>Phone NO.</th> 
                        <th>MNP</th> 
                      </tr>
                    </thead>
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
                  <thead class="table-dark" id="myhead">
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
                  {/if}
                  </tr>
                  </thead>
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
                    {/if}
                  </tr>
                  {/each}
                </table>
              </div>
              {/if}
              {#if user.requestcategory === 'Analysis Request'}
              {#if (!user.requesttypes.includes('IMEI') && user.subtypes !== "IMEI") && (!user.requesttypes.includes('TOWER DATA'))}
              <div class="col-auto scroll-table">
                <table class="table table-bordered">
                  <thead class="table-dark" id="myhead">
                    <tr>
                      <th>Phone No.</th> 
                      <th>Provider</th>
                      <th>From Date</th>
                      <th>To Date</th>
                    </tr>
                  </thead>
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
                  <thead class="table-dark" id="myhead">
                    <tr>
                      <th>IMEI</th> 
                      <th>Provider</th>
                      <th>From Date</th>
                      <th>To Date</th>
                    </tr>
                  </thead>
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
                  <thead class="table-dark" id="myhead">
                  <tr>
                    <th>Phone No.</th> 
                    <th>CAF No.</th>
                    <th>MNP</th>
                  </tr>
                  </thead>
                  {#each result.newnumber as newno}
                  <tr>
                    <td>{newno.Phno}</td>
                    <td>{newno.CAF}</td>
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
              {#if user.requesttype === "CAF/CDR"}
              <div class="col-auto scroll-table">
                <table class="table table-bordered">
                  <thead class="table-dark" id="myhead">
                  <tr>
                    <th>Phone No./CAF No.</th> 
                    <th>From Date</th>
                    <th>To Date</th>
                  </tr>
                  </thead>
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
                    <thead class="table-dark" id="myhead">
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
                    </thead>
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
                    {#if newno.hasOwnProperty('status')}
                    <td class = "{newno.status === "Data_Received" ? "Success" : "Rejected"}">{newno.status}</td>  
                    {:else}
                    <td></td> 
                    {/if}                        
                    {/if}
                    </tr>
                    {/each}
                  </table>
                </div>
                {/if}
              {#if user.requesttype === "IPDR" && user.subtypes === "IPV6" || user.requesttype === "IPDR" && user.subtypes === "IPV4" || user.requesttype === "IPDR" && user.subtypes === ""}
              <div class="col-auto scroll-table">
                <table class="table table-bordered">
                  <thead class="table-dark" id="myhead">
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
                  </thead>
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
              {#if user.requesttype === "RH" && user.subtypes === "Phone" || user.requesttype === "POA" && user.subtypes === "Phone"}
              <div class="col-auto scroll-table">
                <table class="table table-bordered">
                  <thead class="table-dark" id="myhead">
                  <tr>                                
                    <th>Phone</th>
                    <th>NickName</th>                                                          
                      <th>From Date</th>
                      <th>To Date</th>
                  </tr>
                  </thead>
                  {#each result.newnumber as newno}
                  <tr>
                    {#if user.requesttype === "RH"}
                    <td>{newno.Phno}</td>
                    <td class = "text-wrap">{newno.Nickname}</td>
                    {:else if user.requesttype === "POA"}
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
              {#if user.requesttype === "RH" && user.subtypes === "Retailer/Dealer Details" || user.requesttype === "POA" && user.subtypes === "Retailer/Dealer Details"}
              <div class="col-auto scroll-table">
                <table class="table table-bordered">
                  <thead class="table-dark">
                    <tr>                                
                      <th>Dealer Details</th>
                      <th>Dealer Code</th>    
                      <th>Provider</th>                                                     
                        <th>From Date</th>
                        <th>To Date</th>
                    </tr>
                  </thead>
                  {#each result.newnumber as newno}
                  <tr>
                    {#if user.requesttype === "RH"}
                    <td>{newno.RH_Dealer}</td>
                    <td>{newno.RH_code}</td>
                    <td>{newno.ISP}</td>
                    {:else if user.requesttype === "POA"}
                    <td>{newno.POA_Dealer}</td>
                    <td>{newno.POA_code}</td>
                    <td>{newno.ISP}</td>
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
                  <thead class="table-dark" id="myhead">
                  <tr>
                    {#if user.subtypes === "CGI"}
                    <th>CGI ID</th>
                    <th>Provider</th>
                    <th>Status</th>
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
                  </thead>
                  {#each result.newnumber as newno}
                  <tr>
                    {#if user.subtypes === "CGI"}
                    <td>{newno.CGI}</td>
                    <td>{newno.ISP || ''}</td>
                    {#if newno.hasOwnProperty('status')}
                    <td class="{newno.status === "Data_Received" ? "Success" : "Rejected"}">{newno.status}</td>    
                    {:else}
                    <td></td>
                    {/if}      
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
              {:else if user.requestcategory === 'Analysis Request' && user.requesttypes.includes('TOWER DATA')}
              <div class="col-auto scroll-table">
                <table class="table table-dark table-bordered">
                  <thead class="table-dark" id="myhead">
                  <tr>
                    {#if user.subtypes === "CGI"}
                    <th>CGI</th>
                    <th>Provider</th>
                    
                    {:else if user.subtypes === "Phone"}
                    <th>Phone</th>
                    {:else if user.subtypes === "Area"}
                    <th>Area</th>
                    <th>Cell IDs</th>
                    {:else if user.subtypes === "Co-Ordinates"}
                    <th>Latitude</th>
                    <th>Longitude</th>
                    {:else if user.subtypes === "Tower Name"}
                    <th>Tower Name</th>
                    {/if}                               
                      <th>From Date</th>
                      <th>To Date</th>
                  </tr>
                  </thead>
                  {#each result.newnumber as newno}
                  <tr>
                    {#if user.subtypes === "CGI"}  
                    <td>{newno.CGI}</td>
                    <td>{newno.ISP || ''}</td>
              
                    {:else if user.subtypes === "Phone"}
                    <td>{newno.Phno}</td>
                    {:else if user.subtypes === "Area"}
                    <td>{newno.Area}</td>
                    {:else if user.subtypes === "Co-Ordinates"}
                    <td>{newno.Latitude}</td>
                    <td>{newno.Longitude}</td>
                    {/if}
                    <td>{newno.From_Date}</td>
                    <td>{newno.To_Date}</td>
                  </tr>
                  {/each}
                </table>
              </div>
              {/if}
              {/if}
            {#if user.requestcategory === 'Data Request' && (user.requesttype === 'CDR' || user.subtypes === 'Phone')}
              <button class="btn btn-outline-warning" style="margin-bottom: 20px;" on:click={()=> autoresult(user._id)}>Automation Details</button>
              <button class="btn btn-outline-primary" style="margin-bottom: 20px;" on:click={autoclose}>Close</button>
              {#if auto_result !== ''}
                  <div style="max-height: 455px; overflow: auto;">
                    <table class="table table-striped text-nowrap" id="mytable">
                      <thead style="background-color: black;" class="text-white sticky-header">
                        <tr>
                          <th>
                            <button class="bt btn btn-sm btn-danger bg-danger mt-1" data-id={auto_result._id} disabled={buttonDisabled} on:click={deleteSelectedRows}>
                              <i class="bt bi bi-trash"></i>
                            </button>
                          </th>
                          <th>Status</th>
                          <th style="width:50px">PhoneNumbers</th>
                          <th>MNP</th>
                          <th>Nickname</th>
                          <th>SDR</th>
                          <th>From Date</th>
                          <th>To Date</th>
                          <th>Truecaller</th>
                          <th>Remark</th>
                        </tr>
                      </thead>
                  {#if userDetails.role === "Analyst"}
                      {#each auto_result.result || [] as item }  
                      {#if item.SDR !== "" || item.SDR === "" }
                          <tr class="table-info {auto_result.pending === "Ins Approval Pending" || auto_result.pending === 'Ticket_Closed' || auto_result.pending=== "ADDL-SP/DSP Approval Pending" || auto_result.pending === "SP Approval Pending" || auto_result.pending === "Mail Under Process" 
                          || auto_result.pending=== "Rejected by Ins" || auto_result.pending === "Mail Sent" ||  auto_result.pending=== "Rejected by DSP" || auto_result.pending === "Rejected by SP" || auto_result.pending === "Mail Under Process" ? 'disabled' : ''}">
                                  <td>
                                    <input type="checkbox" class="cq checkbox-size {item.mailer_hold === "Hold by Mailer" || item.status === "Data_Received" || auto_result.pending === 'Ticket_Closed' ? "disabled" : ""}" style="text-align:center; vertical-align: middle;" on:change={handleCheckboxChange} id="checkbox_{user._id}" data-msisdn={item.MSISDN} />
                                  </td>
                                  <td class="td {item.mailer_hold === "Hold by Mailer" ? "disabled" : ""} {item.status === "Data_Received" ? "Success" : "Rejected"}" >
                                    {#if item.hasOwnProperty('mailer_hold')}
                                      {item.mailer_hold}
                                    {:else if item.hasOwnProperty('status')}
                                      {item.status}
                                    {:else}
                                      {auto_result.pending}
                                    {/if}
                                  </td>
                                  <td style="text-align:center; vertical-align: middle;">
                                    {item.MSISDN}
                                  </td>
                                  <td class="{item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">
                                    <input 
                                      type="text"
                                      class="mnp editable-cell border-0 "
                                      value={item.MNP}
                                      field=MNP
                                      on:input={e => updateField(user._id, item.MSISDN, 'MNP', e.target.value)}
                                    />
                                  </td>
                                  <td class="{item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">       
                                    <input 
                                      type="text"
                                      data-bs-toggle="tooltip" 
                                      data-bs-placement="top" 
                                      title={item.FetchedNickName}
                                      class="editable-cell border-0"
                                      value={item.FetchedNickName}
                                      field=FetchedNickName
                                      on:input={e => updateField(user._id, item.MSISDN, 'FetchedNickName', e.target.value)}
                                    />
                                  </td>
                                  <td class="{item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">
                                    <textarea
                                        data-bs-toggle="tooltip"
                                        data-bs-placement="top"
                                        title="{item.SDR}"
                                        class="editable-cell border-0 sdr"
                                        value="{item.SDR}"
                                        field="SDR"
                                        on:input="{e => updateField(user._id, item.MSISDN, 'SDR', e.target.value)}"
                                      ></textarea>
                                  </td>
                                  <td class="{item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">
                                    <input 
                                    type="text"
                                    class="mnp1 editable-cell border-0"
                                    value={item.From_Date || item.From_date}
                                    field=From_Date
                                    on:input={e => updateField(user._id, item.MSISDN, 'From_Date', e.target.value)}
                                  />
                                  </td>
                                  <td class="{item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">
                                    <input 
                                    type="text"
                                    class="mnp1 editable-cell border-0"
                                    value={item.To_Date || item.To_date}
                                    field=To_Date
                                    on:input={e => updateField(user._id, item.MSISDN, 'To_Date', e.target.value)}
                                  />
                                  </td>
                                  <td class="{item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">
                                    <input 
                                    type="text"
                                    class="mnp editable-cell border-0"
                                    value={item.Truecaller}
                                    field=Truecaller
                                    on:input={e => updateField(user._id, item.MSISDN, 'Truecaller', e.target.value)}
                                  />
                                  </td>
                                  <td class="{item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">             
                                    <input 
                                    type="text"
                                    class="mnp editable-cell border-0"
                                    value={item.Remarks}
                                    field=PoliticalVerification
                                    on:input={e => updateField(user._id, item.MSISDN, 'Remarks', e.target.value)}
                                  />
                                  </td>
                                  </tr>
                                  {/if}
                                  {/each}
                  {:else}
                            {#each auto_result.result || [] as item }  
                            {#if item.SDR !== "" || item.SDR === "" }
                            <tr class="table-info ">
                                    <td>
                                      <input type="checkbox" class="cq checkbox-size {item.mailer_hold === "Hold by Mailer" || item.status === "Data_Received" || auto_result.pending === 'Ticket_Closed' ? "disabled" : ""}"  style="text-align:center; vertical-align: middle;" on:change={handleCheckboxChange} id="checkbox_{user._id}" data-msisdn={item.MSISDN} />
                                    </td>
                                    <td class="td {item.mailer_hold === "Hold by Mailer" ? "disabled" : ""} {item.status === "Data_Received" ? "Success" : "Rejected"}" >
                                      {#if item.hasOwnProperty('mailer_hold')}
                                        {item.mailer_hold}
                                      {:else if item.hasOwnProperty('status')}
                                        {item.status}
                                      {:else}
                                        {auto_result.pending}
                                      {/if}
                                    </td>
                                        <td class="td {item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">
                                          {item.MSISDN}
                                        </td>
                                        <td class="td {item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">
                                            {item.MNP}
                                        </td>
                                        <td class="td {item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">
                                          <div class="divScroll" data-bs-toggle="tooltip" 
                                          data-bs-placement="top" 
                                          title='{item.FetchedNickName}'>
                                          {item.FetchedNickName}
                                          </div>     
                                      </td>
                                        <td class="mnp {item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">
                                        <textarea data-bs-toggle="tooltip" 
                                        style="width: 582px;height: 76px; text-align:left"
                                        data-bs-placement="top" 
                                        title='{item.SDR}'>
                                          {item.SDR}
                                        </textarea>                     
                                        </td>
                                        <td class="td mnp1 {item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">
                                          {item.From_date || item.From_Date}
                                        </td>
                                        <td class="td mnp1 {item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">
                                        {item.To_date || item.To_Date}
                                        </td>
                                        <td class="td {item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">
                                          {item.Truecaller}
                                        </td>
                                        <td class="td {item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">                  
                                          {item.Remarks}     
                                        </td>
                                        </tr>
                              {/if}
                              {/each}
                  {/if}
                    </table>
                  </div>
              {/if}
            {/if}
          </div>
        </div>
      </div>
    </div>
  </tr>
  {/each}
  </table>
    
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
  </div>
  {:else}
  <p class="d-flex justify-content-center mt-5 no-data">NO DATA</p>
  {/if}  
      </div>
      <!-- Analysis Request Tab content -->
      <div class="tab-pane fade" id="analysis-request" role="tabpanel" aria-labelledby="analysis-request-tab">
        <div class="search_bar">
          {#if userDetails.role !== "Logger" || userDetails.designation !== "SI" || userDetails.role === "Analyst"}
          <h2 style="font-size: 2rem;"></h2>
          {/if}
          <div class="search btn-group" style='margin-bottom: 10px;margin-right: 138px'>
            <input type="search" style="border-radius: 40px 0 0 40px" bind:value={searchValue2} placeholder="Search Data">
            <button
            class="btn btn-outline-primary" style="border-radius: 0 40px 40px 0;cursor: pointer;height: 40px;width: 64px;margin: 0;" type="button" on:click={() => search2('Others_Tickets')}>
            <i class="bi bi-search"></i>
            </button>
          </div>
        </div>
{#if cases2.length > 0}
          <div class="table-responsive text-nowrap scroll-table1">
          <table class="table table-striped table-hover" id="mytb">
            <thead class="table-dark" id="myhead">
              <tr>
              <th></th>
              <th>
                <button style="font-weight: bold;" class="btn btn-dark dropdown-toggle" type="button" id="statusFilterDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                  Priority
                </button>
                <ul class="dropdown-menu" aria-labelledby="statusFilterDropdown">
                  <li>
                    <a class="dropdown-item" href="#" on:click={() => fetchTickets1(currentPage)}>All</a>
                  </li>
                  {#each prio as status}
                  <li>
                    <a class="dropdown-item" href="#" on:click={() => header_filter2(status,'priority')}>{status}</a>
                  </li>
                  {/each}
                </ul>    
              </th>
              <th>
                <button style="font-weight: bold;" class="btn btn-dark dropdown-toggle" type="button" id="statusFilterDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                    Date
                </button>
                <ul class="dropdown-menu" aria-labelledby="statusFilterDropdown">
                  <li>
                    <a class="dropdown-item" href="#" on:click={clear_range1}>Clear</a>
                  </li>
                  <li>
                    <input class="border-0" use:flatpickr={{mode:'range', dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today', onChange:(selectedDates) => {startDate = selectedDates[0];endDate = selectedDates[1];}}} 
                      placeholder="Select Range" id="dateRangePicker11" on:input={Date_range1(startDate,endDate)}>
                  </li>
                </ul>
              </th>
              <th>TicketID</th>
              <th>
                <button style="font-weight: bold;" on:click={()=> fetch_status2('approval')}  class="btn btn-dark dropdown-toggle" type="button" id="statusFilterDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                  Approval Status
                </button>
                <ul class="dropdown-menu" aria-labelledby="statusFilterDropdown">
                  <li>
                    <a class="dropdown-item" href="#" on:click={() => fetchTickets1(currentPage)}>All</a>
                  </li>
                  {#each data2 as status}
                  <li>
                    <a class="dropdown-item" href="#" on:click={() => header_filter2(status,'approval')}>{status}</a>
                  </li>
                  {/each}
                </ul> 
              </th>
              <th>
                <button style="font-weight: bold;" on:click={()=> fetch_status2('pending')} class="btn btn-dark dropdown-toggle" type="button" id="statusFilterDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                  Pending Status
                </button>
                <ul class="dropdown-menu" aria-labelledby="statusFilterDropdown">
                  <li>
                    <a class="dropdown-item" href="#" on:click={() => fetchTickets1(currentPage)}>All</a>
                  </li>
                  {#each data2 as status}
                  <li>
                    <a class="dropdown-item" href="#" on:click={() => header_filter2(status,'pending')}>{status}</a>
                  </li>
                  {/each}
                </ul> 
              </th>
              <th>
                <button style="font-weight: bold;" on:click={()=> fetch_status2('category')} class="btn btn-dark dropdown-toggle" type="button" id="statusFilterDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                  Category
                </button>
                <ul class="dropdown-menu" aria-labelledby="statusFilterDropdown">
                  <li>
                    <a class="dropdown-item" href="#" on:click={() => fetchTickets1(currentPage)}>All</a>
                  </li>
                  {#each data2 as status}
                  <li>
                    <a class="dropdown-item" href="#" on:click={() => header_filter2(status,'category')}>{status}</a>
                  </li>
                  {/each}
                </ul> 
              </th>
              <th>
                <button style="font-weight: bold;" on:click={()=> fetch_status2('requesttype')} class="btn btn-dark dropdown-toggle" type="button" id="statusFilterDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                  Request Types - Subtypes
                </button>
                <ul class="dropdown-menu" aria-labelledby="statusFilterDropdown" style="max-height:250px;overflow: scroll;">
                  <li>
                    <a class="dropdown-item" href="#" on:click={() => fetchTickets1(currentPage)}>All</a>
                  </li>
                  {#each data2 as status}
                  <li>
                    <a class="dropdown-item" href="#" on:click={() => header_filter2(status,'requesttype')}>{status}</a>
                  </li>
                  {/each}
                </ul> 
              </th>
              <th>
                <button style="font-weight: bold;" on:click={()=> fetch_status2('officername')} class="btn btn-dark dropdown-toggle" type="button" id="statusFilterDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                  Officer
                </button>
                <ul class="dropdown-menu" aria-labelledby="statusFilterDropdown" style="max-height:300px;overflow: scroll;">
                  <li>
                    <a class="dropdown-item" href="#" on:click={() => fetchTickets1(currentPage)}>All</a>
                  </li>
                  {#each data2 as status}
                  <li>
                    <a class="dropdown-item" href="#" on:click={() => header_filter2(status,'officername')}>{status}</a>
                  </li>
                  {/each}
                </ul> 
              </th>
              <th>
                <button style="font-weight: bold;" on:click={()=> fetch_status2('edit')} class="btn btn-dark dropdown-toggle" type="button" id="statusFilterDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                  Edited?
                </button>
                <ul class="dropdown-menu" aria-labelledby="statusFilterDropdown">
                  <li>
                    <a class="dropdown-item" href="#" on:click={() => fetchTickets1(currentPage)}>All</a>
                  </li>
                  {#each data2 as status}
                  <li>
                    <a class="dropdown-item" href="#" on:click={() => header_filter2(status,'edit')}>{status}</a>
                  </li>
                  {/each}
                </ul> 
              </th>
              <th>Tickets Details</th>
              </tr>
            </thead>
      {#each cases2 as user}
           <tr>
            <td>

              {#if user.requestcategory !== "Data Request" && (userDetails.team === 'CAT' || userDetails.team === 'ADMIN')}
                    <button class="btn btn-link dropdown-toggle mt-2" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false"><i class="bi bi-three-dots-vertical"></i></button>
                    <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1" style="background-color: white;">
                      {#if userDetails.role === 'Analyst'}
                      <li>
                        <a class="dropdown-item" data-bs-toggle="tooltip" data-bs-placement="top" title='Convert Analysis to Data Request' on:click={()=> raise_new_data(user._id,'convert')}>
                          <i class="bi bi-arrow-up-right-square-fill"></i> Convert</a>
                        </li>
                        {/if}

                        {#if user.requesttypes.includes('CDR') || user.subtypes === 'Phone' || user.requestcategory === 'Note'}
                          <li>
                            <a class="dropdown-item" data-bs-toggle="tooltip" data-bs-placement="top" title='Fill Analysis Request Proforma' on:click={()=> raise_new_data(user._id,'proforma')}>
                            <i class="bi bi-file-text-fill"></i> Analysis Proforma</a>
                          </li>
                        {/if}
                    </ul>
              {/if}

          {#if userDetails.role === "Mailer"}
                <input
                type="checkbox"
                class="mycheck checkbox-size mt-2 ml-5"
                style="text-align: center; vertical-align: middle;"
                bind:group={selected_tickets}
                value={user._id}
              />
          {/if}
            { #if userDetails.role === "Analyst" && userDetails.team === "AP" || userDetails.role === "Analyst" && userDetails.team === "ISOT"}
          <div class="btn-group mt-2">
            {#if selectedOption === "DSP" && uniqid === user._id}
            {#if user.designation !== "DSP" && user.requestcategory === 'Data Request'}
            <button data-bs-placement="top" title='Send to DSP' class= "ml-2 btn btn-outline-success {user.pending=== "Ins Approval Pending" 
                || user.pending=== "ADDL-SP/DSP Approval Pending" ||user.pending==="Fetch_Pending_Data" || user.pending === "Mail Sent" || user.pending === "SP Approval Pending" 
                || user.pending === "Mail Under Process" ? 'hide' : ''}" type="button" data-bs-toggle="modal" data-bs-target="#myModal4{user._id}">
                  <i class="bi bi-send"></i> DSP
                </button>
                <div class="modal fade" id="myModal4{user._id}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true" data-bs-backdrop="static">
                  <div class="modal-dialog" style="width: 30%;">
                    <div class="modal-content">
                      <div class="modal-header">
                      </div>
                      <div class="modal-body text-left"> 
                        <div class="container">
                          <div class="row">
                            <div class="col-12">
                              <div class="row">
                              <h4 class="text-wrap">Are you sure to Send this ticket to Superior?</h4>
                              <select bind:value = {insp}>
                              <option selected value="">Select Other Ins</option>
                              {#each insplist as ins}
                              {#if ins.designation==="DSP" && ins.team === userDetails.team || ins.designation==="ADDL-SP/DSP" && ins.team === userDetails.team }
                              <option value={ins.officername}>{ins.officername}</option>
                              {/if}
                              {/each}
                              </select>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="modal-footer">
                        <button type="button" class="btn btn-outline-success" on:click={() => submitedRecord(user,"ADDL-SP/DSP Approval Pending","-")}>Yes</button>
                        <button type="button" class="btn btn-outline-primary" data-bs-dismiss="modal" on:click={()=> fetchTickets1(currentPage1)} aria-label="Close">No</button>
                      </div>
                    </div>
                  </div> 
                </div>
                {:else if user.designation === "DSP"} 
                        <button data-bs-toggle="tooltip" data-bs-placement="top" title='Send to SP' on:click={() => submitedRecord(user,"SP Approval Pending","-")} type="button" class= "ml-2 btn btn-outline-success {user.pending=== "Ins Approval Pending" || user.pending === "Mail Sent" || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                          <i class="bi bi-send"></i> SP
                    </button>
            {/if}
             {:else if selectedOption === "INSPR" && uniqid === user._id}
                <button data-bs-placement="top" title='Send to Ins' class= "ml-2 btn btn-outline-success {user.pending=== "Ins Approval Pending" 
                || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "Mail Sent" || user.pending === "SP Approval Pending" 
                || user.pending === "Mail Under Process" ? 'hide' : ''}" type="button" data-bs-toggle="modal" data-bs-target="#myModal4{user._id}">
                  <i class="bi bi-send"></i> INSPR
                </button>
                <div class="modal fade" id="myModal4{user._id}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true" data-bs-backdrop="static">
                  <div class="modal-dialog" style="width: 30%;">
                    <div class="modal-content">
                      <div class="modal-header">
                      </div>
                      <div class="modal-body text-left"> 
                        <div class="container">
                          <div class="row">
                            <div class="col-12">
                              <div class="row">
                              <h4 class="text-wrap">Are you sure to Send this ticket to Superior?</h4>
                              <select bind:value = {insp}>
                              <option selected value="">Select Other Ins</option>
                              {#each insplist as ins}
                              {#if ins.designation==="INSPR" && ins.team === userDetails.team}
                              <option value={ins.officername}>{ins.officername}</option>
                              {/if}
                              {/each}
                              </select>
                              </div>    
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="modal-footer">
                        <button type="button" class="btn btn-outline-success" on:click={() => submitedRecord(user,`Ins Approval Pending`,"-")}>Yes</button>
                        <button type="button" class="btn btn-outline-primary" data-bs-dismiss="modal" on:click={()=> fetchTickets1(currentPage1)} aria-label="Close">No</button>
                      </div>
                    </div>
                  </div> 
                </div>
                {:else}
                <button data-bs-toggle="tooltip" data-bs-placement="top" title='Select options from Dropdown' type="button" class="btn btn-outline-success {user.pending=== "Ins Approval Pending" || user.pending === 'Ticket_Closed' || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "Mail Sent" || user.pending === "SP Approval Pending" || user.pending === `${user.superior} Approval Pending`
                || user.pending === "Mail Under Process" || user.pending.includes('Assign') || user.pending=== "Rejected by ADDL-SP/DSP" || user.pending=== "Rejected by DSP" || user.pending === "Rejected by SP" || user.approval.includes('Assigned') ? 'hide' : ''}" disabled>Select</button>
                {/if}
            <button
            class="btn btn-outline-success dropdown-toggle {user.pending=== "Ins Approval Pending" || user.pending=== "Rejected by ADDL-SP/DSP" || user.pending=== "Rejected by DSP" || user.pending === "Rejected by SP" || user.pending === 'Ticket_Closed' || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "Mail Sent" || user.pending === "SP Approval Pending" || user.pending === `${user.superior} Approval Pending`
            || user.pending === "Mail Under Process" || user.pending.includes('Assign') || user.approval.includes('Assigned') ? 'hide' : ''}" type="button" data-bs-toggle="dropdown" aria-expanded="false">
              <span class="sr-only"></span>
            </button>
            <div class="dropdown-menu">
              <a class="dropdown-item" on:click={() => handleOptionSelect("Select",user._id)}>Select</a>
              <a class="dropdown-item" on:click={() => handleOptionSelect("INSPR",user._id)}>Send to Ins</a>
              <a class="dropdown-item" on:click={() => handleOptionSelect('DSP',user._id)}>Send to DSP</a>
            </div>
          </div>
        
          {:else if userDetails.role === "Analyst" && userDetails.team === "CAT"}
            {#if user.pending === 'Report Generated'}
              <div class="btn-group mt-2">
                {#if selectedOption === "Send to DSP" && uniqid === user._id}
                <button on:click={() => submitedRecord(user,"ADDL-SP/DSP Approval Pending","-")} type="button" class="ml-2 btn btn-outline-success {user.pending=== `${userDetails.superior} Approval Pending`
                  || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "Mail Sent"   || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                    <i class="bi bi-send"></i> DSP
                  </button>
                {:else if selectedOption === "Send" && uniqid === user._id}
                <button on:click={() => submitedRecord(user,`${userDetails.superior} Approval Pending`,"-")} type="button" class="ml-2  btn btn-outline-success {user.pending=== `${userDetails.superior} Approval Pending` 
                  || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "Mail Sent"   || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                    <i class="bi bi-send"></i> Send
                  </button>
                
                  {:else if selectedOption === "Send to SP" && uniqid === user._id}
                  <button on:click={() => submitedRecord(user,`SP Approval Pending`,"-")} type="button" class="ml-2  btn btn-outline-success {user.pending=== `${userDetails.superior} Approval Pending` 
                    || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "Mail Sent"   || user.pending=== "Rejected by ADDL-SP/DSP" || user.pending=== "Rejected by DSP" || user.pending === "Rejected by SP" || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                      <i class="bi bi-send"></i> Send
                    </button>
                {:else}
                <button type="button" class="btn btn-outline-success {user.pending=== "Ins Approval Pending" || user.pending === 'Ticket_Closed' || user.pending=== "ADDL-SP/DSP Approval Pending" 
                || user.pending === "Mail Sent"  || user.pending=== "Rejected by ADDL-SP/DSP" || user.pending=== "Rejected by DSP" || user.pending === "Rejected by SP"  || user.pending === "SP Approval Pending" 
                || user.pending === "Mail Under Process" ? 'hide' : ''}" disabled>Select</button>
                {/if}
                <button
                  class="btn btn-outline-success dropdown-toggle {user.pending=== "Ins Approval Pending" || user.pending === 'Ticket_Closed' || user.pending=== "ADDL-SP/DSP Approval Pending" 
                  || user.pending === "Mail Sent"   || user.pending === "SP Approval Pending" || user.pending=== "Rejected by ADDL-SP/DSP" || user.pending=== "Rejected by DSP" || user.pending === "Rejected by SP"
                  || user.pending === "Mail Under Process" ? 'hide' : ''}" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                  <span class="sr-only"></span>
                </button>
                <div class="dropdown-menu">
                  <a class="dropdown-item" on:click={() => handleOptionSelect('Select',user._id)}>Select</a>
                  <a class="dropdown-item" on:click={() => handleOptionSelect('Send',user._id)}>Send to {userDetails.superior}</a>
                  <a class="dropdown-item" on:click={() => handleOptionSelect('Send to DSP',user._id)}>Send to DSP</a>
                  <a class="dropdown-item" on:click={() => handleOptionSelect('Send to SP',user._id)}>Send to SP</a>
                </div>
              </div>
          {/if}
        {/if}

        {#if userDetails.designation === "INSPR" && userDetails.role !== "Analyst"}
          <div class="btn-group">
            {#if selectedOption === "Send to DSP" && uniqid === user._id}
            {#if userDetails.team === "CAT"}
                  {#if user.token.includes("_CO") && user.team === "AP" || user.token.includes("_CO") && user.team === "ISOT"}
                  <button data-bs-toggle="tooltip" data-bs-placement="top" title='Send to DSP' on:click={() => submitedRecord(user,"ADDL-SP/DSP Approval Pending","Approved by CAT Ins")} type="button" class= "ml-2 btn btn-outline-success {user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process"
                    || user.pending=== "Rejected by Ins" || user.pending === "Mail Sent" || user.pending=== "Rejected by ADDL-SP/DSP" || user.pending=== "Rejected by DSP" || user.pending === "Rejected by SP" || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                      Send
                    </button>
                    {:else}
                    <button data-bs-toggle="tooltip" data-bs-placement="top" title='Send to DSP' on:click={() => submitedRecord(user,"ADDL-SP/DSP Approval Pending","Approved by Ins")} type="button" class= "ml-2 btn btn-outline-success {user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process"
                    || user.pending=== "Rejected by Ins" || user.pending === "Mail Sent" || user.pending=== "Rejected by ADDL-SP/DSP" || user.pending=== "Rejected by DSP" || user.pending === "Rejected by SP" || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                      Send
                    </button>
                    {/if}
            {:else}
            <button data-bs-toggle="tooltip" data-bs-placement="top" title='Send to DSP' on:click={() => submitedRecord(user,"ADDL-SP/DSP Approval Pending","Approved by Ins")} type="button" class= "ml-2 btn btn-outline-success {user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process"
              || user.pending=== "Rejected by Ins" || user.pending === "Mail Sent" || user.pending=== "Rejected by ADDL-SP/DSP" || user.pending=== "Rejected by DSP" || user.pending === "Rejected by SP" || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                Send
              </button>
            {/if}          
              {:else if selectedOption === "Self Approve" && uniqid === user._id} 
                    {#if user.requestcategory === 'Analysis Request' && userDetails.team === "AP" || user.requestcategory === 'Analysis Request' && userDetails.team === "ISOT"}
                    <button on:click={() => submitedRecord(user,"Assign to CAT Ins","Approved by Ins")} type="button" class= "ml-2 btn btn-outline-success {user.pending === "Mail Sent" || user.pending === "SP Approval Pending"? 'hide' : ''}" >
                    <i class="bi bi-send"></i> Approve
                    </button>
                    {:else if user.requestcategory === 'Analysis Request' && userDetails.team === "CAT" }
                    <button on:click={() => submitedRecord(user,"--","Approved by Ins")} type="button" class= "ml-2 btn btn-outline-success {user.pending === "Mail Sent" || user.pending === "SP Approval Pending" || user.pending === "--"? 'hide' : ''}" >
                    <i class="bi bi-send"></i> Approve
                    </button>                
                    {:else if userDetails.team === "CAT" && user.requestcategory === 'Data Request'}
                              {#if user.token.includes("_CO") && user.team === "AP" || user.token.includes("_CO") && user.team === "ISOT"}
                              <button data-bs-toggle="tooltip" data-bs-placement="top" title='Self Approve' on:click={() => submitedRecord(user,"Mail Under Process","Approved by CAT Ins")} type="button" class= "ml-2 btn btn-outline-success {user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending" 
                              || user.pending === "Mail Under Process" || user.pending === `${user.superior} Approval Pending`
                                || user.pending=== "Rejected by Ins" || user.pending === "Mail Sent" || user.pending=== "Rejected by ADDL-SP/DSP" || user.pending=== "Rejected by DSP" || user.pending === "Rejected by SP" || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                                  Self
                                </button>
                                {:else}
                                <button data-bs-toggle="tooltip" data-bs-placement="top" title='Self Approve' on:click={() => submitedRecord(user,"Mail Under Process","Approved by Ins")} type="button" class= "ml-2 btn btn-outline-success {user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" 
                                  || user.pending=== "Rejected by Ins" || user.pending === "Mail Sent" || user.pending=== "Rejected by ADDL-SP/DSP" || user.pending=== "Rejected by DSP" || user.pending === "Rejected by SP" || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                                  Self
                                  </button>
                              {/if}
                    {:else}
                      <button data-bs-toggle="tooltip" data-bs-placement="top" title='Self Approve' on:click={() => submitedRecord(user,"Mail Under Process","Approved by Ins")} type="button" class= "ml-2 btn btn-outline-success {user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" 
                        || user.pending=== "Rejected by Ins" || user.pending === "Mail Sent" || user.pending=== "Rejected by ADDL-SP/DSP" || user.pending=== "Rejected by DSP" || user.pending === "Rejected by SP" || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                        Self
                        </button>
                    {/if}
              {:else if selectedOption === "Reject" && uniqid === user._id}
                <button data-bs-toggle="tooltip" data-bs-placement="top" title='Reject' on:click={() => submitedRecord(user,"Rejected by Ins","-")} type="button" class= "ml-2 btn btn-outline-danger {user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" 
                  || user.pending=== "Rejected by Ins" || user.pending === "Mail Sent" || user.pending=== "Rejected by ADDL-SP/DSP" || user.pending=== "Rejected by DSP" || user.pending === "Rejected by SP" || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                    Reject
                  </button>
              {:else}        
              <button type="button" class="btn btn-outline-success {(user.requestcategory === 'Analysis Request' && userDetails.team === 'CAT') || user.pending === "Mail Sent" || user.pending=== "Rejected by Ins" || user.pending=== "Rejected by DSP" || user.pending === "Rejected by SP" || user.pending === 'Ticket_Closed' || user.pending === "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" || user.pending.includes('Assign') 
              || user.approval.includes('Assigned') || user.pending.includes('Rejected') ?  'hide' : ''}" disabled>Select</button>
              {/if}         
              <button
            class=" btn btn-outline-success dropdown-toggle {(user.requestcategory === 'Analysis Request' && userDetails.team === 'CAT') || user.pending === "Mail Sent" || user.pending=== "Rejected by Ins" || user.pending=== "Rejected by DSP"|| user.pending=== "Rejected by ADDL-SP/DSP" || user.pending === "Rejected by SP" || user.pending === 'Ticket_Closed' || user.pending === "ADDL-SP/DSP Approval Pending" || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" || user.pending.includes('Assign') 
            || user.approval.includes('Assigned') || user.pending.includes('Rejected') ?  'hide' : ''}" type="button" data-bs-toggle="dropdown" aria-expanded="false">
              <span class="sr-only"></span>
            </button>
            <div class="dropdown-menu">
              {#if user.requestcategory === 'Data Request'}
              <a class="dropdown-item" on:click={() => handleOptionSelect('Self Approve', user._id)}>Self Approve</a>
              {/if}
              <a class="dropdown-item" on:click={() => handleOptionSelect('Send to DSP',user._id)}>Send to {userDetails.superior}</a>
              <a class="dropdown-item" on:click={() => handleOptionSelect('Reject',user._id)}>Reject</a>
            </div>
          </div>
          {:else if userDetails.designation === "DSP" || userDetails.designation === "ADDL-SP/DSP"}
          <!-- {#if userDetails.designation === "ADDL-SP/DSP"} -->
          <div class="btn-group">
              {#if selectedOption === "Self Approve" && uniqid === user._id}
    
                  {#if user.requestcategory === 'Analysis Request' && userDetails.team === "AP" || user.requestcategory === 'Analysis Request' && userDetails.team === "ISOT"}
                    <button on:click={() => submitedRecord(user,"Assign to CAT Ins","Approved by ADDL-SP/DSP")} type="button" class= "ml-2 btn btn-outline-success {user.pending.includes("Assign") ||user.pending === "Mail Sent" || user.pending === "SP Approval Pending"? 'hide' : ''}" >
                    <i class="bi bi-send"></i> Approve
                    </button>

                    {:else if user.requestcategory === 'Analysis Request' && user.proforma_data.length > 0}
                    <button on:click={() => submitedRecord(user,"-","Report Approved by ADDL-SP/DSP")} type="button" class= "ml-2 btn btn-outline-success {user.pending === "Mail Sent"|| user.pending === "--" || user.pending === "-"? 'hide' : ''}" >
                      <i class="bi bi-send"></i> Approve
                    </button>
                  {:else if user.requestcategory === 'Analysis Request' && userDetails.team === "CAT" }
                    <button on:click={() => submitedRecord(user,"--","Approved by ADDL-SP/DSP")} type="button" class= "ml-2 btn btn-outline-success {user.pending === "Mail Sent" || user.pending === "SP Approval Pending" || user.pending === "--"? 'hide' : ''}" >
                    <i class="bi bi-send"></i> Approve
                    </button>
    
                  {:else if user.token.includes("_CO") && userDetails.team === "AP" || user.token.includes("_CO") && userDetails.team === "ISOT"}
                      <button on:click={() => submitedRecord(user,"Annexe Send to CAT INS","Approved by ADDL-SP/DSP")} type="button" class= "ml-2 btn btn-outline-success {user.pending === "SP Approval Pending"|| user.pending === "Annexe Send to CAT INS" || user.pending === "Mail Sent" || user.pending === "Mail Under Process" 
                      || user.pending=== "Rejected by Ins" || user.pending=== "Rejected by DSP" || user.pending=== "Rejected by ADDL-SP/DSP" || user.pending === "Rejected by SP" || user.pending === "Mail Under Process"? 'hide' : ''}" >
                      Approve
                      </button>
                  {:else if userDetails.team === "CAT" && user.token.includes("_CO") && user.team === "AP" || userDetails.team === "CAT" && user.token.includes("_CO") && user.team === "ISOT"}
                      <button on:click={() => submitedRecord(user,"Mail Under Process","Approved by CAT DSP")} type="button" class= "ml-2 btn btn-outline-success {user.pending === "SP Approval Pending"|| user.pending === "Annexe Send to CAT INS" || user.pending === "Mail Sent" || user.pending === "Mail Under Process" 
                      || user.pending=== "Rejected by Ins" || user.pending=== "Rejected by ADDL-SP/DSP" || user.pending === "Rejected by SP" || user.pending === "Mail Under Process"? 'hide' : ''}" >
                      Approve
                      </button>
                  {:else}
                      <button on:click={() => submitedRecord(user,"Mail Under Process","Approved by ADDL-SP/DSP")} type="button" class= "ml-2 btn btn-outline-success {user.pending === "Mail Sent" || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process"? 'hide' : ''}" >
                      <i class="bi bi-send"></i> Approve
                      </button>
                  {/if}
              {:else if selectedOption === "Send to SP" && uniqid === user._id}
            <button data-bs-toggle="tooltip" data-bs-placement="top" title='Send to SP' on:click={() => submitedRecord(user,"SP Approval Pending","Approved by ADDL-SP/DSP")} type="button" class= "ml-2 btn btn-outline-success {user.pending === "SP Approval Pending"|| user.pending === "Annexe Send to CAT INS" || user.pending === "Mail Sent" || user.pending === "Mail Under Process" 
              || user.pending=== "Rejected by Ins" || user.pending=== "Rejected by ADDL-SP/DSP" || user.pending === "Rejected by SP" || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                Send
              </button>
              {:else if selectedOption === "Reject" && uniqid === user._id}
            <button data-bs-toggle="tooltip" data-bs-placement="top" title='Reject' on:click={() => submitedRecord(user,"Rejected by ADDL-SP/DSP","-")} type="button" class= "ml-2 btn btn-outline-danger {user.pending === "SP Approval Pending" || user.pending === "Mail Sent" || user.pending === "Mail Under Process" 
              || user.pending=== "Rejected by Ins" || user.pending.includes('Rejected') || user.pending=== "Rejected by ADDL-SP/DSP" || user.pending === "Annexe Send to CAT INS" || user.pending === '-' || user.pending === '--' || user.pending === "Rejected by SP" || user.pending === "Mail Under Process" ? 'hide' : ''}" >
                Reject
              </button>
            {:else}
            <button type="button" class="btn btn-outline-success {(user.requestcategory === 'Analysis Request' && userDetails.team === 'CAT') || user.pending.includes('Assign') || user.pending=== "Rejected by Ins" || user.pending === "Mail Sent" 
            || user.pending=== "Rejected by DSP" || user.pending=== "Rejected by ADDL-SP/DSP" || user.pending === "Rejected by SP" || user.pending === '-' || user.pending === '--'|| user.pending === 'Ticket_Closed' || user.approval.includes('Assigned') 
            || user.pending === "Mail Sent" || user.pending.includes('Rejected') || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" ?  'hide' : ''}" disabled>Select</button>
            {/if}              
            <button
          class="btn btn-outline-success dropdown-toggle {(user.requestcategory === 'Analysis Request' && userDetails.team === 'CAT') || user.pending.includes('Assign')  || user.pending=== "Rejected by Ins" || user.pending === "Mail Sent" || user.pending=== "Rejected by DSP" || user.pending=== "Rejected by ADDL-SP/DSP" || user.pending === "Rejected by SP" || user.pending === '-' || user.pending === '--'|| user.pending === 'Ticket_Closed' || user.approval.includes('Assigned') || user.pending === "Mail Sent" || user.pending === "SP Approval Pending" || user.pending === "Mail Under Process" ?  'hide' : ''}" type="button" data-bs-toggle="dropdown" aria-expanded="false">
            <span class="sr-only"></span>
          </button>
          <div class="dropdown-menu">
            <a class="dropdown-item" on:click={() => handleOptionSelect('Self Approve',user._id)}>Self Approve</a>
            <a class="dropdown-item" on:click={() => handleOptionSelect('Send to SP',user._id)}>Send to {userDetails.superior}</a>
            <a class="dropdown-item" on:click={() => handleOptionSelect('Reject',user._id)}>Reject</a>
          </div>
          </div>     
          {:else if userDetails.designation === "SP"}
          <div class="btn-group">
          {#if selectedOption === "Self Approve" && uniqid === user._id}      
          {#if user.requestcategory === 'Analysis Request' && userDetails.team === "AP" || user.requestcategory === 'Analysis Request' && userDetails.team === "ISOT"}
          <button on:click={() => submitedRecord(user,"Assign to CAT Ins","Approved by SP")} type="button" class= "ml-2 btn btn-outline-success {user.pending.includes("Assign")||user.pending === "Mail Sent"? 'hide' : ''}" >
            <i class="bi bi-send"></i> Approve
          </button>
        {:else if user.requestcategory === 'Analysis Request' && user.proforma_data.length > 0}
        <button on:click={() => submitedRecord(user,"-","Report Approved by SP")} type="button" class= "ml-2 btn btn-outline-success {user.pending === "Mail Sent"|| user.pending === "--" || user.pending === "-"? 'hide' : ''}" >
          <i class="bi bi-send"></i> Approve
        </button>
        {:else if user.requestcategory === 'Note' && user.team === "CAT"}
          <button on:click={() => submitedRecord(user,"-","Note Approved by SP")} type="button" class= "ml-2 btn btn-outline-success {user.pending=== "Ins Approval Pending" || user.pending === 'Ticket_Closed' || user.pending === "-"   || user.requestcategory === 'Analysis Request' || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending === "Mail Sent" || user.pending === "--"? 'hide' : ''}" >
            <i class="bi bi-send"></i> Approve
          </button>
        {:else if user.requestcategory === 'Analysis Request' && userDetails.team === "ADMIN" }
        <button on:click={() => submitedRecord(user,"--","Approved by SP")} type="button" class= "ml-2 btn btn-outline-success {user.pending === "Mail Sent"|| user.pending === "--"? 'hide' : ''}" >
          <i class="bi bi-send"></i> Approve
        </button>
          {:else if user.token.includes("_CO") && userDetails.team === "AP" || user.token.includes("_CO") && userDetails.team === "ISOT"}
          <button on:click={() => submitedRecord(user,"Annexe Send to CAT INS","Approved by SP")} type="button" class= "ml-2 btn btn-outline-success {user.pending === "Mail Under Process" || user.pending === "Annexe Send to CAT INS"
            || user.pending=== "Rejected by Ins" || user.pending=== "Rejected by DSP"|| user.pending=== "Rejected by ADDL-SP/DSP" || user.pending === "Rejected by SP" || user.pending === "Mail Under Process"? 'hide' : ''}" >
              Approve
            </button>
            {:else if userDetails.team === "CAT" && user.token.includes("_CO") && user.team === "AP" || userDetails.team === "CAT" && user.token.includes("_CO") && user.team === "ISOT"}
            <button on:click={() => submitedRecord(user,"Mail Under Process","Approved by CAT SP")} type="button" class= "ml-2 btn btn-outline-success {user.pending === "Mail Under Process" || user.pending === "Annexe Send to CAT INS"
              || user.pending=== "Rejected by Ins" || user.pending=== "Rejected by DSP"|| user.pending=== "Rejected by ADDL-SP/DSP" || user.pending === "Rejected by SP" || user.pending === "Mail Under Process"? 'hide' : ''}" >
                Approve
              </button>
              {:else}
              <button on:click={() => submitedRecord(user,"Mail Under Process","Approved by SP")} type="button" class= "ml-2 btn btn-outline-success {user.pending === "Mail Under Process" || user.pending === "Annexe Send to CAT INS"
                || user.pending=== "Rejected by Ins" || user.pending=== "Rejected by DSP" || user.pending=== "Rejected by ADDL-SP/DSP" || user.pending === "Rejected by SP" || user.pending === "Mail Under Process"? 'hide' : ''}" >
                   Approve
                </button>
            {/if}
            {:else if selectedOption === "Reject" && uniqid === user._id}
          <button data-bs-toggle="tooltip" data-bs-placement="top" title='Reject' on:click={() => submitedRecord(user,"Rejected by SP","-")} type="button" class= "ml-2 btn btn-outline-danger {user.pending === "Annexe Send to CAT INS" || user.pending === "Mail Under Process" 
            || user.pending=== "Rejected by Ins" || user.pending=== "Rejected by DSP" || user.pending=== "Rejected by ADDL-SP/DSP" || user.pending === "Rejected by SP" || user.pending === "Mail Under Process" ? 'hide' : ''}" >
              Reject
            </button>
          {:else}
          <button type="button" class="btn btn-outline-success {(user.requestcategory === 'Analysis Request' && userDetails.team === 'ADMIN') ||user.pending.includes('Assign') || user.pending=== "Fetch_Pending_Data" || user.pending=== "Approval Pending" || user.pending=== "--" || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending=== "Ins Approval Pending" || user.pending=== "Rejected by Ins" || user.pending === "Mail Sent" || user.pending=== "Rejected by DSP" || user.pending === "Rejected by SP" || user.pending === '-' || user.pending === 'Ticket_Closed' 
          ||user.pending==='Mail Under Process'|| user.pending.includes('Rejected') || user.pending=== "Rejected by ADDL-SP/DSP" || user.approval.includes('Assigned')?  'hide' : ''}" disabled>Select</button>
          {/if}
          <button
          class="btn btn-outline-success dropdown-toggle {(user.requestcategory === 'Analysis Request' && userDetails.team === 'ADMIN') ||user.pending.includes('Assign') || user.pending=== "Rejected by Ins" || user.pending=== "Fetch_Pending_Data" || user.pending=== "--" || user.pending=== "Approval Pending" || user.pending=== "ADDL-SP/DSP Approval Pending" || user.pending=== "Ins Approval Pending" || user.pending === "Mail Sent" || user.pending=== "Rejected by DSP" || user.pending === "Rejected by SP" || user.pending === '-' || user.pending === 'Ticket_Closed' 
          ||user.pending==='Mail Under Process'|| user.pending.includes('Rejected') || user.pending=== "Rejected by ADDL-SP/DSP" || user.approval.includes('Assigned')?  'hide' : ''}" type="button" data-bs-toggle="dropdown" aria-expanded="false">
          <span class="sr-only"></span>
          </button>
          <div class="dropdown-menu">
          <a class="dropdown-item" on:click={() => handleOptionSelect('Self Approve',user._id)}>Approve</a>
          <a class="dropdown-item" on:click={() => handleOptionSelect('Reject',user._id)}>Reject</a>
          </div>
          </div>
          {/if}
          </td>
          {#if user.priority === "Emergency"}
        <td class="mt-2" style="color: red;font-weight:bold">{user.priority}</td>
        {:else}
        <td style="color: green;font-weight:bold">{user.priority}</td>
        {/if}
          <td class="mt-2">{user.date}</td>
              <td>
                {user.token}
            </td>
            <td class={user.approval.includes('Approved') || user.approval.includes('Assigned') || user.approval === 'Data_Received' ? "Success" : "Rejected"} >
              {user.approval}
            </td>
            <td class={user.pending.includes("Mail") ? "Rejected" : "Rejected"} >

              {#if user.pending === 'Mail Under Process' && (user.subtypes === 'Phone' || user.requesttype === 'CDR')}
              {user.pending} ({user.res_len}/{user.total_len})
              {:else if user.pending === 'Mail Under Process' && (user.subtypes === 'IMEI' || user.requesttype === 'IMEI CDR')}
              {user.pending} ({user.newno_len}/{user.total_len})
              {:else}
              {user.pending}
              {/if}
            </td>
             <td class="td">{user.requestcategory}</td>
             {#if user.requestcategory === 'Data Request'}
             <td class="td">{user.requesttype} - {user.subtypes}</td>
             {:else if user.requestcategory === 'Analysis Request'}
             <td class="td">{user.requesttypes} - {user.subtypes}</td>
             {:else}
             <td class="td">{user.requesttype}</td>
             {/if}
             <td class="td">{user.officername}</td>
             <td class="td">
              {#if user.edit === "YES"}
              <mark class="mark1">
                {user.edit}
              </mark>
              {:else}
              <mark class="mark2">
                {user.edit}
              </mark>
              {/if}
            </td>
            <button type="button" on:click={()=> collapse(user)} class="mycol btn btn-info" data-bs-toggle="modal" data-bs-target="#mymodal{user._id}">
              View
            </button>
            <div class="modal fade" id="mymodal{user._id}" aria-hidden="true" aria-labelledby="exampleModalToggleLabel" tabindex="-1">
              <div class="modal-dialog modal-fullscreen" style="max-width: 2174px;">
                <div class="modal-content">
                  <div class="modal-header">
                    <h3 class="modal-title" id="exampleModalToggleLabel">
                      Ticket Details
                    </h3>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                  </div>
                  <div class="modal-body">
                    <div class="d-flex" style="text-align: left;">
                      <p style="margin-left: 25px;"><b>Request Category : </b>{user.requestcategory}</p>
                      <p style="margin-left: 25px;"><b>Request Type : </b>{user.requesttype || user.requesttypes}</p>
                      <p style="margin-left: 25px;"><b>Subtype : </b>{user.subtypes}</p>
                      <p style="margin-left: 25px;"><b>Officer : </b>{result.officername}</p>
                      <p style="margin-left: 25px;"><b>Assigned To Others : </b>{result.others}</p>

                      </div>
                      <div class="d-flex" style="text-align: left;">
                      {#if user.requestcategory === "Data Request"}
                      <p style="margin-left: 25px;"><b>Nickname :</b> {result.nickname}</p>
                      {/if}
                      <p style="margin-left: 25px;"><b>Reason For Obtaining :</b> {result.reason}</p>                      
                      <p style="margin-left: 25px;"><b>Ref No :</b> {result.refno}</p>
                      {#if result.hasOwnProperty('Comments')}
                      <p style="margin-left: 25px;"><b>Comments :</b> {result.Comments}</p>
                      {/if}
                      {#if result.hasOwnProperty('assign_Officer')}
                      <p style="margin-left: 25px;"><b>Assigned To :</b> {result.assign_Officer}</p>
                      {/if}
                      <p style="margin-left: 25px;"><b>Remarks :</b></p> <textarea readonly style="margin-left: 10px;"> {result.remarks}</textarea>
                    </div>
                    <div  class="d-flex" style="text-align: left;margin-top: 10px;">
                      {#if result.hasOwnProperty('raise_time')}
                        <p style="margin-left: 25px;" class="text-wrap"><b>Raised Date and Time :</b> {result.raise_time}</p>                
                      {/if}
                      {#if result.hasOwnProperty('Analyst_Approval')}
                          <p style="margin-left: 25px;" class="text-wrap"><b>Analyst Approved on :</b> {result.Analyst_Approval}</p>
                      {/if}
                      {#if userDetails.designation === 'INSPR' && userDetails.role !== 'Analyst'}
                          {#if result.hasOwnProperty('Send_time')}
                            <p style="margin-left: 25px;" class="text-wrap"><b>Received Date and Time :</b> {result.Send_time}</p>
                          {/if}
                          {#if result.hasOwnProperty('INSPR_Approval')}
                            <p style="margin-left: 25px;" class="text-wrap"><b>INS Approved on :</b> {result.INSPR_Approval}</p>
                          {/if}
                          {#if result.hasOwnProperty('INS_Reject')}
                            <p style="margin-left: 25px;" class="text-wrap"><b>INS Rejected on :</b> {result.INS_Reject}</p>       
                          {/if}
                      {:else if userDetails.designation === 'ADDL-SP/DSP'}
                        {#if result.hasOwnProperty('Send_to_DSP')}
                          <p style="margin-left: 25px;" class="text-wrap"><b>Received Date and Time :</b> {result.Send_to_DSP}</p>
                        {/if}
                        {#if result.hasOwnProperty('DSP_Approval')}
                          <p style="margin-left: 25px;" class="text-wrap"><b>DSP Approved on :</b> {result.DSP_Approval}</p>       
                        {/if}
                        {#if result.hasOwnProperty('DSP_Reject')}
                          <p style="margin-left: 25px;" class="text-wrap"><b>DSP Rejected on :</b> {result.DSP_Reject}</p>       
                        {/if}

                      {:else if userDetails.designation === 'SP'}
                        {#if result.hasOwnProperty('Send_to_SP')}
                          <p style="margin-left: 25px;" class="text-wrap"><b>Received Date and Time :</b> {result.Send_to_SP}</p>
                        {/if}
                        {#if result.hasOwnProperty('Analyst_Approval')}
                          <p style="margin-left: 25px;" class="text-wrap"><b>Analyst Approved on :</b> {result.Analyst_Approval}</p>
                        {/if}
                        {#if result.hasOwnProperty('SP_Approval')}
                          <p style="margin-left: 25px;" class="text-wrap"><b>SP Approved on :</b> {result.SP_Approval}</p>            
                        {/if}
                        {#if result.hasOwnProperty('DSP_Approval')}
                          <p style="margin-left: 25px;" class="text-wrap"><b>DSP Approved on :</b> {result.DSP_Approval}</p>       
                        {/if}
                        {#if result.hasOwnProperty('INSPR_Approval')}
                          <p style="margin-left: 25px;" class="text-wrap"><b>INS Approved on :</b> {result.INSPR_Approval}</p>
                        {/if}
                        {#if result.hasOwnProperty('DSP_Reject')}
                          <p style="margin-left: 25px;" class="text-wrap"><b>DSP Rejected on :</b> {result.DSP_Reject}</p>       
                        {/if}
                        {#if result.hasOwnProperty('SP_Reject')}
                          <p style="margin-left: 25px;" class="text-wrap"><b>SP Rejected on :</b> {result.SP_Reject}</p>       
                        {/if}
                        {#if result.hasOwnProperty('INS_Reject')}
                          <p style="margin-left: 25px;" class="text-wrap"><b>INS Rejected on :</b> {result.INS_Reject}</p>       
                        {/if}
                      {/if}
                    </div>
            {#if result !== ''}

            {#if result.requestcategory === 'Analysis Request'}
                  {#if userDetails.designation === 'INSPR' && userDetails.team === 'CAT'}
                  <div style="margin-top: 20px;">
                    <div>
                    {#if result.team === "AP" || result.team === "ISOT" || result.team === "CAT"}
                    <select bind:value={result.assign_Officer} style="width:130px !important;height:38px;margin-bottom:5px">
                      <option disabled selected value = "">Assign Officer</option>
                      {#each userDetails.ALL as alladmin}
                        <option value={alladmin.officername}>{alladmin.officername}</option>
                      {/each}
                    </select>    
                    <button on:click={toggleData} class="btn btn-outline-dark {result.pending=== "ADDL-SP/DSP Approval Pending" || result.pending === "SP Approval Pending" || result.pending === '--'
                                    || user.pending=== "Rejected by CAT Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.approval === "Assigned by CAT SP" || result.Comments  ? 'disabled' : ''}">Add Comments</button>                              
                        <div class="btn-group">
                          {#if selected1 === "Send to DSP"}
                          <button on:click={() => asigntoCAT(result,'ADDL-SP/DSP Approval Pending',"Assigned by CAT Ins")} class="btn btn-outline-success {result.pending=== "ADDL-SP/DSP Approval Pending" || result.pending === "SP Approval Pending"
                            || result.pending=== "Rejected by Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.approval === "Assigned by CAT SP" ? 'disabled' : ''}">{selected1}</button>
                            {/if}
                            {#if selected1 === "Self Approve"}
                          <button on:click={() => asigntoCAT(result,'--',"Assigned by CAT Ins")} class="btn btn-outline-success {result.pending=== "--" || result.pending === "SP Approval Pending"
                            || result.pending=== "Rejected by Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.approval === "Assigned by CAT SP" ? 'disabled' : ''}">{selected1}</button>
                            {/if}
                            {#if selected1 === 'Select'}
                          <button type="button" class="btn btn-outline-success" disabled>{selected1}</button>
                          {/if}
                          <button
                          class="btn btn-outline-success dropdown-toggle {result.pending=== "ADDL-SP/DSP Approval Pending" || result.pending === "SP Approval Pending" || result.pending === '--'
                          || result.pending=== "Rejected by CAT Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.approval === "Assigned by CAT SP" ? 'disabled' : ''}" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <span class="sr-only"></span>
                          </button>
                          <div class="dropdown-menu">
                            <a class="dropdown-item" on:click={() => handleSelect('Send to DSP')}>Send to DSP</a>
                            <a class="dropdown-item" on:click={() => handleSelect('Self Approve')}>Self Approve</a>
                          </div>
                        </div>
                        {/if}
                        </div>
                        </div>
                        {/if}
                        {#if userDetails.designation === "DSP" && userDetails.team === "CAT" || userDetails.designation === "ADDL-SP/DSP" && userDetails.team === "CAT"}
                                         <div style="margin-top: 20px;">
                                           <div>
                                             {#if result.team === "AP" || result.team === "ISOT" ||result.team === "CAT" }
                                             
                                             <select bind:value={result.assign_Officer} style="width:130px !important;height:38px">
                                               <option disabled selected value = "">Assign Officer</option>
                                               {#each userDetails.ALL as alladmin}
                                                 <option value={alladmin.officername}>{alladmin.officername}</option>
                                               {/each}
                                             </select>
                                             <button on:click={toggleData} class="btn btn-outline-dark {result.pending === "SP Approval Pending" || result.pending === "--" 
                                                || result.pending=== "Rejected by Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.pending === "Mail Under Process" || result.approval === "Assigned by CAT SP" ? 'disabled' : ''}">Add Comments</button>                      
                                             <div class="btn-group">
                                               {#if selected1 === "Send"}
                                               <button on:click={() => asigntoCAT(result, "SP Approval Pending","Assigned by CAT DSP")} class="btn btn-outline-success {result.pending === "SP Approval Pending" || result.pending === "Mail Under Process" 
                                                 || result.pending=== "Rejected by Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.pending === "Mail Under Process" || result.approval === "Assigned by CAT SP" ? 'disabled' : ''}">{selected1}</button>
                                                 {/if}
                                                 {#if selected1 === "Self Approve"}
                                               <button on:click={() => asigntoCAT(result,'--',"Assigned by CAT DSP")} class="btn btn-outline-success {result.pending === "SP Approval Pending" || result.pending === "--" 
                                                 || result.pending=== "Rejected by Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.pending === "Mail Under Process" || result.approval === "Assigned by CAT SP" ? 'disabled' : ''}">{selected1}</button>
                                                 {/if}
                                                 {#if selected1 === 'Select'}
                                           <button type="button" class="btn btn-outline-success" disabled>{selected1}</button>
                                           {/if}
                                               <button
                                               class="btn btn-outline-success dropdown-toggle {result.pending === "SP Approval Pending" || result.pending === "--" 
                                               || result.pending=== "Rejected by Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.pending === "Mail Under Process" || result.approval === "Assigned by CAT SP" ? 'disabled' : ''}"  type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                                 <span class="sr-only"></span>
                                               </button>
                                               <div class="dropdown-menu">
                                                 <a class="dropdown-item" on:click={() => handleSelect('Send')}>Send to SP</a>
                                                 <a class="dropdown-item" on:click={() => handleSelect('Self Approve')}>Self Approve</a>
                                                </div>
                                             </div>                                        
                                             <button on:click={() => asigntoCAT(result, "Rejected by DSP","-")} class="btn btn-outline-danger {result.pending === "SP Approval Pending" || result.pending === "--" 
                                              || result.pending=== "Rejected by Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.pending === "Mail Under Process" || result.approval === "Assigned by CAT SP" ? 'disabled' : ''}">Reject</button>
                                             {/if}
                                           </div>
                                         </div>
                                         <div>
                                         </div>
                        {/if}

                        {#if userDetails.designation === "SP" && userDetails.team === "CAT" || userDetails.designation === "SP" && userDetails.team === "ADMIN"}
                                      <div style="margin-top: 20px;">
                                       <div>
                                        {#if result.team === "AP" || result.team === "ISOT" ||result.team === "CAT" ||result.team === "ADMIN" }                                    
                                        <select bind:value={result.assign_Officer} style="width:130px !important;height:38px">
                                          <option disabled selected value = "">Assign Officer</option>
                                          {#each userDetails.ALL as alladmin}
                                            <option value={alladmin.officername}>{alladmin.officername}</option>
                                          {/each}
                                        </select>
                                        <button on:click={toggleData} class="btn btn-outline-dark {result.pending === "--" || result.pending=== "Rejected by Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.pending === "Mail Under Process"? 'disabled' : ''}">Add Comments</button>                      
                                        <button on:click={() => asigntoCAT(result,"--","Assigned by CAT SP")} class="btn btn-outline-success {result.pending === "--" || result.pending=== "Rejected by Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.pending === "Mail Under Process"? 'disabled' : ''}">Approve</button>
                                        <button on:click={() => asigntoCAT(result,"Rejected by SP", "-")} class="btn btn-outline-danger {result.pending === "--" || result.pending=== "Rejected by Ins" || result.pending=== "Rejected by DSP" || result.pending === "Rejected by SP" || result.pending === "Mail Under Process"? 'disabled' : ''}">Reject</button>
                                        {/if}
                                      </div>
                                    </div>
                                    <div>
                                </div>
                        {/if}
                        {#if showData}
                        <div class="row mb-3">
                            <div class="col-sm-3">
                                <label for="inputPassword3" class="col-sm-3 col-form-label">Comments</label>
                            </div>
                            <div class="col-sm-9">
                                <textarea name="comments" placeholder="Add Comment" id="comments" row="3" style='width: 1052px; margin-left: -494px ' aria-label="With textarea" bind:value={comments}></textarea>
                            </div>
                        </div>                   
                        <div class="row mb-3 justify-content-center text-center">
                            <div class="col-12">
                            <button type="button" on:click={() => handleSubmits(result)}  class="btn btn-success">submit</button>
                        </div>
                        </div>                                    
                      {/if}
                    
              {/if}
              <div class="d-flex justify-content-start">  
                <button on:click={fetchDataAndDownloadExcel(user)} type="button" class ="btn btn-outline-success" style="border-radius: 10px;margin-bottom:10px">
                  <i class="bi bi-cloud-arrow-down"></i>                   
              </button>
              </div>
                      {#if user.requesttype === "SDR" && (user.subtypes === "SDR" || user.subtypes === "SDR HISTORY") || user.requesttype === 'Analysis Note'}
                        <div class="col-auto scroll-table">
                            <table class="table table-bordered">
                              <thead class="table-dark" id="myhead">
                                <tr>
                                  <th>Phone NO.</th> 
                                  <th>MNP</th> 
                                </tr>
                              </thead>
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
                            <thead class="table-dark">
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
                            {/if}
                            </tr>
                            </thead>
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
                              {/if}
                            </tr>
                            {/each}
                          </table>
                        </div>
                        {/if}
                        {#if user.requestcategory === 'Analysis Request'}
                        {#if (!user.requesttypes.includes('IMEI') && user.subtypes !== "IMEI") && (!user.requesttypes.includes('TOWER DATA'))}
                        <div class="col-auto scroll-table">
                          <table class="table table-bordered">
                            <thead class="table-dark">
                            <tr>
                              <th>Phone No.</th> 
                              <th>Provider</th>
                              <th>From Date</th>
                              <th>To Date</th>
                          
                            </tr>
                            </thead>
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
                            <thead class="table-dark">
                            <tr>
                              <th>IMEI</th> 
                              <th>Provider</th>
                              <th>From Date</th>
                              <th>To Date</th>
                          
                            </tr>
                            </thead>
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
                              <thead class="table-dark" id="myhead">
                              <tr>
                                <th>Phone No.</th> 
                                <th>CAF No.</th>
                                <th>MNP</th>
                              </tr>
                              </thead>
                              {#each result.newnumber as newno}
                              <tr>
                                <td>{newno.Phno}</td>
                                <td>{newno.CAF}</td>
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
                        {#if user.requesttype === "CAF/CDR"}
                        <div class="col-auto scroll-table">
                          <table class="table table-bordered">
                            <thead class="table-dark">
                            <tr>
                              <th>Phone No./CAF No.</th> 
                              <th>From Date</th>
                              <th>To Date</th>
                            </tr>
                            </thead>
                            {#each result.newnumber as newno}
                            <tr class="table-dark">
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
                              <thead class="table-dark">
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
                              </thead>
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
                              {#if newno.hasOwnProperty('status')}
                              <td class = "{newno.status === "Data_Received" ? "Success" : "Rejected"}">{newno.status}</td>  
                              {:else}
                              <td></td> 
                              {/if}                        
                              {/if}
                              </tr>
                              {/each}
                            </table>
                          </div>
                          {/if}
                        {#if user.requesttype === "IPDR" && user.subtypes === "IPV6" || user.requesttype === "IPDR" && user.subtypes === "IPV4" || user.requesttype === "IPDR" && user.subtypes === ""}
                        <div class="col-auto scroll-table">
                          <table class="table table-bordered">
                            <thead class="table-dark">
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
                            </thead>
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
                        {#if user.requesttype === "RH" && user.subtypes === "Phone" || user.requesttype === "POA" && user.subtypes === "Phone"}
                        <div class="col-auto scroll-table">
                          <table class="table table-bordered">
                            <thead class="table-dark">
                            <tr>                                
                              <th>Phone</th>
                              <th>NickName</th>                                                          
                                <th>From Date</th>
                                <th>To Date</th>
                            </tr>
                            </thead>
                            {#each result.newnumber as newno}
                            <tr>
                              {#if user.requesttype === "RH"}
                              <td>{newno.Phno}</td>
                              <td class = "text-wrap">{newno.Nickname}</td>
                              {:else if user.requesttype === "POA"}
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
                        {#if user.requesttype === "RH" && user.subtypes === "Retailer/Dealer Details" || user.requesttype === "POA" && user.subtypes === "Retailer/Dealer Details"}
                        <div class="col-auto scroll-table">
                          <table class="table table-bordered">
                            <thead class="table-dark">
                            <tr>                                
                              <th>Dealer Details</th>
                              <th>Dealer Code</th>    
                              <th>Provider</th>                                                     
                                <th>From Date</th>
                                <th>To Date</th>
                            </tr>
                            </thead>
                            {#each result.newnumber as newno}
                            <tr>
                              {#if user.requesttype === "RH"}
                              <td>{newno.RH_Dealer}</td>
                              <td>{newno.RH_code}</td>
                              <td>{newno.ISP}</td>
                              {:else if user.requesttype === "POA"}
                              <td>{newno.POA_Dealer}</td>
                              <td>{newno.POA_code}</td>
                              <td>{newno.ISP}</td>
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
                            <thead class="table-dark">
                            <tr>
                              {#if user.subtypes === "CGI"}
                              <th>CGI ID</th>
                              <th>Provider</th>
                              <th>Status</th>
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
                            </thead>
                            {#each result.newnumber as newno}
                            <tr>
                              {#if user.subtypes === "CGI"}
                              <td>{newno.CGI}</td>
                              <td>{newno.ISP || ''}</td>
                              {#if newno.hasOwnProperty('status')}
                              <td class="{newno.status === "Data_Received" ? "Success" : "Rejected"}">{newno.status}</td>    
                              {:else}
                              <td></td>
                              {/if}      
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
                        {:else if user.requestcategory === 'Analysis Request' && user.requesttypes.includes('TOWER DATA')}
                        <div class="col-auto scroll-table">
                          <table class="table table-bordered">
                            <thead class="table-dark">
                            <tr>
                              {#if user.subtypes === "CGI"}
                              <th>CGI</th>
                              <th>Provider</th>
                              
                              {:else if user.subtypes === "Phone"}
                              <th>Phone</th>
                              {:else if user.subtypes === "Area"}
                              <th>Area</th>
                              <th>Cell IDs</th>
                              {:else if user.subtypes === "Co-Ordinates"}
                              <th>Latitude</th>
                              <th>Longitude</th>
                              {:else if user.subtypes === "Tower Name"}
                              <th>Tower Name</th>
                              {/if}                               
                                <th>From Date</th>
                                <th>To Date</th>
                            </tr>
                            </thead>
                            {#each result.newnumber as newno}
                            <tr>
                              {#if user.subtypes === "CGI"}  
                              <td>{newno.CGI}</td>
                              <td>{newno.ISP || ''}</td>
                              {:else if user.subtypes === "Phone"}
                              <td>{newno.Phno}</td>
                              {:else if user.subtypes === "Area"}
                              <td>{newno.Area}</td>
                              {:else if user.subtypes === "Co-Ordinates"}
                              <td>{newno.Latitude}</td>
                              <td>{newno.Longitude}</td>
                              {/if}
                              <td>{newno.From_Date}</td>
                              <td>{newno.To_Date}</td>
                            </tr>
                            {/each}
                          </table>
                        </div>
                        {/if}
            {/if}
                    
                    {#if user.requestcategory === 'Data Request' && (user.requesttype === 'CDR' || user.subtypes === 'Phone')}
                    <button class="btn btn-outline-warning" style="margin-bottom: 20px;" on:click={()=> autoresult(user._id)}>Automation Details</button>
                    <button class="btn btn-outline-primary" style="margin-bottom: 20px;" on:click={autoclose}>Close</button>
                      

                    {#if showData1}
                        <div class="d-flex justify-content-center">
                            <div>
                                <label for="inputPassword3">Are You Sure to Hold This Numbers?</label>
                                {msisdn}
                            </div>
                            <div  style="margin-left: 20px;">
                                <textarea name="comments" placeholder="Add Comment" id="comments" row="3" style='width: 1052px;' aria-label="With textarea" bind:value={mailer_remark}></textarea>
                            </div>
                        </div>                   
                        <div class="d-flex justify-content-center">
                              <button type="button" style="margin-bottom: 10px;" on:click={() => status_update(user,selectedOption2)} class="btn btn-warning"><i class="bi bi-slash-circle-fill"></i> Hold</button>
                        </div>                                    
                      {/if}


                      {#if auto_result !== ''}
                          <div style="max-height: 455px; overflow: auto;">
                            <table class="table table-striped text-nowrap" id="mytable">
                              <thead style="background-color: black;" class="text-white sticky-header">
                                <tr>
                                  <th>
                                    {#if userDetails.role === "Mailer"}
                                      <div class="btn-group mt-2">              
                                          {#if selectedOption2 === "Hold" && uniqid2 === user._id}
                                            <button class="btn btn-outline-warning" type="button" on:click={toggleData1}><i class="bi bi-check-square"></i></button>
                                          {:else}
                                          <button type="button" class="btn btn-outline-light" disabled>Select</button>
                                          {/if}
                                          <button
                                        class="btn btn-light dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                          <span class="sr-only"></span>
                                        </button>
                                        <div class="dropdown-menu">
                                          <a class="dropdown-item"  on:click={() => handleOptionSelect2('Select',user._id)}>Select</a>
                                          <a class="dropdown-item"  on:click={() => handleOptionSelect2('Hold',user._id)}>Hold</a>
                                        </div>
                                      </div>  
                                    {/if}      
                                  </th>
                                  <th>Status</th>
                                  <th style="width:50px">PhoneNumbers</th>
                                  <th>MNP</th>
                                  <th>Nickname</th>
                                  <th>SDR</th>
                                  <th>From Date</th>
                                  <th>To Date</th>
                                  <th>Truecaller</th>
                                  <th>Remark</th>
                                </tr>
                              </thead>
                                    {#each auto_result.result || [] as item }  
                                    {#if item.SDR !== "" || item.SDR === "" }
                                    <tr class="table-info ">
                                            <td >
                                              {#if userDetails.role === 'Mailer'}
                                              <input type="checkbox" class="cq checkbox-size {item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}" style="text-align:center; vertical-align: middle;" on:change={handleCheckboxChange1} id="checkbox_{user._id}" data-msisdn={item.MSISDN} value={item.MSISDN} />
                                            {/if}                                            </td>
                                            <td class="td {item.mailer_hold === "Hold by Mailer" ? "disabled" : ""} {item.status === "Data_Received" ? "Success" : "Rejected"}" >
                                              {#if item.hasOwnProperty('mailer_hold')}
                                                {item.mailer_hold}
                                              {:else if item.hasOwnProperty('status')}
                                                {item.status}
                                              {:else}
                                                {auto_result.pending}
                                              {/if}
                                            </td>
                                                <td class="td {item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">
                                                  {item.MSISDN}
                                                </td>
                                                <td class="td {item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">
                                                    {item.MNP}
                                                </td>
                                                <td class="td {item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">
                                                    <div class="divScroll" data-bs-toggle="tooltip" 
                                                    data-bs-placement="top" 
                                                    title='{item.FetchedNickName}'>
                                                    {item.FetchedNickName}
                                                    </div>     
                                                </td>
                                                <td class="mnp  {item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">
                                                <textarea readonly data-bs-toggle="tooltip" 
                                                style="width: 582px;height: 76px; text-align:left"
                                                data-bs-placement="top" 
                                                title='{item.SDR}'>
                                                  {item.SDR}
                                                </textarea>                     
                                                </td>
                                                <td class="td mnp1 {item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">
                                                  {item.From_date || item.From_Date}
                                                </td>
                                                <td class="td mnp1 {item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">
                                                {item.To_date || item.To_Date}
                                                </td>
                                                <td class="td {item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">
                                                  {item.Truecaller}
                                                </td>
                                                <td class="td {item.mailer_hold === "Hold by Mailer" ? "disabled" : ""}">   
                                                  {#if item.hasOwnProperty('mailer_remarks')}               
                                                    {item.mailer_remarks}   
                                                  {:else}
                                                    {item.Remarks}
                                                  {/if}  
                                                </td>
                                                </tr>
                                      {/if}
                                      {/each}
                            </table>
                          </div>
                      {/if}
                    {/if}
                  </div>
                  <div class="modal-footer">
                    <button class="btn btn-primary" data-bs-dismiss="modal">Close</button>
                  </div>
                </div>
              </div>
            </div>
            </tr>
    {/each}
    </table>      
    <div class="page d-flex justify-content-end mr-5" style="margin-right:50px">
      <nav aria-label="Page navigation">
        <ul class="pagination d-flex justify-content-end">
          <p class="mr-3 mt-2" style="margin-right:15px">Showing {cases2.length} out of {pagination2.total_tickets1} rows</p>
          <li class="page-item">
            <button class="page-link" on:click={() => fetchTickets1(currentPage1)}>First</button>
          </li>
          <li class="page-item">
            <button class="page-link" aria-label="Previous" on:click={prevPage1} disabled={currentPage1 === 1}>
              <span aria-hidden="true">&laquo;</span>
            </button>
          </li>
          {#each Array.from({ length: Math.min(pagination2.total_pages1, 5) }, (_, i) => i + 1 + (currentPage1 > 5 ? currentPage1 - 5 : 0)) as page}
            <li class="page-item">
              <button class="page-link {page === currentPage1 ? 'selected' : ''}" on:click={() => fetchTickets1(page)}>{page}</button>
            </li>
          {/each}
          <li class="page-item">
            <button class="page-link" aria-label="Next" on:click={nextPage1} disabled={currentPage1 === pagination2.total_pages1}>
              <span aria-hidden="true">&raquo;</span>
            </button>
          </li>
          <li class="page-item">
            <button class="page-link" on:click={() => fetchTickets1(pagination2.total_pages1)}>Last</button>
          </li>
        </ul>
      </nav>
    </div>
      </div>
      {:else}
  <p class="d-flex justify-content-center mt-5 no-data">NO DATA</p>
  {/if}
    </div>
    </div>
    </main>
    </div> 