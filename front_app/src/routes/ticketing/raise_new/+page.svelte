<script>
// @ts-nocheck

import '../global.css';
import { goto } from "$app/navigation"
import {basepath} from "$lib/config";
import { onMount } from 'svelte';
import { page } from "$app/stores";


import { userDetailsStore } from '$lib/datastore.js';
console.log("userDetailsStore",userDetailsStore)
let userDetails;

userDetailsStore.subscribe(value => {
userDetails = value;
console.log("value",value)
});

console.log("demo",userDetails);
onMount(() => {
      // beware of truthy and falsy values
      if (localStorage.getItem("userAuth")==="true"){
          // console.log("jsno",localStorage.getItem("userDetails"))
          // console.log('auth is passed')
         userDetailsStore.set(JSON.parse(localStorage.getItem("userDetails")))
         
      }
      else{
          goto('/');
      }
  })
  async function logout() {
      await fetch(basepath()+'/logout', {
          method: 'POST',
          headers: {
          'Content-Type': 'application/json'
      }
  })

// Set the authentication to false
localStorage.setItem("userAuth", false);

// Redirect the user to the login page after logging out
goto('/');
}

function close(){
  window.location.reload();
}

const url = $page.url;
let id;
id = url.search.replace("?id=", "");
console.log(id);

let data = [];
let requestcategory = 'Data Request';
let update = 'NEW';
let requesttype = ''
let fromDate = [''];
let toDate = [''];
 let newtype = '';
 $: newtype = (input_type|| secondDropdownValue || showPoaDropdownvalue || showCdrDropdownvalue || showGprssDropdownvalue || showGprsDropdownvalue || showRhDropdownvalue || sdrdropdown || showIpdrDropdownvalue)
 let phoneNumbersArray = [''];
 let phoneNumberToNickname = {};
 let cellInput = {};
 let provider = [];
 let requesttypes = [];

 let phoneNumbers = '';
 $: phoneNumbers = phoneNumbersArray
 let name = '';
 let phnumber = '';
 let state = '';
 let roaming = '';
 let team = '';
 let modules = '';
 let relation = '';
 let nickname = '';
 $: nickname =  (userDetails.modules)  + '_' + name + '_' + location + '_' + relation;
 let suspect = '';
 let location = '';
 let source = '';
 let reason = '';
 let refno = '';
 let refdate = '';
 let sdr = '';
 let truecaller = '';
 let priority = '';
 let required = '';
 let isp = '';
 let firstDropdownValue = '';
 let  secondDropdownValue = '';
  let showPoaDropdownvalue = '';
  let showCdrDropdownvalue ='';
  let showGprsDropdownvalue = '' ;
  let showIpdrDropdownvalue = '' ;
  let showRhDropdownvalue = '' ;
  let sdrdropdown = "";
  let showGprssDropdownvalue = '';
 let fromdatepicker ='';
 let fromdatepicker12 ='';
 let showIsotDetailsvalue ='';
 let showApDetailsvalue = '';
 let showCatDetailsvalue = '';
 let remarks='';
 let token = '';
 let POA_NAME=[""];
 let POA_CODE_Dealerid = [""];
 let latitude = [''];
 let longitude = [''];
 let IMEI = [''];
 let POA = [""];
 let input_type = '';
 let input_type1 = '';
let fileData = '';
let date = ''
let header = [];
let showinput = false;
let analysisreq =[];
let newnumber = [
  {
    Phno: '',
    Nickname: '',
    Latitude: '',
    Longitude: '',
    IMEI: '',
    CGI: '',
    IP_Address: '',
    Area: '',
    Tower_name: '',
    RH_Dealer:'',
    RH_code:'',
    POA_Dealer:'',
    POA_code:'',
    Cell_id: '',
    Rad:'',
    CAF:'',
    Provider:'',
    From_Date:'',
    From_Time:'',
    To_Date:'',
    To_Time:'',
    ISP:''

  }
];
async function raise_new_data(){
    if (id){
    const response = await fetch(basepath() + '/raise_new_data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          id: id
  })
  });
  const cases = await response.json();
  if (response.ok){
    console.log(cases)
    data = cases
    refno = data[0]['refno'];
    refdate = data[0]['refdate'];
    token = data[0]['token'];
    priority = data[0]['priority'];
    remarks =  data[0]['remarks'];
    newnumber = data[0]['newnumber'];
    requesttype = data[0]['requesttypes'][0];
    console.log(requesttype);
    // newtype = data[0]['subtypes'];
    secondDropdownValue  =data[0]['subtypes'];
    showPoaDropdownvalue=data[0]['subtypes'];
    showCdrDropdownvalue=data[0]['subtypes'];
    showGprsDropdownvalue=data[0]['subtypes'];
    showIpdrDropdownvalue=data[0]['subtypes'];
    showRhDropdownvalue=data[0]['subtypes'];
    sdrdropdown=data[0]['subtypes'];
    showGprssDropdownvalue
    console.log(newnumber,'newnumber');
    const columns = data[0]['newnumber'];
    if (columns.length > 0) {
  const order = [
    "Phno",
    "ISP",
    "Nickname",
    "Latitude",
    "Longitude",
    "IMEI",
    "CGI",
    "IP_Address",
    "Area",
    "Tower_name",
    "RH_Dealer",
    "RH_code",
    "POA_Dealer",
    "POA_code",
    "Cell_id",
    "Rad",
    "CAF",
    "Provider",
    "From_Date",
    "From_Time",
    "To_Date",
    "To_Time"
  ];

  const firstRow = columns[0];
  header = order.filter(key => firstRow[key] !== "");

  console.log(header);
}}
}
for (let i = 0; i < newnumber.length; i++) {
  const res = newnumber[i];

  handleNicknameInput(res.Phno)
  phone_match(res.Phno, i);
}
}


onMount(()=>{
  raise_new_data();
})



let showSecondDropdown = false;
let showCdrDropdown = false;
let showIpdrDropdown = false;
let showGprsDropdown = false;
let showPoaDropdown = false;
let showRhDropdown = false;
let showGprssDropdown = false;


function handleFirstDropdownChange() {
  // onRequesttypeChange()
  if (requesttype !== 'IPDR') {
    showSecondDropdown = false;
  } else {
    showSecondDropdown = true;
  }
  if (requesttype !== 'GPRS') {
    showGprssDropdown = false;
  } else {
    showGprssDropdown = true;
  }
  if (requesttype !== 'TOWER CDR') {
    showCdrDropdown = false;
  } else {
    showCdrDropdown = true;
  }
  if (requesttype !== 'TOWER GPRS') {
    showGprsDropdown = false;
  } else {
    showGprsDropdown = true;
  }
  if (requesttype !== 'TOWER IPDR') {
    showIpdrDropdown = false;
  } else {
    showIpdrDropdown = true;
  }
  if (requesttype !== 'POINT OF ACTIVATION (POA)') {
    showPoaDropdown = false;
  } else {
    showPoaDropdown = true;
  }
  if (requesttype !== 'RECHARGE HISTORY (RH)') {
    showRhDropdown = false;
  } else {
    showRhDropdown = true;
  }
  

}
onMount(() => {
  // Call handleFirstDropdownChange initially to set the initial value of showSecondDropdown
  handleFirstDropdownChange();
});
let index=0;
let startDate;
let endDate;
let mindate;
const today = new Date();

const year = today.getFullYear(); // Get the four-digit year
const month = String(today.getMonth() + 1).padStart(2, '0'); // Get the month (0-11) and add leading zero if necessary
const day = String(today.getDate()).padStart(2, '0'); // Get the day of the month and add leading zero if necessary

const formattedDate = `${day}/${month}/${year}`; // Create the formatted date string
mindate = `${String(today.getDate() + 1).padStart(2, '0')}/${month}/${2021}`;
console.log(formattedDate);
async function newform() {
  // if (

  //   phoneNumbers === '' ||
  //   requestcategory === '' ||
  //   requesttype === '' ||
  //   team === '' ||
  //   name === '' ||
  //   location === '' ||
  //   fromdatepickerpicker === '' ||
  //   todatepickerpicker === ''

  // ) 
  // {
  //   alert('Please fill in all the required fields.');
  //   return;
  // }
      
  

   const response = await fetch(basepath()+'/newform_converter', {
     method: 'POST',
     headers: {
       'Content-Type': 'application/json'
     },
     body: JSON.stringify({
      update:update,
      requestcategory:requestcategory,
      requesttype:requesttype,
      subtype:newtype,
      date:formattedDate,
      sdrdropdown:sdrdropdown,
      phoneNumbers:phnumber,
      Numbers:phoneNumbers,
      status:'Converted',
      token:token,
      team:userDetails.team,
      modules:userDetails.modules,
      relation:relation,
      nickname:nickname,
      suspect:suspect,
      name:name,
      location:location,
      source:source,
      reason:reason,
      refdate:refdate,
      refno:refno,
      fileData:fileData,
      priority:priority,
      remarks:remarks,
      officername: userDetails.officername,
      useremail: userDetails.email,
      superior: userDetails.superior,
      role: userDetails.role,
      newnumber:newnumber,
      designation :userDetails.designation,

     })
     
   });
   console.log(phnumber)
   const result = await response.json();
  //  goto('/newanalystdata');
    goto('/ticketing/Datareq/'); 
 }

 function again_check(){ //for Manually Enter Phone Number of using Excel File Some Numbers Nickname Not Present in DB then using this Add oor Desire Nickname using module/name/loc/rel
  if (newtype !== 'IMEI' || requesttype !== 'IMEI CDR'){
    if (userDetails.modules !== '' && name !== '' && location !== '' && relation !== ''){
      for (let i = 0; i < newnumber.length; i++) {
        const data = newnumber[i];
        console.log(data)
        phone_match(data['Phno'],i)
      }
    }
  }
}

 async function phone_match(number, index) {  //For Nickname Fetching from CDAT DATA
  console.log(number)
  try {
    const response = await fetch(basepath() + '/nickname_search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        phone: number
      })
    });

    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }
      const cases = await response.json();
      // console.log('Response Data:', cases);
      const loadingIndicator = document.getElementById(`fetchnickname${index}`);
      loadingIndicator.style.display = 'block';
      analysisreq = cases;
      showinput = true;
      console.log(analysisreq,'//////////////////////////////////////////////')
      phoneNumberToNickname[number] = analysisreq.nickname;
      const nicknameElement = document.getElementById(`fetchnickname${index}`);
    
        if (phoneNumberToNickname[number] === "") { //If Nickname not present in DB then its create dynamically a Nickname using module/name/loc/rel
          if (userDetails.modules !== '' && name !== '' && location!== "" && relation !== ''){
            newnumber[index]["Nickname"] = (userDetails.modules + '_' + name + '_' + location + '_' + relation);
          }
          nicknameElement.style.color = "red";
        
        } else { //If present then show green if not then red
          newnumber[index]["Nickname"] = (phoneNumberToNickname[number] || '');
          nicknameElement.style.color = "green";// Set text color to green
        }
      
      } 
    // console.log(phoneNumberToNickname);
  catch (error) {
    console.error(error);
  }
}

function handleNicknameInput(phoneNumber) {
  phoneNumberToNickname[phoneNumber] = analysisreq.nickname;
}





</script>

<style>
   main{
    background:linear-gradient(120deg, #e2e2e2, #e2e2e2);
    background-color: #c0ace0;
    width: auto;
    height: auto;
    }
h3 {
  
    font-weight: bold;
    color: white;
}

select {
    border: none;
    border-radius: 4px;
    padding: 2px;
    

}
.second_dd{
  margin-left:20px;
}
form{
     box-shadow: 0 .5rem 1rem rgb(0, 0, 0)!important;    
     background:linear-gradient(120deg, #e2e2e2, #e2e2e2);
     
     border-radius: 10px;
      margin-bottom: 50px;
  
  }
a{
  text-decoration: none;
}
#flex-container {
  display: flex;
  justify-content: center;
  /* max-height: 20em;
  overflow-y: scroll; */
}
#flex-container1{
  display: flex;
  justify-content: center;
  margin-left: 100px;
}
#flex-container2{
  display: flex;
  justify-content: center;
  margin-left: 135px;
}
.flex-item {
  width: 185px;
  margin-left: 2px;
 
}
.uni{
margin-left: 23.7%;
margin-top: 20px;
}
.text{
margin-left: 24%;
}
.scroll-table {
  display: flex;
  justify-content: center;
  max-height: 20em;
  overflow-y: scroll;
}
.clear{
  width:50px;
  border-radius: 10px;
  margin-bottom: 5px;
  margin-left: 5px;
}
#flex-container-caf{
  display: flex;
  justify-content: center;
  margin-left: -88px;
  
}
.table-bordered th, .table-bordered td {
            border: 1px solid #dee2e6;
            padding: 0.75rem;
            border-collapse: collapse;
}

.show{
 padding-left: 0 !important;
 padding-right: 0 !important;
}
</style>
<main>
  <nav class="navbar navbar-dark bg-dark" style="background-color: #343a40!important;">
    <div></div>
    <h3>Data Request</h3>
    <div class="pt-0 ">
      <div class="d-flex justify-content-end bd-highlight">
        <div class="p-2 bd-highlight">
          <div class="search-container">
          </div>
      </div>
    </nav>

    <section>
    <div class="container">
      <form action="" class="p-5">
        <div class="row mb-3">
        <div class="col-3">IO NAME</div>
        <input type="text" disabled class="col-sm-4 border-0 text-dark" bind:value={userDetails.officername}/>
        </div>
        <div class="row mb-3 d-none">
        <div class="col-3 ">Login Email</div>
        <input type="text" class="col-sm-4 border-0" bind:value={userDetails.email}/>
        </div>
        <div class="row mb-3">
        <label class="col-sm-3 col-form-label">TEAM</label>
        <input class="col-sm-4 border-0" bind:value={userDetails.team} readonly>
        </div>
        <div class="row mb-3">
        <label class="col-sm-3 col-form-label">MODULE</label>
        <input class="col-sm-4 border-0" bind:value={userDetails.modules} readonly>
        </div>

        {#each data as user}
        <div class="row mb-3">
          <label class="col-sm-3 col-form-label">REQUEST CATEGORY</label>
          <input class="col-sm-4 border-0" bind:value={requestcategory} readonly>
          </div>
          <div class="row mb-3">
            <label class="col-sm-3 col-form-label">NEW/UPDATE</label>
            <input class="col-sm-4 border-0" bind:value={update} readonly>
          </div>
          <div class="row mb-3">
            <label class="col-sm-3 col-form-label">REQUEST TYPE</label>
            <!-- <MultiSelect id='lang'  bind:value={requesttype} on:change={handleFirstDropdownChange}> -->
              <select class="col-sm-4" bind:value={requesttype}>
                <option value="">Select </option>
                <option value="CAF">CAF</option>
                <option value="SDR">SDR</option>
                <option value="CDR">CDR</option>
                <option value="CAF/CDR">CAF/CDR</option>
                <option value="ISD">ISD</option>
                <option value="GPRS">GPRS</option>
                <option value="IPDR">IPDR</option>
                <option value="RECHARGE HISTORY (RH)">RECHARGE HISTORY (RH)</option>
                <option value="POINT OF ACTIVATION (POA)">POINT OF ACTIVATION (POA)</option>
                <option value="IMEI CDR"> IMEI CDR</option>
                <option value="TOWER CDR">TOWER CDR</option>
                <option value="TOWER GPRS">TOWER GPRS</option>
                <option value="TOWER IPDR">TOWER IPDR</option>
                <!-- <option value="POA OF DEALER">POA OF DEALER</option> -->
                
              </select>
              {#if requesttype === "IPDR"}
              <select class="col-sm-2" style = "margin-left:5px;" bind:value={secondDropdownValue} >
                <option value="">Select </option>
                <option value="IPV6">IPV6</option>
                <option value="IPV4">IPV4</option>
                <option value="IMEI">IMEI</option>
                <option value="Phone">Phone</option>
                </select>
                {/if}
                {#if requesttype === "GPRS"}
                <select class="col-sm-2" style = "margin-left:5px;" bind:value={showGprssDropdownvalue}  >
                <option value="">Select </option>
                <option value="Phone">Phone No.</option>
                <option value="IMEI">IMEI</option>
                </select>
                {/if}
                {#if requesttype === "TOWER CDR" || requesttype === "TOWER GPRS"||requesttype === "TOWER IPDR"}
                <select class="col-sm-2 ml-1" style="margin-left:5px" bind:value={showCdrDropdownvalue}>
                  <option value="">Select </option>
                  <option value="CGI">CGI (Cell ID)</option>
                  <option value="Phone">Phone No.</option>
                  <!-- <option value="Area">Area</option> -->
                  <option value="Co-Ordinates">Co-Ordinates</option>
                  <!-- <option value="Tower Name">Tower Name</option>   -->
                </select>
                {/if}
                {#if requesttype === "RECHARGE HISTORY (RH)"||requesttype === "POINT OF ACTIVATION (POA)"}
                <select class="col-sm-2" style = "margin-left:5px;" bind:value={showPoaDropdownvalue}>
                  <option value="">Select </option>
                  <option value="Phone">PHONE</option>
                  <option value="Retailer/Dealer Details">Retailer/Dealer Details</option>
                  <!-- <option value="Retailer/Dealer Code*">Retailer/Dealer Code*</option> -->
                </select>
                {/if}
                {#if requesttype === "SDR"}
                <select class="col-sm-2" style = "margin-left:5px;" bind:value={sdrdropdown}>
                  <option value="">Select </option>
                  <option value="SDR">SDR</option>
                  <option value="SDR HISTORY">SDR History</option>
                </select>
                {/if}
                </div>

                <div class="row mb-3">
                  <label class="col-sm-3 col-form-label">NAME-LOCATION</label>
                  <input class="col-sm-4 border-0" placeholder="Name" bind:value={name} on:input={again_check}>
                </div>
            
                <div class="row mb-3">
                  <label class="col-sm-3 col-form-label"></label>
                  <input class="col-sm-4 border-0" placeholder="Location" bind:value={location} on:input={again_check}>
                </div>
            
                <div class="row mb-3">
                  <label class="col-sm-3 col-form-label">RELATIONSHIP/ASSOCIATION</label >
                  <input class="col-sm-4 border-0" placeholder="Relationship/Association" on:input={again_check} bind:value={relation}>
                </div>
                {#if requesttype !== "CDR" && requesttype !== "POINT OF ACTIVATION (POA)"&& requesttype !== "RECHARGE HISTORY (RH)" && requesttype !== "GPRS" && requesttype !== "IPDR" && requesttype !== "TOWER CDR" && requesttype !== "TOWER GPRS" && requesttype !== "TOWER IPDR"}
                <div class="row mb-3">
                  <label class="col-sm-3 col-form-label">NICKNAME</label>
                  <input class="col-sm-4 border-0" bind:value={nickname} readonly>
                </div>
                {/if}

                <div class="row mb-2">
                  <label class="col-sm-3 col-form-label">ENTER INPUTS</label>
                  {#if requesttype === "CDR" || showGprssDropdownvalue === 'Phone' || showCdrDropdownvalue === "Phone" || showPoaDropdownvalue === "Phone" || secondDropdownValue === "Phone"}
                      <div class="col-auto scroll-table">
                      <table class="table table-bordered">
                      <tr>
                      <th>Phone</th>
                      <th>Nickname</th>
                      <th>From_Date</th>
                      <th>To_Date</th>
                      </tr>
                      {#each user.newnumber as record, index}
                      <tr>
                      <td> {record.Phno}</td>
                      <td>
                        <input type="text" style="margin-top: -1px;" class="border-0" id="fetchnickname{index}" bind:value={newnumber[index]["Nickname"]}>
                      </td>
                      <td>{record.From_Date}</td>
                      <td>{record.To_Date}</td>
                      </tr>
                      {/each}
                      </table>
                      </div>
                  {:else if requesttype !== ""}
                      <div class="col-auto scroll-table">
                      <table class="table table-bordered">
                      <tr>
                      {#each header as columnName}
                        <th>{columnName}</th>
                      {/each}
                      </tr>
                      {#each user.newnumber as record, index}

                        <tr>
                          {#each header as columnName}
                            <td>{record[columnName]}</td>

                          {/each}
                        </tr>
                      {/each}
                      </table>
                      </div>
                      {/if}
                </div>   
                <div class="row mb-3">
                  <label class="col-sm-3 col-form-label">SUSPECT CATEGORY</label>
                  <select class="col-sm-4" bind:value={suspect}>
                    <option value="">Select </option>
                    <option value="A">A</option>
                    <option value="B">B</option>
                    <option value="C">C</option>
                    <option value="D">D</option>
                    <option value="UNKNOWN">UNKNOWN</option>
                  </select>
                </div>

                <div class="row mb-3">
                  <label class="col-sm-3 col-form-label">SOURCE TYPE</label>
                  <select class="col-sm-4" label="SOURCE TYPE" value={source}>
                    <option selected value="">Select</option>
                    <option value="LOGGER">LOGGER</option>
                    <option value="ANALYSIS">ANALYSIS</option>
                    <option value="TEAM">TEAM</option>
                    <option value="FIELD">FIELD</option>
                    <option value="INTERNET">INTERNET</option>
                    <option value="IR">IR</option>
                    <option value="OTHER AGENCY">OTHER AGENCY</option>
                    <option value="SOURCE">SOURCE</option>
                    <option value="DOCUMENTS RECOVERY">DOCUMENTS RECOVERY</option>
                    <option value="WEBINT">WEBINT</option>
                  </select>
                </div>
                <div class="row mb-3">
                  <label class="col-sm-3 col-form-label">REF NO - DATE</label> 
                  <input class="col-sm-2 border-0" placeholder="REF NO" type="text" bind:value={refno}> 
                  <input class="col-sm-2 border-0" readonly style="margin-left: 5px;width:170px" type="text" bind:value={refdate}> 
                </div>

                <div class="row mb-3">
                  <label class="col-sm-3 col-form-label">PRIORITY</label> 
                  <input class="col-sm-4 border-0" placeholder="PRIORITY" type="text" bind:value={priority}> 
                </div>

                <div class="row mb-3">
                  <label class="col-sm-3 col-form-label">REMARK</label> 
                  <textarea class="col-sm-4 border-0" rows="3" id="comment" bind:value={remarks}></textarea>
                </div>

                <div class="text-center">
                  <button
                  on:click={newform}
                  class="btn-outline-success rounded mt-5 p-2"
                  type="submit">Submit</button>
                </div>
        {/each}
      </form>
    </div>
    </section>
</main>