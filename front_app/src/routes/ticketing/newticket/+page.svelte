<script>
  // @ts-nocheck
  
    // import '../global.css';
    import Navbar from "$lib/component/Navbar.svelte";
    import { goto } from "$app/navigation"
    import {basepath} from "$lib/config";
    import SelectDropdown from "$lib/component/SelectDropdown.svelte";
    import RadioButtons from "$lib/component/RadioButtons.svelte";
    import TextArea from "$lib/component/TextArea.svelte";
    import InputField from "$lib/component/InputField.svelte";
    import RadioButton from "$lib/component/RadioButton.svelte";
     import { onMount } from 'svelte';
     import flatpickr from 'flatpickr';
  import 'flatpickr/dist/flatpickr.css';
  import * as XLSX from 'xlsx';
  import { page } from "$app/stores";
  // import { toasts, ToastContainer, BootstrapToast }  from "svelte-toasts";
  import { toasts, ToastContainer, FlatToast }  from "svelte-toasts";
  
  import { userDetailsStore } from '$lib/datastore.js';
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
           
        }
        else{
            goto('/');
        }
    })

    async function sample_excel(){
      try {
      const response = await fetch(basepath() + '/sample_excel')
          
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
let mindate;
const today = new Date();
const year = today.getFullYear(); // Get the four-digit year
const month = String(today.getMonth() + 1).padStart(2, '0'); // Get the month (0-11) and add leading zero if necessary
const day = String(today.getDate()).padStart(2, '0'); // Get the day of the month and add leading zero if necessary
const formattedDate = `${day}/${month}/${year}`; // Create the formatted date string
mindate = `${String(today.getDate() + 1).padStart(2, '0')}/${month}/${2021}`;
let formattedDate1;
const today1 = new Date();
formattedDate1 = `${today1.getDate()}-${today1.getMonth() + 1}-${today1.getFullYear()}_${today1.getHours()}${today1.getMinutes()}${today1.getSeconds()}${today1.getMilliseconds()}`;
formattedDate1 = formattedDate1
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
console.log('////////////////////',formattedDate2)
let cases = [];
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
    ISP:[],
    Remarks:'',
    showDropdown : false
  }
];
let nickname = '';
$: nickname =  (modules  + '_' + name + '_' + location + '_' + relation);
async function phone_match(number, index) {  //For Nickname Fetching from CDAT DATA
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
      phoneNumberToNickname[number] = analysisreq.nickname;
      const nicknameElement = document.getElementById(`fetchnickname${index}`);
    
        if (phoneNumberToNickname[number] === "") { //If Nickname not present in DB then its create dynamically a Nickname using module/name/loc/rel
          if (module !== '' && name !== '' && location!== "" && relation !== ''){
            newnumber[index]["Nickname"] = (module + '_' + name + '_' + location + '_' + relation);
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

onMount(() => { // For User Authantication Login
  // beware of truthy and falsy values
  if (localStorage.getItem("userAuth") === "true") {
    console.log('auth is passed')
  }});


function again_check(){ //for Manually Enter Phone Number of using Excel File Some Numbers Nickname Not Present in DB then using this Add oor Desire Nickname using module/name/loc/rel
  if (newtype !== 'IMEI' || requesttype !== 'IMEI CDR'){
    if (module !== '' && name !== '' && location !== '' && relation !== ''){
      for (let i = 0; i < newnumber.length; i++) {
        const data = newnumber[i];
        console.log(data)
        phone_match(data['Phno'],i)
      }
    }
  }
}

 let fromDate = [''];
 let toDate = [''];
 let update = '';
 let requestcategory = '';
 let requesttype = '';
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
 let isot_modules = ''
 let relation = '';
 let modules = '';
$: modules = (isot_modules || userDetails.modules) 
 let suspect = '';
 let location = '';
 let source = '';
 let reason = '';
 let refno = '1';
 let refdate = '';
 $: refdate = year;
 let sdr = '';
 let truecaller = '';
 let priority = 'Normal';
 let isp = '';
 let secondDropdownValue = '';
  let showPoaDropdownvalue = '';
  let showCdrDropdownvalue ='';
  let showGprsDropdownvalue = '' ;
  let showIpdrDropdownvalue = '' ;
  let showRhDropdownvalue = '' ;
  let sdrdropdown = "";
  let showGprssDropdownvalue = '';
  let fromdatepicker ='';
  let module ='';
  let todatepicker= formattedDate;
  let remarks='';
  let POA_NAME=[""];
  let POA_CODE_Dealerid = [""];
  let latitude = [''];
  let longitude = [''];
  let IMEI = [''];
  let input_type = '';
  let input_type1 = '';
  let fileData = '';
  let cell = [];


// async function newanalysis() {  //For SAVE ANALYSIS REQ FORM DATA
//  const response = await fetch(basepath()+'/newanalysis', {
//    method: 'POST',
//    headers: {
//      'Content-Type': 'application/json'
//    },
//    body: JSON.stringify({
//     update:update,
//     requestcategory:requestcategory,
//     requesttypes:requesttypes,
//     requesttype:requesttype,
//     subtype:newtype,
//     date:formattedDate,
//     phoneNumbers: phoneNumbers,
//     team:userDetails.team,
//     modules:userDetails.modules,
//     reason:reason,
//     refdate:refdate,
//     refno:refno,
//     priority:priority,
//     remarks:remarks,
//     officername: userDetails.officername,
//     useremail: userDetails.email,
//     superior: userDetails.superior,
//     role: userDetails.role,
//     input_type:input_type,
//     input_type1:input_type1,
//     fromDate:fromDate,
//     toDate:toDate,
//     designation :userDetails.designation,
//     newnumber:newnumber,
//     raise_time : formattedDate2


//    })
//  });
// //  goto('/newanalystdata');
//   goto('/ticketing/Analysisreq/');
// }

async function newanalysis() {
  // Get the value of the reason dropdown
  const reasonValue = reason;

      if (reasonValue === "Select Reason") {
        alert("Please select a reason.");
        return; 
    } else if (showDropdown1 || !secondDropdownValue) {
        alert("Please select at least one request type.");
        return; // Exit the function without sending the form data
    } 

  // If the reason is selected, proceed with sending the form data
  const response = await fetch(basepath()+'/newanalysis', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      update:update,
      requestcategory:requestcategory,
      requesttypes:requesttypes,
      requesttype:requesttype,
      subtype:newtype,
      date:formattedDate,
      phoneNumbers: phoneNumbers,
      team:userDetails.team,
      modules:userDetails.modules,
      reason:reason,
      refdate:refdate,
      refno:refno,
      priority:priority,
      remarks:remarks,
      officername: userDetails.officername,
      useremail: userDetails.email,
      superior: userDetails.superior,
      role: userDetails.role,
      input_type:input_type,
      input_type1:input_type1,
      fromDate:fromDate,
      toDate:toDate,
      designation :userDetails.designation,
      newnumber:newnumber,
      raise_time : formattedDate2
    })
  });

  // Redirect to the specified route after sending the form data
  goto('/ticketing/Analysisreq/');
}


async function update_nickname(num){  //Update New Nicknames to CDAT DB
  const response = await fetch(basepath()+'/update_nickname', {
     method: 'POST',
     headers: {
       'Content-Type': 'application/json'
     },
     body: JSON.stringify({
        num: num,
        email:userDetails.email,
     })
});
}

// async function newform() { //For SAVE DATA REQ FORM DATA
//    const response = await fetch(basepath()+'/newform', {
//      method: 'POST',
//      headers: {
//        'Content-Type': 'application/json'
//      },
//      body: JSON.stringify({
//       update:update,
//       requestcategory:requestcategory,
//       requesttype:requesttype,
//       subtype:newtype,
//       date:formattedDate,
//       sdrdropdown:sdrdropdown,
//       phoneNumbers:phnumber,
//       Numbers:phoneNumbers,
//       team:userDetails.team,
//       modules:modules,
//       relation:relation,
//       nickname:nickname,
//       suspect:suspect,
//       name:name,
//       location:location,
//       source:source,
//       reason:reason,
//       refdate:refdate,
//       refno:refno,
//       fileData:fileData,
//       remarks:remarks,
//       officername: userDetails.officername,
//       useremail: userDetails.email,
//       superior: userDetails.superior,
//       role: userDetails.role,
//       newnumber:newnumber,
//       designation :userDetails.designation,
//       priority:priority,
//       raise_time : formattedDate2
//      })
     
//    });
//    update_nickname(newnumber);
//     goto('/ticketing/Datareq/');
//  }


async function newform() { // For SAVE DATA REQ FORM DATA
    if (!requestcategory || !requesttype || (showSecondDropdown && !secondDropdownValue) || (showGprssDropdown && !newtype) || (showPoaDropdown && !showPoaDropdownvalue) || (showCdrDropdown && !newtype) || (showGprsDropdown && !newtype) || (showIpdrDropdown && !newtype) || (showRhDropdown && !newtype) ){
        // alert("Please fill in all required fields.");
    } else {
        try {
            const response = await fetch(basepath() + '/newform', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    // Your data payload here
                    update:update,
                    requestcategory:requestcategory,
                    requesttype:requesttype,
                    subtype:newtype,
                    date:formattedDate,
                    sdrdropdown:sdrdropdown,
                    phoneNumbers:phnumber,
                    Numbers:phoneNumbers,
                    team:userDetails.team,
                    modules:modules,
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
                    remarks:remarks,
                    officername: userDetails.officername,
                    useremail: userDetails.email,
                    superior: userDetails.superior,
                    role: userDetails.role,
                    newnumber:newnumber,
                    designation :userDetails.designation,
                    priority:priority,
                    raise_time : formattedDate2
                })
            });
            if (response.ok) {
                // Process successful response
                update_nickname(newnumber);
                goto('/ticketing/Datareq/');
                alert("successfully created");
            } else {
                // Handle unsuccessful response
                console.error('Failed to submit form:', response.statusText);
                alert('Failed to submit form. Please try again later.');
            }
        } catch (error) {
            // Handle fetch error
            console.error('Error while submitting form:', error);
            alert('Error while submitting form. Please try again later.');
        }
    }
}



 let proforma_data = [{
          phone: '',
          sdr: '',
          target_number: '',
          voip: '',
          sdb: '',
          FLSL: '',
          remarks: '',
          category: '',
        }];
  let analysis_type = '';
  let user_details = '';
  let note_refno = '';
  let summary1 = '';
  let summary2 = '';


 async function note_create(){
  for (let i = 0; i < proforma_data.length; i++) {
    if (!newnumber[i]) {
      newnumber[i] = {
                Phno: '',
              }
      }
    const data = proforma_data[i];
    newnumber[i]['Phno'] = data['phone'];
  }
  console.log(newnumber)
  const response = await fetch(basepath()+'/note_create', {
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
      team:userDetails.team,
      modules:modules,
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
      remarks:remarks,
      officername: userDetails.officername,
      useremail: userDetails.email,
      superior: userDetails.superior,
      role: userDetails.role,
      newnumber:newnumber,
      designation :userDetails.designation,
      priority:priority,
      raise_time : formattedDate2,

      refno:note_refno,
      type:analysis_type,
      user:user_details,
      date:formattedDate,
      officer : userDetails.officername,
      summary1 : summary1,
      summary2 : summary2,
      newnumber:newnumber,
      user:user_details,
      data : proforma_data
     })
  })
  goto('/ticketing/Analysisreq/');
  }
 let save = ''
 function note_save(){
  for (let i = 0; i < proforma_data.length; i++) {
    const data = proforma_data[i];
    if (data.phone === '' && data.sdr === '' && data.target_number === '' && analysis_type === '' && note_refno === ''){
      const toast = toasts.add({
      title: 'Input Error',
      description: `All fields are mandatory!`,
      duration: 10000,
      placement: 'top-center',
			showProgress: true,
      type: 'error',
      theme: 'dark',
      onClick: () => {},
      onRemove: () => {},
    });
    return;
    }
    else{
      save = 'Note Generated Successfully....!'
    }
  }
 }
  // Fetching CellID/Area/TowerNames using LAT LONG OR CGI with RAD
  async function cell_id_fetch(lat = '', long = '',i,rad = '') {
  try {
    const response = await fetch(basepath() + '/get_tower_by_radius', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        lat: lat,
        long:long,
        rad:rad,
        type:showCdrDropdownvalue,
        // cgi:cgi
      })
    });
    // console.log(cgi,"CGIIIIIIIIIIIIIIIIIIIII")
    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }
    
    const cases = await response.json();
    cell = cases;
  console.log(cell,"Cell_id");
    if (showCdrDropdownvalue === "Co-Ordinates" && lat){
    cellInput[lat] = cell.CELL_ID;
    newnumber[i]["Cell_id"] = (cellInput[lat] || '');
    newnumber[i]["Rad"] = (cell.RAD || '');
    newnumber[i]["AreaDescription"] = (cell.AreaDescription || '')
    newnumber[i]["Operator"] = (cell.Operator || '')
    newnumber[i]["State"] = (cell.State || '')
  }
    
  } catch (error) {
    console.error(error);
  }

  }


function close(){ 
  window.location.reload();
}

let columnNames = [];
let records = [];
let file;
let data;
function resetState() {   //Before Upload Any Excel File Need To clear all Previous Inputs and Veriabals
  newnumber = [
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
    ISP:[],
    Remarks:''
  }
];
    records = [];
    columnNames = [];
    const fileInput = document.getElementById('excel_file');
    fileInput.value = '';
    file = {}
    // console.log(file,"after changessssssssssssssssssss");
  }

  function onRequesttypeChange() {
    // Reset the state when Requesttype changes
    resetState();
  } 
  const handleFileUpload = async (event) => {  // Excel File Upload Handler
    file = event.target.files[0];  
    const formData = new FormData();
    console.log(file)
    formData.append('file', file);
    formData.append('category', requestcategory);
    formData.append('type', requesttype);
    formData.append('type2', requesttypes);
    formData.append('subtype', newtype);
    formData.append('time', formattedDate1);
    formData.append('team', `${userDetails.team}`);
    formData.append('modules', `${userDetails.modules}`);
    formData.append('officername', `${userDetails.officername}`);
    try {
      const response = await fetch(basepath()+'/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        console.log(result,'Backend Data');
        records = result[0].newnumber
        newnumber = result[0].newnumber
        if (requestcategory === 'Data Request'){
          columnNames = result[0].columns
        }
        else if (requestcategory === 'Analysis Request'){
          if(newtype === 'Phone'){
            columnNames = ['Phno','ISP','From_Date','To_Date']
          }
          else if(newtype === 'IMEI'){
            columnNames = ['IMEI','ISP','From_Date','To_Date']
          }
          else if(newtype === 'IPV6' || newtype === 'IPV4'){
            columnNames = ['IP_Address','From_Date','To_Date']
          }
          else if(newtype === 'CGI'){
            columnNames = ['CGI','From_Date','To_Date']
          }
          else if(newtype === 'Co-Ordinates'){
            columnNames = ['Latitude','Longitude','From_Date','To_Date']
          }
          else if(requesttypes.length === 1 && requesttypes.includes('RH') && newtype === 'Retailer/Dealer Details'){
            columnNames = ['RH_Dealer','RH_code','ISP','From_Date','To_Date']
          }
          else if(requesttypes.length === 1 && requesttypes.includes('POA') && newtype === 'Retailer/Dealer Details'){
            columnNames = ['POA_Dealer','POA_code','ISP','From_Date','To_Date']
          }
        }
        const others = result[0].others
        for (let i = 0; i < others.length; i++) {
          data = others[i];
          if (others.length > 0){
            newnumber[i]['Nickname'] = (data.module + "_" + data.nickname);
            priority = data.priority;
            source = data.source;
            module = data.module;
          }
        }
        for (let i = 0; i < records.length; i++) {  // Send Data From Excel file To particular Fns for Fetching Data
          const index = records[i];
          if (index.Phno){
            phone_match(index.Phno,i)
          }
          if (index.Latitude && index.Longitude){
            cell_id_fetch(index.Latitude,index.Longitude,i,index.Rad,'')
          }
          // if (index.CGI){
          //   cell_id_fetch("","",i,index.Radindex.CGI)
          // }
          if (index.IMEI){
            imei_convert(index.IMEI,i)
          }
        }
        console.log(records,'Processed Data');
      } else {
        const error = await response.json();
        alert(error.error)
        window.location.reload();
      }
    } catch (error) {
      console.error('Error during file upload:', error);
    }
  };

async function imei_convert(imei,i){
  const response = await fetch(basepath() + '/imei_convert', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        imei: imei,
        req:requesttype,
        req2:requesttypes,
        sub:newtype
      })
    });
    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }
    const cases = await response.json();
    cell = cases;
  console.log(cell);
  newnumber[i]["IMEI"] = (cell.IMEI || '');
  records[i]['IMEI'] = (cell.IMEI || '');
    console.log(newnumber[i]["IMEI"]);
  }


let showSecondDropdown = false;
let showCdrDropdown = false;
let showIpdrDropdown = false;
let showGprsDropdown = false;
let showPoaDropdown = false;
let showRhDropdown = false;
let showGprssDropdown = false;


function handleFirstDropdownChange() { // For handling Submenu dropdowns from Differ. Request Types
  onRequesttypeChange()
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
  if (requesttype !== 'POA') {
    showPoaDropdown = false;
  } else {
    showPoaDropdown = true;
  }
  if (requesttype !== 'RH') {
    showRhDropdown = false;
  } else {
    showRhDropdown = true;
  }
  

}
onMount(() => {
  // Call handleFirstDropdownChange initially to set the initial value of showSecondDropdown
  handleFirstDropdownChange();
});


function handleInputs(event, index,type) { //Handle All Inputs
  if (type === "Phno"){
    phone_match(newnumber[index][type],index);
    // handleNicknameInput(event,newnumber[index][type]);
  }
  if (type === 'Latitude') {
    newnumber[index].Latitude = event.target.value;
  } else if (type === 'Longitude') {
    newnumber[index].Longitude = event.target.value;
  } else if (type === 'Rad') {
    newnumber[index].Rad = event.target.value;
  }
  // Check if both latitude and longitude are available in the array and then call cell_id_fetch
  if (newnumber[index].Latitude !== undefined && newnumber[index].Longitude !== undefined && newnumber[index].Latitude !== '' && newnumber[index].Longitude !== '') {
    cell_id_fetch(newnumber[index].Latitude, newnumber[index].Longitude, index,newnumber[index].Rad);
    // handlecellInput(newnumber[index].Latitude);
  }
  if (type === 'CGI') {
    newnumber[index][type] = event.target.value;
  } else if (type === 'Rad') {
    newnumber[index].Rad = event.target.value;
  }
  if (newnumber[index].CGI !== undefined && newnumber[index].Rad !== undefined && newnumber[index].CGI !== '' && newnumber[index].Rad !== '' ) {
    cell_id_fetch(newnumber[index].Latitude, newnumber[index].Longitude, index,newnumber[index].Rad,newnumber[index].CGI);
    // handlecellInput(newnumber[index].CGI);
  }
  newnumber[index][type] = event.target.value;  
}

function handleInput() {
  if (requesttype === "IMEI CDR" || requesttype=== "IPDR" && secondDropdownValue === "IMEI" || requesttype==="GPRS" &&showGprssDropdownvalue === "IMEI"){
      newnumber = [...newnumber, { IMEI: '' ,ISP:'',From_Date: '' ,From_Date: '' }];
      }
      else{
        newnumber = [...newnumber, { Phno: '' ,From_Date: '' ,To_Date: '' }];

      }
    }
      // newinput = [...{"Phno": }]
function handlelatlong() {

  if(requesttype=== "TOWER CDR" && showCdrDropdownvalue === "Co-Ordinates" || requesttype=== "TOWER GPRS" && showCdrDropdownvalue === "Co-Ordinates" || requesttype=== "TOWER IPDR" && showCdrDropdownvalue === "Co-Ordinates" ){
    newnumber = [...newnumber, { Latitude: '' ,Longitude: '',From_Date: '',From_Date: ''}];
        
} else  {
  newnumber = [...newnumber, { Phno: '' ,From_Date: '' ,From_Date: '' }];
  
}
}
function remove(i) {
  newnumber = newnumber.slice(0, i).concat(newnumber.slice(i + 1));
}

function remove2(i) {
  proforma_data = proforma_data.slice(0, i).concat(proforma_data.slice(i + 1));

}
function handleInput2() {
  proforma_data = [...proforma_data, { phone: '' ,sdr: '' ,target_number: '' ,voip:'',sdb:'',FLSL:'',remarks:'',category:''}];
    }
function for_caf(){
  if(requesttype ==="CAF"){
  newnumber = [...newnumber, { Phno: '' ,CAF:''}];
}else if (requesttype === "SDR" && (sdrdropdown === "SDR" || sdrdropdown === "SDR HISTORY") || requesttype === "ISD"){
  newnumber = [...newnumber, { Phno: ''}];
}
else if (requesttype ==="CAF/CDR") {
  newnumber = [...newnumber, { Phno: '' ,CAF:'',From_Date: '' ,From_Date: '' }];
}
}
function removelatlong(i) {
  newnumber = newnumber.slice(0, i).concat(newnumber.slice(i + 1));

}

let showDropdown1 = false;

  function toggleDropdown(i) {
    newnumber[i]['showDropdown'] = ! newnumber[i]['showDropdown'];
  }
  function toggleDropdown1() {
    showDropdown1 = !showDropdown1;
  }



  function clearCheckboxes1(i) {
    newnumber[i]['ISP'] = [];
    // console.log("requesttypes_updated: ", requesttypes)
    const checkboxes1 = document.querySelectorAll('.check2');
    checkboxes1.forEach((checkbox1) => {
      checkbox1.checked = false;

    });
  console.log(newnumber[i]['ISP']);

  }
  function selectallCheckboxes1(i) {
  const types = ['Jio', 'Airtel', 'Vodafone', 'Cellone'];
  newnumber[i]['ISP'] = types.join(',');
  // console.log("requesttypes_updated_new: ", requesttypes)

  const checkboxes = document.querySelectorAll('.check2');
  checkboxes.forEach((checkbox1) => {
    checkbox1.checked = true;
  });
  console.log(newnumber[i]['ISP']);
}

function updateSelectedCount(i, value) {
  // Ensure that newnumber[i]['ISP'] is initialized as a string
  if (typeof newnumber[i]['ISP'] !== 'string') {
    newnumber[i]['ISP'] = '';
  }

  // Toggle the selected state of the provider
  const selectedProviders = newnumber[i]['ISP'].split(',');
  const selectedIndex = selectedProviders.indexOf(value);

  if (selectedIndex === -1) {
    // Provider is not selected, add it to the string
    if (newnumber[i]['ISP'].length > 0) {
      newnumber[i]['ISP'] += ',' + value;
    } else {
      newnumber[i]['ISP'] = value;
    }
  } else {
    // Provider is selected, remove it from the string
    selectedProviders.splice(selectedIndex, 1);
    newnumber[i]['ISP'] = selectedProviders.join(',');
  }

  // Do other necessary updates based on selectedProviders
  console.log(newnumber[i]['ISP']);
}


  function updateSelectedCount1() {
    const selectedCheckboxes = Array.from(document.querySelectorAll('.check1:checked')).map(checkbox => checkbox.value);
    requesttypes = selectedCheckboxes;
    // console.log("requesttypes: ", requesttypes)

  }
  function clearCheckboxes() {
    requesttypes = [];
    // console.log("requesttypes_updated: ", requesttypes)
    const checkboxes1 = document.querySelectorAll('.check1');
    checkboxes1.forEach((checkbox1) => {
      checkbox1.checked = false;
    });
  }
  let types = [
    "CAF",
    "SDR",
    "CDR",
    "GPRS",
    "IPDR",
    "RH",
    "POA",
    "TOWER DATA"
  ];
  function selectallCheckboxes() {
    requesttypes = types;
    // console.log("requesttypes_updated_new: ", requesttypes)

    const checkboxes = document.querySelectorAll('.check1');
    checkboxes.forEach((checkbox1) => {
      checkbox1.checked = true;
    });
  }
  function handleClickOutside(event) {
    newnumber.forEach((item, index) => {
      if (item.showDropdown) {
        const dropdown = document.getElementById(`dropdown-${index}`);
        if (!dropdown.contains(event.target)) {
          item.showDropdown = false;
        }
      }
    });
    if (showDropdown1 && !event.target.closest('.dropdown')) {
      showDropdown1 = false;
    }
  }

  // Function to clear all checkboxes
 

  // Add a click event listener to the window to handle clicks outside the dropdown

  onMount(() => {
    window.addEventListener('click', handleClickOutside);

    // Clean up the event listener when the component is unmounted
    return () => {
      window.removeEventListener('click', handleClickOutside);
    };
  });

  
let ref_nos = [];
async function fetch_ref(){
  const response = await fetch(basepath() + '/fetch_ref', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ 
      email: userDetails.email,
      name : userDetails.officername,
      team: userDetails.team
    })
  });
  if (response.ok){
    cases = await response.json();
    // console.log(cases,'===================================')
    ref_nos = cases.filter((user) => user.useremail === userDetails.email && user.requestcategory === 'Analysis Request')
    // console.log(ref_nos,'/////////////////////////////')
  }
}

onMount(() => {
  // Call handleFirstDropdownChange initially to set the initial value of showSecondDropdown
  fetch_ref();
});



let search_ref = [];
let refs = '';
function fetch_ref_2(){
  search_ref = ref_nos.filter((user) => user.refno === refs)
  console.log(search_ref)
  refno = refs;
  refdate = search_ref[0]['refdate'];
  requesttypes = (search_ref[0]['requesttypes'] || '');
  secondDropdownValue = (search_ref[0]['subtypes'] || '');
  newnumber = (search_ref[0]['newnumber'] || '');


  const imei = search_ref[0]['newnumber'];
  if (search_ref[0]['requesttypes'].includes( 'IMEI')){
    for (let i = 0; i < imei.length; i++) {
      const data = imei[i];
      // console.log(data.IMEI)
      imei_convert(data.IMEI,i)
    }
  }
}




async function ref_no(){
  const response = await fetch(basepath() + '/ref_no', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        team: `${userDetails.team}`,
        modules : `${userDetails.modules}`,
        request: requestcategory,
        refno:refno
      })
    });
    if (response.ok){
    cases = await response.json();
    refno = cases.new_ref;
    // console.log(cases,'===================================')
  }
}
function resizeTextarea(event) {
    const textarea = event.target;
    textarea.style.height = "44px";
    textarea.style.height = `${textarea.scrollHeight}px`;
  }
  
  
  </script>
  
  <style>
    label{
      font-family: 'Times New Roman', Times, serif;
    }
    input,select,textarea{
      border:none;
      border-radius: 5px !important;
      background-color: rgb(255, 255, 255);
      border-bottom:1px solid black !important;
     box-shadow: 0 .5rem 1rem rgba(0, 0, 0, 0.486)!important;    
  
    }
    main{
    background-color: aliceblue;
    width: auto;
    height: auto;
    }
  h3 {
    
      font-weight: bold;
      color: white;
  }
  
  .second_dd{
    margin-left:20px;
  }
  form{
     box-shadow: 0 .5rem 1rem rgb(0, 0, 0)!important;    
     background:linear-gradient(120deg, white, white);
     border-radius: 10px;
    margin-bottom: 50px;
  }
  a{
    text-decoration: none;
  }
  #flex-container {
    display: flex;
    justify-content: center;
  
    margin-left: -50px;
    /* max-height: 20em;
    overflow-y: scroll; */
  }
  #flex-container1{
    display: flex;
    justify-content: center;
    margin-left: 90px;
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
  .flex-item_22 {
    width: 350px;
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
    margin-left: -140px;
    
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

    .refno{
      width: 200px;
    }
    .reciever {
      margin-top: 21px;
      margin-bottom: 76px;
      margin-left: 50px;
    }
    .form-control{
      background-color: transparent !important;
      border: none;
    }
    .tophead{
      margin-right: 190px;
      padding: 30px;
      margin-top: -34px;
      font-family: 'Times New Roman', Times, serif;
      font-size: 25px;
      font-style:oblique;
    }
    main{
      font-family: 'Times New Roman', Times, serif;
    }
    .Analysis-input{
      background: transparent !important;
      height: 40px;
      width:350px;
      margin-top: -5px;
      margin-left: 30px;
      margin-bottom: 20px;
    }
    .table-container {
      display: flex;
      width: 1721px;
      margin-left: -304px;
      margin-right: 20px;
      margin-top: 50px;
    }
    .textarea{
      height: 44px;
    }
    .textarea1{
      height: 140px;
    }
    .tophead{
      margin-right: 190px;
      padding: 30px;
      margin-top: -25px;
      font-family: 'Times New Roman', Times, serif;
      font-size: 25px;
      font-style:oblique;
    }

    .form-header {
    display: flex;
    margin-top: -10px;
    justify-content: space-between;
  }

  .left-header {
    flex: 1;
  }
  .right-header {
    flex: 1;
    text-align: right;
  }

  .form-footer {
    display: flex;
    padding: 50px;
    justify-content: center;
    margin-top: 190px;
  }
  .sign1 {
    margin-top: -129px !important;
  }
  
  </style>
  <main>
    <head>
  
    </head>
  <nav class="navbar navbar-dark bg-dark" style="background-color: #343a40!important;">
    <div class="">
    </div>
      {#if requestcategory !== ""}
      <h3>{requestcategory}</h3>
      {:else}
      <h3>New Request Form</h3>
      {/if}
      <div></div>
  </nav>
  <br>
  <br>
  <!-- <section> -->
    <div style='width:70% !important; margin-left:250px'>
      <div class="row">
        <form action="" class="p-5">
          <div class='d-flex justify-content-end' style='margin-top:-20px;margin-bottom:25px;'>
            <button class='btn btn-primary' data-bs-toggle="tooltip" data-bs-placement="top" title='Download Sample Excel File For all Types' on:click={sample_excel}><i class="bi bi-file-earmark-spreadsheet-fill"></i> Sample Excel</button>
          </div>
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
        {#if userDetails.role === "Analyst" && userDetails.team === 'ISOT'}
          <select class="col-sm-4 ml-3" bind:value={isot_modules} >
            <option selected value="">Select Module</option>
            <option value="ISOT">ISOT</option>
            <option value="ISOT-M1">ISOT-M1</option>
            <option value="ISOT-M2">ISOT-M2</option>
            <option value="ISOT-M3">ISOT-M3</option>
          </select>
          {:else}
          <input class="col-sm-4 border-0" bind:value={userDetails.modules} readonly>
          {/if}
      </div>
        <div class="row mb-3">
          <label class="col-sm-3 col-form-label">REQUEST CATEGORY</label> 
          <select class="col-sm-4 border-0" bind:value={requestcategory} on:change={ref_no} required>
              <option selected value="">Select</option>
              <option value="Data Request">Data Request</option>
              <option value="Analysis Request">Analysis Request</option>
              <option value="Note">Note</option>
          </select>
      </div>
  {#if requestcategory === "Analysis Request"}
    <SelectDropdown label={"NEW/FURTHER ANALYSIS"} options={["Select Reason","NEW ANALYSIS","FURTHER ANALYSIS"]} display_func={o => o} bind:value={reason} required />
    {#if reason === "FURTHER ANALYSIS"}
        <div class="row mb-3">
        <label class="col-sm-3 col-form-label">REF Nos</label> 
        <select class="col-sm-4 border-0" style="margin-left: 2px !important;" bind:value={refs} display_func={o => o} on:change = {fetch_ref_2}>
          <option selected value="">Ref Nos. </option>
          {#each ref_nos as ref}
          <option value={ref.refno}>{ref.refno}</option>
         {/each}
        </select>
      </div>
      {#if refs !== ''}
        {#each search_ref as ref}
        <div class="row mb-3">
          <label class="col-sm-3 col-form-label" >REF NO - DATE</label> 
          <input class="col-sm-4 border-0" placeholder={refs} type="text" bind:value={refno}> 
          <select class="col-sm-2" style="margin-left: 10px !important;" display_func={o => o} bind:value={ref.refdate}>
            <option disabled value="">Ref Year </option>
                <option value="{year}">{year}</option>
              <option value="{year-1}">{year-1}</option>
              <option value="{year-2}">{year-2}</option>
              <option value="{year-3}">{year-3}</option>
          </select>
        </div>
        <div class="row mb-3">
          <label class="col-sm-3 col-form-label">REQUEST TYPE</label>
          <div class="show dropdown col-sm-4">
            <input type="text" class="form-control" placeholder="Select Request Type" readonly on:click={toggleDropdown1} value={requesttypes.join(', ')} required>
            <div class="dropdown-menu ml-2" style="{showDropdown1 ? 'display: block;' : 'display: none;'}; width:300px;margin-left: 0.5rem!important">
              <!-- <button type="button" class="clear btn btn-outline-danger ml-1" on:click={clearCheckboxes}><i class="bi bi-x-square"></i></button>
              <button type="button" class="clear btn btn-outline-success ml-1" on:click={selectallCheckboxes}><i class="bi bi-check2-square"></i></button><br> -->
              <input class="check1 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="ALL PARAMETERS" name="ALL PARAMETERS" value="ALL PARAMETERS" on:change={updateSelectedCount1}>
              <label style="display: inline-block;" for="ALL PARAMETERS">ALL PARAMETERS</label><br>
              <input class="check1 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="CAF" name="CAF" value="CAF" on:change={updateSelectedCount1}>
              <label style="display: inline-block;" for="CAF">CAF</label><br>
              <input class="check1 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="SDR" name="SDR" value="SDR" on:change={updateSelectedCount1}>
              <label style="display: inline-block;" for="SDR">SDR</label><br>
              <input class="check1 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="CDR" name="CDR" value="CDR" on:change={updateSelectedCount1}>
              <label style="display: inline-block;" for="CDR">CDR</label><br>
              <input  class="check1 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="IMEI" name="IMEI" value="IMEI" on:change={updateSelectedCount1}>
              <label style="display: inline-block;" for="IMEI">IMEI</label><br>
              <input class="check1 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="GPRS" name="GPRS" value="GPRS" on:change={updateSelectedCount1}>
              <label style="display: inline-block;" for="GPRS">GPRS</label><br>
              <input class="check1 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="IPDR" name="IPDR" value="IPDR" on:change={updateSelectedCount1}>
              <label style="display: inline-block;" for="IPDR">IPDR</label><br>
              <input class="check1 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="RH" name="RH" value="RH" on:change={updateSelectedCount1}>
              <label style="display: inline-block;" for="RH">RH</label><br>
              <input class="check1 ml-2" style="margin-left: 0.5rem!important"  type="checkbox" id="POA" name="POA" value="POA" on:change={updateSelectedCount1}>
              <label style="display: inline-block;" for="POA">POA</label><br>
              <input class="check1 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="TOWER DATA" name="TOWER DATA" value="TOWER DATA" on:change={updateSelectedCount1}>
              <label style="display: inline-block;" for="TOWER DATA">TOWER DATA</label><br>
            </div>
          </div>
          {#if requesttypes.length !== 0}
          <select class="col-sm-2 ml-1" style="margin-left: 10px !important;" bind:value={secondDropdownValue} required>
          <option value="">Select </option>
          {#if requesttypes.length === 1 && requesttypes.includes("CDR") || requesttypes.length === 1 && requesttypes.includes("CAF") || requesttypes.length === 1 && requesttypes.includes("SDR")}
          <option value="Phone">Phone</option>
          <!-- <option value="IMEI">IMEI</option> -->
          {:else if requesttypes.length === 1 && requesttypes.includes("IMEI")}
          <option value="IMEI">IMEI</option>
          <option value="Phone">Phone</option>
          {:else if requesttypes.length === 1 && requesttypes.includes("IPDR")}
          <option value="IPV6">IPV6</option>
          <option value="IPV4">IPV4</option>
          <option value="Phone">Phone</option>
          <option value="IMEI">IMEI</option>
          {:else if requesttypes.length === 1 && requesttypes.includes("GPRS") || requesttypes.length === 2 && requesttypes.includes("GPRS" && "IPDR")}
          <option value="Phone">Phone</option>
          <option value="IMEI">IMEI</option>
          {:else if requesttypes.length === 1 && requesttypes.includes("TOWER DATA")}
          <option value="CGI">CGI (Cell ID)</option>
          <option value="Phone">Phone</option>
          <option value="Co-Ordinates">Co-Ordinates</option>
          <!-- <option value="Area">Area</option>
          <option value="Tower Name">Tower Name</option>   -->
          {:else if requesttypes.length === 1 && requesttypes.includes("RH") || requesttypes.length === 1 && requesttypes.includes("POA") || requesttypes.length === 2 && requesttypes.includes("POA" && "RH")}
          <option value="Phone">Phone</option>
          <option value="Retailer/Dealer Details">Retailer/Dealer Details</option>
          {:else if requesttypes.length === 1 && requesttypes.includes("ALL PARAMETERS")}
          <option value="Phone">Phone</option>
          <option value="IMEI">IMEI</option>
          {/if}
          </select>
          {/if}
        </div>
        <div class="row mb-3">
          <div class="col-3">
            <label for="input3">ENTER INPUTS</label>
          </div>
          {#if records.length === 0}
          {#if requesttypes.length !== 0 && secondDropdownValue === "Phone" && !requesttypes.includes("IMEI")}
                  <div id="flex-container1">
                    <div class="flex-item">
                      {#each newnumber as newno, index}
                        <div class="input-group mb-1 border-0">
                          <input class="form-control" bind:value={newno.Phno} placeholder="Enter Phone" 
                            aria-label="enter phone number" aria-describedby="button-addon2"  tabindex={index}
                            on:input={(event) => handleInputs(event, index, "Phno")} 
                            maxlength="10"
                      on:input={() => {
                       if (!/^[0-9]*$/.test(newno.Phno)) {
                        newno.Phno = newno.Phno.replace(/[^0-9]/g, ''); // Remove non-digit characters
                          }
                        }}>
                        </div>
                      {/each}
                    </div> 
                    <div class="flex-item">
                      <!-- From Dates Section -->
                      {#each newnumber as newno, index}
                        <div class="input-group border-0">
                          <div class="dropdown" id={`dropdown-${index}`}>
                            <input type="text" class="form-control" style='margin-top:2px' placeholder="Select Providers" readonly on:click={()=> toggleDropdown(index)} bind:value={newno.ISP}>
                            <div class="dropdown-menu ml-3" style="{newno.showDropdown ? 'display: block;' : 'display: none; margin-left: 0.5rem!important'}">
                              <button type="button" class="clear btn btn-outline-danger ml-1" on:click={()=> clearCheckboxes1(index)}><i class="bi bi-x-square"></i></button>
                              <button type="button" class="clear btn btn-outline-success ml-1" on:click={()=> selectallCheckboxes1(index)}><i class="bi bi-check2-square"></i></button><br>                    
                              <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Jio" name="provider[]" value="Jio" on:change={()=> updateSelectedCount(index, 'Jio')}>
                              <label style="display: inline-block;" for="provider_Jio">Jio</label><br>
                              <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Airtel" name="provider[]" value="Airtel" on:change={()=> updateSelectedCount(index, 'Airtel')}>
                              <label style="display: inline-block;" for="provider_Airtel">Airtel</label><br>
                              <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_VI" name="provider[]" value="Vodafone" on:change={()=> updateSelectedCount(index,'Vodafone')}>
                              <label style="display: inline-block;" for="provider_VI">Vodafone</label><br>
                              <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_CO" name="provider[]" value="Cellone" on:change={()=> updateSelectedCount(index,'Cellone')}>
                              <label style="display: inline-block;" for="provider_CO">Cellone</label><br>
                            </div>
                          </div>
                        </div>
                      {/each}
                    </div>
              <div class="flex-item">
                <!-- From Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.From_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                  </div>
                {/each}
              </div>
              <div class="flex-item">
                <!-- To Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.To_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',defaultDate: "today"}} placeholder="Select To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                    {#if newnumber.length > 1}
                    <button class="btn btn-danger" on:click={() => removelatlong(index)}>-</button>
                    {/if}
                    {#if index === newnumber.length - 1}
                    <button class="btn btn-primary" id="button-addon2" on:click={handlelatlong}>+</button>
                    <!-- <button class="btn btn-warning" id="button-addon2" on:click={phone_match(newno.Phno)}>Check</button> -->
                    {/if}
                  </div>
                {/each}
               </div>
              </div>
              {/if}
        {#if requesttypes.length === 1 && requesttypes.includes("GPRS")  || requesttypes.length === 1 && requesttypes.includes("IPDR") || requesttypes.length === 2 && requesttypes.includes("GPRS" && "IPDR")}
                  <!-- Phone Numbers Section -->
                  {#if requesttypes.includes("IPDR") && secondDropdownValue === "IPV6" || requesttypes.includes("IPDR") && secondDropdownValue === "IPV4"}
                  <div id="flex-container">
                    <div class="flex-item">    
                  {#each newnumber as newno, index}
                    <div class="input-group mb-1 border-0">
                      {#if requesttypes.includes("IPDR") && secondDropdownValue === "IPV6"}
                      <input class="form-control" bind:value={newno.IPV6} tabindex={index} placeholder="enter IPV6" 
                      aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"IP_Address")}>
                      {:else if requesttypes.includes("IPDR") && secondDropdownValue === "IPV4"}
                      <input class="form-control" bind:value={newno.IPV4} tabindex={index} placeholder="enter IPV4" 
                      aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"IPV4")}>
                      {:else}
                      <input class="form-control" bind:value={newno.Phno} tabindex={index} placeholder="enter Phone." 
                      aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"Phno")} maxlength="10"
                      on:input={() => {
                       if (!/^[0-9]*$/.test(newno.Phno)) {
                        newno.Phno = newno.Phno.replace(/[^0-9]/g, ''); // Remove non-digit characters
                          }
                        }}>
                      {#if newno.Phno.length <10}
                          <p style="color: red;font-weight:bold">Enter 10 Digits Only</p>
                          {/if}
                      {/if}
                    </div>
                  {/each}
                  </div>
                  <div class="flex-item">
                    <!-- From Dates Section -->
                    {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.From_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y H:i",minDate: mindate,maxDate: 'today', enableTime : true}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                      </div>
                    {/each}
                  </div>
                  <div class="flex-item">
                    <!-- To Dates Section -->
                    {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.To_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y H:i",minDate: mindate,maxDate: 'today', enableTime: true,defaultDate: "today"}} placeholder="Select To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                        {#if newnumber.length > 1}
                        <button class="btn btn-danger" on:click={() => remove(index)}>-</button>
                        {/if}
                        {#if index === newnumber.length - 1}
                        <button class="btn btn-primary" id="button-addon2" on:click={handleInput}>+</button>
                        {/if}
                      </div>
                    {/each}
                  </div>
                  </div>
                  {/if}            
                  {#if requesttypes.includes("IPDR") && secondDropdownValue === "IMEI" || requesttypes.includes("GPRS")  && secondDropdownValue === "IMEI"}
                  <div id="flex-container">
                    <div class="flex-item">    
                  {#each newnumber as newno, index}
                    <div class="input-group mb-1 border-0">
                      <input class="form-control" bind:value={newno.IMEI} tabindex={index} placeholder="enter IMEI" 
                      aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"IMEI")} on:input={() => {
                        if (!/^[0-9]*$/.test(newno.IMEI)) {
                         newno.IMEI = newno.IMEI.replace(/[^0-9]/g, ''); // Remove non-digit characters
                           }
                         }}
                      maxlength="15">
                    </div>
                  {/each}
                  </div>
                  <div class="flex-item">
                    <!-- From Dates Section -->
                    {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.From_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y H:i",minDate: mindate,maxDate: 'today', enableTime : true}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                      </div>
                    {/each}
                  </div>
                  <div class="flex-item">
                    <!-- To Dates Section -->
                    {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.To_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y H:i",minDate: mindate,maxDate: 'today', enableTime: true,defaultDate: "today"}} placeholder="Select To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                        {#if newnumber.length > 1}
                        <button class="btn btn-danger" on:click={() => remove(index)}>-</button>
                        {/if}
                        {#if index === newnumber.length - 1}
                        <button class="btn btn-primary" id="button-addon2" on:click={handleInput}>+</button>
                        {/if}
                      </div>
                    {/each}
                  </div>
                  </div>
                  {/if}
              {/if}
              
              {#if requesttypes.includes("IMEI") && secondDropdownValue === "IMEI" || requesttypes.includes("IMEI") && secondDropdownValue === "Phone" }
              <div id="flex-container1">
                {#if secondDropdownValue === 'IMEI'}
                <div class="flex-item">    
              {#each newnumber as newno, index}
                <div class="input-group mb-1 border-0">
                  <input class="form-control" bind:value={newno.IMEI} tabindex={index} placeholder="enter IMEI"
                  aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"IMEI")} on:input={() => {
                    if (!/^[0-9]*$/.test(newno.IMEI)) {
                     newno.IMEI = newno.IMEI.replace(/[^0-9]/g, ''); // Remove non-digit characters
                       }
                     }}
                  maxlength="15">
                </div>
              {/each}
              </div>
              {:else}
              <div class="flex-item">
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.Phno} tabindex={index} placeholder="Enter Phone" 
                      aria-label="enter phone number" aria-describedby="button-addon2" 
                      on:input={(event) => handleInputs(event, index, "Phno")} 
                      maxlength="10"
                on:input={() => {
                 if (!/^[0-9]*$/.test(newno.Phno)) {
                  newno.Phno = newno.Phno.replace(/[^0-9]/g, ''); // Remove non-digit characters
                    }
                  }}>
                  </div>
                  {#if newno.Phno.length <10}
                  <p style="color: red;font-weight:bold">Enter 10 Digits Only</p>
                  {/if}
                {/each}
              </div> 
              {/if}
              <div class="flex-item">
                <!-- From Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group border-0">
                    <div class="dropdown" id={`dropdown-${index}`}>
                      <input type="text" class="form-control" style='margin-top:2px' placeholder="Select Providers" readonly on:click={()=> toggleDropdown(index)} bind:value={newno.ISP}>
                      <div class="dropdown-menu ml-3" style="{newno.showDropdown ? 'display: block;' : 'display: none; margin-left: 0.5rem!important'}">
                        <button type="button" class="clear btn btn-outline-danger ml-1" on:click={()=> clearCheckboxes1(index)}><i class="bi bi-x-square"></i></button>
                        <button type="button" class="clear btn btn-outline-success ml-1" on:click={()=> selectallCheckboxes1(index)}><i class="bi bi-check2-square"></i></button><br>       
                        <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Jio" name="provider[]" value="Jio" on:change={()=> updateSelectedCount(index, 'Jio')}>
                        <label style="display: inline-block;" for="provider_Jio">Jio</label><br>
                        <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Airtel" name="provider[]" value="Airtel" on:change={()=> updateSelectedCount(index, 'Airtel')}>
                        <label style="display: inline-block;" for="provider_Airtel">Airtel</label><br>
                        <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_VI" name="provider[]" value="Vodafone" on:change={()=> updateSelectedCount(index,'Vodafone')}>
                        <label style="display: inline-block;" for="provider_VI">Vodafone</label><br>
                        <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_CO" name="provider[]" value="Cellone" on:change={()=> updateSelectedCount(index,'Cellone')}>
                        <label style="display: inline-block;" for="provider_CO">Cellone</label><br>
                      </div>
                    </div>
                  </div>
                {/each}
              </div>
              <div class="flex-item">
                <!-- From Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.From_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today'}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                  </div>
                {/each}
              </div>
              <div class="flex-item">
                <!-- To Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.To_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',defaultDate: "today"}} placeholder="Select To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                    {#if newnumber.length > 1}
                    <button class="btn btn-danger" on:click={() => remove(index)}>-</button>
                    {/if}
                    {#if index === newnumber.length - 1}
                    <button class="btn btn-primary" id="button-addon2" on:click={handleInput}>+</button>
                    {/if}
                  </div>
                {/each}
              </div>
              </div>
              {/if}
      
              {#if requesttypes.length === 1 && requesttypes.includes("TOWER DATA") && secondDropdownValue === "Co-Ordinates" }
              <div id="flex-container2">
                <div class="flex-item">
              {#each newnumber as newno, index}
              <div class="input-group mb-1 border-0">
                <input
                  class="form-control"
                  bind:value={newno.Latitude}
                  placeholder="Enter Lat*"
                  aria-label="Enter Latitude" tabindex={index}
                  aria-describedby="button-addon2"
                  on:input={(event) => handleInputs(event, index,"Latitude")}
                />
              </div>
              {/each}
                </div>
                <div class="flex-item">
                  {#each newnumber as newno, index}
                  
                  <div class="input-group mb-1 border-0">
                <input
                  class="form-control"
                  bind:value={newno.Longitude}
                  placeholder="Enter Long*" tabindex={index}
                  aria-label="Enter Area Name/Co-Ordinates"
                  aria-describedby="button-addon2"
                  on:input={(event) => handleInputs(event, index,"Longitude")}
                />
              </div>
              {/each}
              </div>
              
              
              <div class="flex-item">
                <!-- From Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.From_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate, maxDate: 'today'}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                  </div>
                {/each}
              </div>
              <div class="flex-item">
                <!-- To Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.To_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate, maxDate: 'today',defaultDate: "today"}} placeholder="Select To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                    {#if newnumber.length > 1}
                    <button class="btn btn-danger" on:click={() => removelatlong(index)}>-</button>
                    {/if}
                    {#if index === newnumber.length - 1}
                    <button class="btn btn-primary" id="button-addon2" on:click={handlelatlong}>+</button>
                    {/if}
                  </div>
                {/each}
              </div>
              </div>
              {/if}
      
      
      <!-- CGI ID -->
      
            {#if requesttypes.length === 1 && requesttypes.includes("TOWER DATA") && secondDropdownValue === "CGI"}
                <div id="flex-container">
                  <div class="flex-item">    
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.CGI} tabindex={index} placeholder="Enter CGI ID" 
                    aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"CGI")}/>
                  </div>
                {/each}
                </div>
              <div class="flex-item">
                <!-- From Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.From_Date} tabindex={index}  use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today'}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                  </div>
                {/each}
              </div>
              <div class="flex-item">
                <!-- To Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.To_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',defaultDate: "today"}} placeholder="Select To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                    {#if newnumber.length > 1}
                    <button class="btn btn-danger" on:click={() => removelatlong(index)}>-</button>
                    {/if}
                    {#if index === newnumber.length - 1}
                    <button class="btn btn-primary" id="button-addon2" on:click={handlelatlong}>+</button>
                    {/if}
                  </div>
                {/each}
              </div>
              </div>
              {/if}
        {/if}
        {#if requesttypes.length === 1 && requesttypes.includes("RH") && secondDropdownValue === "Retailer/Dealer Details" || requesttypes.length === 1 && requesttypes.includes("POA") && secondDropdownValue === "Retailer/Dealer Details"}
                {#if requesttypes.length === 1 && requesttypes.includes("RH") && secondDropdownValue === "Retailer/Dealer Details"}
                <div id="flex-container1">
                  <div class="flex-item">    
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.RH_Dealer} placeholder="Dealer Details**" 
                    aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"RH_Dealer")}>
                  </div>
                {/each}
                </div>
                <div class="flex-item" style="width: 120px;">    
                  {#each newnumber as newno, index}
                    <div class="input-group mb-1 border-0">
                      <input class="form-control" bind:value={newno.RH_code} placeholder="Dealer code" 
                      aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"RH_code")}>
                    </div>
                  {/each}
                  </div>
                  <div class="flex-item">
                    <!-- From Dates Section -->
                    {#each newnumber as newno, index}
                      <div class="input-group border-0">
                        <div class="dropdown" id={`dropdown-${index}`}>
                          <input type="text" class="form-control" style='margin-top:2px' placeholder="Select Providers" readonly on:click={()=> toggleDropdown(index)} bind:value={newno.ISP}>
                          <div class="dropdown-menu ml-3" style="{newno.showDropdown ? 'display: block;' : 'display: none; margin-left: 0.5rem!important'}">
                            <button type="button" class="clear btn btn-outline-danger ml-1" on:click={()=> clearCheckboxes1(index)}><i class="bi bi-x-square"></i></button>
                              <button type="button" class="clear btn btn-outline-success ml-1" on:click={()=> selectallCheckboxes1(index)}><i class="bi bi-check2-square"></i></button><br>       
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Jio" name="provider[]" value="Jio" on:change={()=> updateSelectedCount(index, 'Jio')}>
                            <label style="display: inline-block;" for="provider_Jio">Jio</label><br>
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Airtel" name="provider[]" value="Airtel" on:change={()=> updateSelectedCount(index, 'Airtel')}>
                            <label style="display: inline-block;" for="provider_Airtel">Airtel</label><br>
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_VI" name="provider[]" value="Vodafone" on:change={()=> updateSelectedCount(index,'Vodafone')}>
                            <label style="display: inline-block;" for="provider_VI">Vodafone</label><br>
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_CO" name="provider[]" value="Cellone" on:change={()=> updateSelectedCount(index,'Cellone')}>
                            <label style="display: inline-block;" for="provider_CO">Cellone</label><br>
                          </div>
                        </div>
                      </div>
                    {/each}
                  </div>
              <div class="flex-item"  style="width: 140px;">
                <!-- From Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.From_Date} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                  </div>
                {/each}
              </div>
              <div class="flex-item"  style="width: 140px;">
                <!-- To Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.To_Date} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',defaultDate: "today"}} placeholder="To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                    {#if newnumber.length > 1}
                    <button class="btn btn-danger" on:click={() => removelatlong(index)}>-</button>
                    {/if}
                    {#if index === newnumber.length - 1}
                    <button class="btn btn-primary" id="button-addon2" on:click={handlelatlong}>+</button>
                    {/if}
                  </div>
                {/each}
              </div>
              </div>
              {/if}
              {#if requesttypes.length === 1 && requesttypes.includes("POA") && secondDropdownValue === "Retailer/Dealer Details"}
              
              <div id="flex-container1">
                <div class="flex-item">    
                  {#each newnumber as newno, index}
                    <div class="input-group mb-1 border-0">
                      <input class="form-control" bind:value={newno.POA_Dealer} placeholder="Dealer Details**" 
                      aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"POA_Dealer")}>
                    </div>
                  {/each}
                  </div>
                  <div class="flex-item" style="width: 120px;">    
                    {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.POA_code} placeholder="Dealer code" 
                        aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"POA_code")}>
                      </div>
                    {/each}
                    </div>
                    <div class="flex-item">
                      <!-- From Dates Section -->
                      {#each newnumber as newno, index}
                        <div class="input-group border-0">
                          <div class="dropdown" id={`dropdown-${index}`}>
                            <input type="text" class="form-control" style='margin-top:2px' placeholder="Select Providers" readonly on:click={()=> toggleDropdown(index)} bind:value={newno.ISP}>
                            <div class="dropdown-menu ml-3" style="{newno.showDropdown ? 'display: block;' : 'display: none; margin-left: 0.5rem!important'}">
                              <button type="button" class="clear btn btn-outline-danger ml-1" on:click={()=> clearCheckboxes1(index)}><i class="bi bi-x-square"></i></button>
                              <button type="button" class="clear btn btn-outline-success ml-1" on:click={()=> selectallCheckboxes1(index)}><i class="bi bi-check2-square"></i></button><br>       
                              <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Jio" name="provider[]" value="Jio" on:change={()=> updateSelectedCount(index, 'Jio')}>
                              <label style="display: inline-block;" for="provider_Jio">Jio</label><br>
                              <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Airtel" name="provider[]" value="Airtel" on:change={()=> updateSelectedCount(index, 'Airtel')}>
                              <label style="display: inline-block;" for="provider_Airtel">Airtel</label><br>
                              <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_VI" name="provider[]" value="Vodafone" on:change={()=> updateSelectedCount(index,'Vodafone')}>
                              <label style="display: inline-block;" for="provider_VI">Vodafone</label><br>
                              <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_CO" name="provider[]" value="Cellone" on:change={()=> updateSelectedCount(index,'Cellone')}>
                              <label style="display: inline-block;" for="provider_CO">Cellone</label><br>
                            </div>
                          </div>
                        </div>
                      {/each}
                    </div>
              <div class="flex-item" style="width: 140px;">
                <!-- From Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.From_Date} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                  </div>
                {/each}
              </div>
              <div class="flex-item" style="width: 140px;">
                <!-- To Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.To_Date} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',defaultDate: "today"}} placeholder="Select To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                    {#if newnumber.length > 1}
                    <button class="btn btn-danger" on:click={() => removelatlong(index)}>-</button>
                    {/if}
                    {#if index === newnumber.length - 1}
                    <button class="btn btn-primary" id="button-addon2" on:click={handlelatlong}>+</button>
                    {/if}
                  </div>
                {/each}
              </div>
              </div>
              {/if}
        {/if}
        {#if records.length > 0}
        <div class="col-auto scroll-table">
          <table class="table table-bordered">
               <tr>
                 {#each columnNames as columnName}
                 <th>{columnName}</th>
                   
                 {/each}
                </tr>
                {#each records as record}
                
                   <tr>
                     {#each columnNames as columnName}
                     <td>{record[columnName]}</td>
                     
                     {/each}
                    </tr>
                    
                    {/each}
                  </table>
           </div>
           {/if}
           <div class="uni">
          <input type="file" accept=".csv,.xlsx, .xls" on:change={handleFileUpload} id="excel_file"/>
          {#if records.length > 0}
          <p class="ml-2 mb-2" style = "color:green;">File Uploaded......</p>
      {/if}
          </div>
        </div>
      {/each}
      {/if}
  {:else}
        <div class="row mb-3">
          <label class="col-sm-3 col-form-label" >REF NO - DATE</label> 
          <input class="col-sm-4 border-0" placeholder="Ref No." type="text" bind:value={refno} readonly> 
          <input class="col-sm-2" style="margin-left: 10px !important;" readonly bind:value={refdate}> 
      
        </div>
      
      <div class="row mb-3">
      <label class="col-sm-3 col-form-label">REQUEST TYPE</label>
      <div class="show dropdown col-sm-4">
        <input type="text" class="form-control" placeholder="Select Request Type" readonly on:click={toggleDropdown1} value={requesttypes.join(', ')} required>
        <div class="dropdown-menu ml-2" style="{showDropdown1 ? 'display: block;' : 'display: none;'}; width:300px;margin-left: 0.5rem!important">
          <button type="button" class="clear btn btn-outline-danger ml-1" on:click={clearCheckboxes}><i class="bi bi-x-square"></i></button>
          <button type="button" class="clear btn btn-outline-success ml-1" on:click={selectallCheckboxes}><i class="bi bi-check2-square"></i></button><br>
          <input class="check1 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="ALL PARAMETERS" name="ALL PARAMETERS" value="ALL PARAMETERS" on:change={updateSelectedCount1}>
          <label style="display: inline-block;" for="ALL PARAMETERS">ALL PARAMETERS</label><br>
          <input class="check1 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="CAF" name="CAF" value="CAF" on:change={updateSelectedCount1}>
          <label style="display: inline-block;" for="CAF">CAF</label><br>
          <input class="check1 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="SDR" name="SDR" value="SDR" on:change={updateSelectedCount1}>
          <label style="display: inline-block;" for="SDR">SDR</label><br>
          <input class="check1 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="CDR" name="CDR" value="CDR" on:change={updateSelectedCount1}>
          <label style="display: inline-block;" for="CDR">CDR</label><br>
          <input  class="check1 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="IMEI" name="IMEI" value="IMEI" on:change={updateSelectedCount1}>
          <label style="display: inline-block;" for="IMEI">IMEI</label><br>
          <input class="check1 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="GPRS" name="GPRS" value="GPRS" on:change={updateSelectedCount1}>
          <label style="display: inline-block;" for="GPRS">GPRS</label><br>
          <input class="check1 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="IPDR" name="IPDR" value="IPDR" on:change={updateSelectedCount1}>
          <label style="display: inline-block;" for="IPDR">IPDR</label><br>
          <input class="check1 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="RH" name="RH" value="RH" on:change={updateSelectedCount1}>
          <label style="display: inline-block;" for="RH">RH</label><br>
          <input class="check1 ml-2" style="margin-left: 0.5rem!important"  type="checkbox" id="POA" name="POA" value="POA" on:change={updateSelectedCount1}>
          <label style="display: inline-block;" for="POA">POA</label><br>
          <input class="check1 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="TOWER DATA" name="TOWER DATA" value="TOWER DATA" on:change={updateSelectedCount1}>
          <label style="display: inline-block;" for="TOWER DATA">TOWER DATA</label><br>
        </div>
      </div>
      
      {#if requesttypes.length !== 0}
      <select class="col-sm-2 ml-1" style="margin-left: 10px !important;" bind:value={secondDropdownValue} required>
      <option value="">Select </option>
      {#if requesttypes.length === 1 && requesttypes.includes("CDR") || requesttypes.length === 1 && requesttypes.includes("CAF") || requesttypes.length === 1 && requesttypes.includes("SDR")}
      <option value="Phone">Phone</option>
      <!-- <option value="IMEI">IMEI</option> -->
      {:else if requesttypes.length === 1 && requesttypes.includes("IMEI")}
      <option value="IMEI">IMEI</option>
      <option value="Phone">Phone</option>
      {:else if requesttypes.length === 1 && requesttypes.includes("IPDR")}
      <option value="IPV6">IPV6</option>
      <option value="IPV4">IPV4</option>
      <option value="Phone">Phone</option>
      <option value="IMEI">IMEI</option>
      {:else if requesttypes.length === 1 && requesttypes.includes("GPRS") || requesttypes.length === 2 && requesttypes.includes("GPRS" && "IPDR")}
      <option value="Phone">Phone</option>
      <option value="IMEI">IMEI</option>
      {:else if requesttypes.length === 1 && requesttypes.includes("TOWER DATA")}
      <option value="CGI">CGI (Cell ID)</option>
      <option value="Phone">Phone</option>
      <option value="Co-Ordinates">Co-Ordinates</option>
      <!-- <option value="Area">Area</option>
      <option value="Tower Name">Tower Name</option>   -->
      {:else if requesttypes.length === 1 && requesttypes.includes("RH") || requesttypes.length === 1 && requesttypes.includes("POA") || requesttypes.length === 2 && requesttypes.includes("POA" && "RH")}
      <option value="Phone">Phone</option>
      <option value="Retailer/Dealer Details">Retailer/Dealer Details</option>
      {:else if requesttypes.length === 1 && requesttypes.includes("ALL PARAMETERS")}
      <option value="Phone">Phone</option>
      <option value="IMEI">IMEI</option>
      {:else if requesttypes.length > 0}
      <option value="Phone">Phone</option>
      <option value="IMEI">IMEI</option>
      {/if}
      </select>
      {/if}
      
      </div>
      <!-- {/if} -->
      <div class="row mb-3">
          <div class="col-3">
            <label for="input3">ENTER INPUTS</label>
          </div>
    {#if records.length === 0}
          
          {#if requesttypes.length !== 0 && secondDropdownValue === "Phone" && !requesttypes.includes("IMEI")}
                  <div id="flex-container1">
                    <div class="flex-item">
                      {#each newnumber as newno, index}
                        <div class="input-group mb-1 border-0">
                          <input class="form-control" bind:value={newno.Phno} placeholder="Enter Phone" 
                            aria-label="enter phone number" aria-describedby="button-addon2"  tabindex={index}
                            on:input={(event) => handleInputs(event, index, "Phno")} 
                            maxlength="10"
                      on:input={() => {
                       if (!/^[0-9]*$/.test(newno.Phno)) {
                        newno.Phno = newno.Phno.replace(/[^0-9]/g, ''); // Remove non-digit characters
                          }
                        }}>
                        </div>
                        
                      {/each}
                    </div> 
                    <div class="flex-item">
                      <!-- From Dates Section -->
                      {#each newnumber as newno, index}
                        <div class="input-group border-0">
                          <div class="dropdown" id={`dropdown-${index}`}>
                            <input type="text" class="form-control" style='margin-top:2px' placeholder="Select Providers" readonly on:click={()=> toggleDropdown(index)} bind:value={newno.ISP}>
                            <div class="dropdown-menu ml-3" style="{newno.showDropdown ? 'display: block;' : 'display: none; margin-left: 0.5rem!important'}">
                              <button type="button" class="clear btn btn-outline-danger ml-1" on:click={()=> clearCheckboxes1(index)}><i class="bi bi-x-square"></i></button>
                              <button type="button" class="clear btn btn-outline-success ml-1" on:click={()=> selectallCheckboxes1(index)}><i class="bi bi-check2-square"></i></button><br>       
                              <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Jio" name="provider[]" value="Jio" on:change={()=> updateSelectedCount(index, 'Jio')}>
                              <label style="display: inline-block;" for="provider_Jio">Jio</label><br>
                              <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Airtel" name="provider[]" value="Airtel" on:change={()=> updateSelectedCount(index, 'Airtel')}>
                              <label style="display: inline-block;" for="provider_Airtel">Airtel</label><br>
                              <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_VI" name="provider[]" value="Vodafone" on:change={()=> updateSelectedCount(index,'Vodafone')}>
                              <label style="display: inline-block;" for="provider_VI">Vodafone</label><br>
                              <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_CO" name="provider[]" value="Cellone" on:change={()=> updateSelectedCount(index,'Cellone')}>
                              <label style="display: inline-block;" for="provider_CO">Cellone</label><br>
                            </div>
                          </div>
                        </div>
                      {/each}
                    </div>
              <div class="flex-item">
                <!-- From Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.From_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                  </div>
                {/each}
              </div>
              <div class="flex-item">
                <!-- To Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.To_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',defaultDate: "today"}} placeholder="Select To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                    {#if newnumber.length > 1}
                    <button class="btn btn-danger" on:click={() => removelatlong(index)}>-</button>
                    {/if}
                    {#if index === newnumber.length - 1}
                    <button class="btn btn-primary" id="button-addon2" on:click={handlelatlong}>+</button>
                    <!-- <button class="btn btn-warning" id="button-addon2" on:click={phone_match(newno.Phno)}>Check</button> -->
                    {/if}
                  </div>
                {/each}
               
              </div>
              </div>
              {/if}
        {#if requesttypes.length === 1 && requesttypes.includes("GPRS")  || requesttypes.length === 1 && requesttypes.includes("IPDR") || requesttypes.length === 2 && requesttypes.includes("GPRS" && "IPDR")}
                  <!-- Phone Numbers Section -->
                  {#if requesttypes.includes("IPDR") && secondDropdownValue === "IPV6" || requesttypes.includes("IPDR") && secondDropdownValue === "IPV4"}
                  <div id="flex-container">
                    <div class="flex-item">    
                  {#each newnumber as newno, index}
                    <div class="input-group mb-1 border-0">
                      {#if requesttypes.includes("IPDR") && secondDropdownValue === "IPV6"}
                      <input class="form-control" bind:value={newno.IPV6} tabindex={index} placeholder="enter IPV6" 
                      aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"IP_Address")}>
                      {:else if requesttypes.includes("IPDR") && secondDropdownValue === "IPV4"}
                      <input class="form-control" bind:value={newno.IPV4} tabindex={index} placeholder="enter IPV4" 
                      aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"IPV4")}>
                      {:else}
                      <input class="form-control" bind:value={newno.Phno} tabindex={index} placeholder="enter Phone." 
                      aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"Phno")} maxlength="10"
                      on:input={() => {
                       if (!/^[0-9]*$/.test(newno.Phno)) {
                        newno.Phno = newno.Phno.replace(/[^0-9]/g, ''); // Remove non-digit characters
                          }
                        }}>
                      {#if newno.Phno.length <10}
                          <p style="color: red;font-weight:bold">Enter 10 Digits Only</p>
                          {/if}
                      {/if}
                    </div>
                  {/each}
                  </div>
                  <div class="flex-item">
                    <!-- From Dates Section -->
                    {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.From_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y H:i",minDate: mindate,maxDate: 'today', enableTime : true}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                      </div>
                    {/each}
                  </div>
                  <div class="flex-item">
                    <!-- To Dates Section -->
                    {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.To_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y H:i",minDate: mindate,maxDate: 'today', enableTime: true,defaultDate: "today"}} placeholder="Select To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                        {#if newnumber.length > 1}
                        <button class="btn btn-danger" on:click={() => remove(index)}>-</button>
                        {/if}
                        {#if index === newnumber.length - 1}
                        <button class="btn btn-primary" id="button-addon2" on:click={handleInput}>+</button>
                        {/if}
                      </div>
                    {/each}
                  </div>
                  </div>
                  {/if}            
                  {#if requesttypes.includes("IPDR") && secondDropdownValue === "IMEI" || requesttypes.includes("GPRS")  && secondDropdownValue === "IMEI"}
                  <div id="flex-container">
                    <div class="flex-item">    
                  {#each newnumber as newno, index}
                    <div class="input-group mb-1 border-0">
                      <input class="form-control" bind:value={newno.IMEI} tabindex={index} placeholder="enter IMEI" 
                      aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"IMEI")} on:input={() => {
                        if (!/^[0-9]*$/.test(newno.IMEI)) {
                         newno.IMEI = newno.IMEI.replace(/[^0-9]/g, ''); // Remove non-digit characters
                           }
                         }}
                      maxlength="15">
                    </div>
                  {/each}
                  </div>
                  <div class="flex-item">
                    <!-- From Dates Section -->
                    {#each newnumber as newno, index}
                      <div class="input-group border-0">
                        <div class="dropdown" id={`dropdown-${index}`}>
                          <input type="text" class="form-control" style='margin-top:2px' placeholder="Select Providers" readonly on:click={()=> toggleDropdown(index)} bind:value={newno.ISP}>
                          <div class="dropdown-menu ml-3" style="{newno.showDropdown ? 'display: block;' : 'display: none; margin-left: 0.5rem!important'}">
                            <button type="button" class="clear btn btn-outline-danger ml-1" on:click={()=> clearCheckboxes1(index)}><i class="bi bi-x-square"></i></button>
                            <button type="button" class="clear btn btn-outline-success ml-1" on:click={()=> selectallCheckboxes1(index)}><i class="bi bi-check2-square"></i></button><br>       
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Jio" name="provider[]" value="Jio" on:change={()=> updateSelectedCount(index, 'Jio')}>
                            <label style="display: inline-block;" for="provider_Jio">Jio</label><br>
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Airtel" name="provider[]" value="Airtel" on:change={()=> updateSelectedCount(index, 'Airtel')}>
                            <label style="display: inline-block;" for="provider_Airtel">Airtel</label><br>
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_VI" name="provider[]" value="Vodafone" on:change={()=> updateSelectedCount(index,'Vodafone')}>
                            <label style="display: inline-block;" for="provider_VI">Vodafone</label><br>
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_CO" name="provider[]" value="Cellone" on:change={()=> updateSelectedCount(index,'Cellone')}>
                            <label style="display: inline-block;" for="provider_CO">Cellone</label><br>
                          </div>
                        </div>
                      </div>
                    {/each}
                  </div>
                  <div class="flex-item">
                    <!-- From Dates Section -->
                    {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.From_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y H:i",minDate: mindate,maxDate: 'today', enableTime : true}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                      </div>
                    {/each}
                  </div>
                  <div class="flex-item">
                    <!-- To Dates Section -->
                    {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.To_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y H:i",minDate: mindate,maxDate: 'today', enableTime: true,defaultDate: "today"}} placeholder="Select To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                        {#if newnumber.length > 1}
                        <button class="btn btn-danger" on:click={() => remove(index)}>-</button>
                        {/if}
                        {#if index === newnumber.length - 1}
                        <button class="btn btn-primary" id="button-addon2" on:click={handleInput}>+</button>
                        {/if}
                      </div>
                    {/each}
                  </div>
                  </div>
                  {/if}
              {/if}
              
              {#if requesttypes.includes("IMEI") && secondDropdownValue === "IMEI" || requesttypes.includes("IMEI") && secondDropdownValue === "Phone" }
              <div id="flex-container1">
                {#if secondDropdownValue === 'IMEI'}
                        <div class="flex-item">    
                      {#each newnumber as newno, index}
                        <div class="input-group mb-1 border-0">
                          <input class="form-control" bind:value={newno.IMEI} tabindex={index} placeholder="enter IMEI"
                          aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"IMEI")} on:input={() => {
                            if (!/^[0-9]*$/.test(newno.IMEI)) {
                            newno.IMEI = newno.IMEI.replace(/[^0-9]/g, ''); // Remove non-digit characters
                              }
                            }}
                          maxlength="15">
                        </div>
                      {/each}
                      </div>
                      {:else}
                      <div class="flex-item">
                        {#each newnumber as newno, index}
                          <div class="input-group mb-1 border-0">
                            <input class="form-control" bind:value={newno.Phno} tabindex={index} placeholder="Enter Phone" 
                              aria-label="enter phone number" aria-describedby="button-addon2" 
                              on:input={(event) => handleInputs(event, index, "Phno")} 
                              maxlength="10"
                        on:input={() => {
                        if (!/^[0-9]*$/.test(newno.Phno)) {
                          newno.Phno = newno.Phno.replace(/[^0-9]/g, ''); // Remove non-digit characters
                            }
                          }}>
                          </div>
                  {#if newno.Phno.length <10}
                  <p style="color: red;font-weight:bold">Enter 10 Digits Only</p>
                  {/if}
                {/each}
              </div> 
              {/if}
              <div class="flex-item">
                <!-- From Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group border-0">
                    <div class="dropdown" id={`dropdown-${index}`}>
                      <input type="text" class="form-control" style='margin-top:2px' placeholder="Select Providers" readonly on:click={()=> toggleDropdown(index)} bind:value={newno.ISP}>
                      <div class="dropdown-menu ml-3" style="{newno.showDropdown ? 'display: block;' : 'display: none; margin-left: 0.5rem!important'}">
                        <button type="button" class="clear btn btn-outline-danger ml-1" on:click={()=> clearCheckboxes1(index)}><i class="bi bi-x-square"></i></button>
                        <button type="button" class="clear btn btn-outline-success ml-1" on:click={()=> selectallCheckboxes1(index)}><i class="bi bi-check2-square"></i></button><br>       
                        <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Jio" name="provider[]" value="Jio" on:change={()=> updateSelectedCount(index, 'Jio')}>
                        <label style="display: inline-block;" for="provider_Jio">Jio</label><br>
                        <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Airtel" name="provider[]" value="Airtel" on:change={()=> updateSelectedCount(index, 'Airtel')}>
                        <label style="display: inline-block;" for="provider_Airtel">Airtel</label><br>
                        <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_VI" name="provider[]" value="Vodafone" on:change={()=> updateSelectedCount(index,'Vodafone')}>
                        <label style="display: inline-block;" for="provider_VI">Vodafone</label><br>
                        <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_CO" name="provider[]" value="Cellone" on:change={()=> updateSelectedCount(index,'Cellone')}>
                        <label style="display: inline-block;" for="provider_CO">Cellone</label><br>
                      </div>
                    </div>
                  </div>
                {/each}
              </div>
              <div class="flex-item">
                <!-- From Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.From_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today'}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                  </div>
                {/each}
              </div>
              <div class="flex-item">
                <!-- To Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.To_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',defaultDate: "today"}} placeholder="Select To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                    {#if newnumber.length > 1}
                    <button class="btn btn-danger" on:click={() => remove(index)}>-</button>
                    {/if}
                    {#if index === newnumber.length - 1}
                    <button class="btn btn-primary" id="button-addon2" on:click={handleInput}>+</button>
                    {/if}
                  </div>
                {/each}
              </div>
              </div>
              {/if}
      
              {#if requesttypes.length === 1 && requesttypes.includes("TOWER DATA") && secondDropdownValue === "Co-Ordinates" }
              <div id="flex-container2">
                <div class="flex-item">
              {#each newnumber as newno, index}
              <div class="input-group mb-1 border-0">
                <input
                  class="form-control"
                  bind:value={newno.Latitude}
                  placeholder="Enter Lat*"
                  aria-label="Enter Latitude" tabindex={index}
                  aria-describedby="button-addon2"
                  on:input={(event) => handleInputs(event, index,"Latitude")}
                />
              </div>
              {/each}
                </div>
                <div class="flex-item">
                  {#each newnumber as newno, index}
                  
                  <div class="input-group mb-1 border-0">
                <input
                  class="form-control"
                  bind:value={newno.Longitude}
                  placeholder="Enter Long*" tabindex={index}
                  aria-label="Enter Area Name/Co-Ordinates"
                  aria-describedby="button-addon2"
                  on:input={(event) => handleInputs(event, index,"Longitude")}
                />
              </div>
              {/each}
              </div>
             
              <div class="flex-item">
                <!-- From Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.From_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate, maxDate: 'today'}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                  </div>
                {/each}
              </div>
              <div class="flex-item">
                <!-- To Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.To_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate, maxDate: 'today',defaultDate: "today"}} placeholder="Select To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                    {#if newnumber.length > 1}
                    <button class="btn btn-danger" on:click={() => removelatlong(index)}>-</button>
                    {/if}
                    {#if index === newnumber.length - 1}
                    <button class="btn btn-primary" id="button-addon2" on:click={handlelatlong}>+</button>
                    {/if}
                  </div>
                {/each}
              </div>
              </div>
              {/if}
      
      
      <!-- CGI ID -->
      
            {#if requesttypes.length === 1 && requesttypes.includes("TOWER DATA") && secondDropdownValue === "CGI"}
                <div id="flex-container">
                  <div class="flex-item">    
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.CGI} tabindex={index} placeholder="Enter CGI ID" 
                    aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"CGI")}/>
                  </div>
                {/each}
                </div>
              <div class="flex-item">
                <!-- From Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.From_Date} tabindex={index}  use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today'}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                  </div>
                {/each}
              </div>
              <div class="flex-item">
                <!-- To Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.To_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',defaultDate: "today"}} placeholder="Select To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                    {#if newnumber.length > 1}
                    <button class="btn btn-danger" on:click={() => removelatlong(index)}>-</button>
                    {/if}
                    {#if index === newnumber.length - 1}
                    <button class="btn btn-primary" id="button-addon2" on:click={handlelatlong}>+</button>
                    {/if}
                  </div>
                {/each}
              </div>
              </div>
              {/if}
        {#if requesttypes.length === 1 && requesttypes.includes("RH") && secondDropdownValue === "Retailer/Dealer Details" || requesttypes.length === 1 && requesttypes.includes("POA") && secondDropdownValue === "Retailer/Dealer Details"}
                {#if requesttypes.length === 1 && requesttypes.includes("RH") && secondDropdownValue === "Retailer/Dealer Details"}
                <div id="flex-container1">
                  <div class="flex-item">    
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.RH_Dealer} placeholder="Dealer Details**" 
                    aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"RH_Dealer")}>
                  </div>
                {/each}
                </div>
                <div class="flex-item" style="width: 120px;">    
                  {#each newnumber as newno, index}
                    <div class="input-group mb-1 border-0">
                      <input class="form-control" bind:value={newno.RH_code} placeholder="Dealer code" 
                      aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"RH_code")}>
                    </div>
                  {/each}
                  </div>
                  <div class="flex-item">
                    <!-- From Dates Section -->
                    {#each newnumber as newno, index}
                      <div class="input-group border-0">
                        <div class="dropdown" id={`dropdown-${index}`}>
                          <input type="text" class="form-control" style='margin-top:2px' placeholder="Select Providers" readonly on:click={()=> toggleDropdown(index)} bind:value={newno.ISP}>
                          <div class="dropdown-menu ml-3" style="{newno.showDropdown ? 'display: block;' : 'display: none; margin-left: 0.5rem!important'}">
                            <button type="button" class="clear btn btn-outline-danger ml-1" on:click={()=> clearCheckboxes1(index)}><i class="bi bi-x-square"></i></button>
                              <button type="button" class="clear btn btn-outline-success ml-1" on:click={()=> selectallCheckboxes1(index)}><i class="bi bi-check2-square"></i></button><br>       
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Jio" name="provider[]" value="Jio" on:change={()=> updateSelectedCount(index, 'Jio')}>
                            <label style="display: inline-block;" for="provider_Jio">Jio</label><br>
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Airtel" name="provider[]" value="Airtel" on:change={()=> updateSelectedCount(index, 'Airtel')}>
                            <label style="display: inline-block;" for="provider_Airtel">Airtel</label><br>
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_VI" name="provider[]" value="Vodafone" on:change={()=> updateSelectedCount(index,'Vodafone')}>
                            <label style="display: inline-block;" for="provider_VI">Vodafone</label><br>
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_CO" name="provider[]" value="Cellone" on:change={()=> updateSelectedCount(index,'Cellone')}>
                            <label style="display: inline-block;" for="provider_CO">Cellone</label><br>
                          </div>
                        </div>
                      </div>
                    {/each}
                  </div>
              <div class="flex-item"  style="width: 140px;">
                <!-- From Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.From_Date} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                  </div>
                {/each}
              </div>
              <div class="flex-item"  style="width: 140px;">
                <!-- To Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.To_Date} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',defaultDate: "today"}} placeholder="To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                    {#if newnumber.length > 1}
                    <button class="btn btn-danger" on:click={() => removelatlong(index)}>-</button>
                    {/if}
                    {#if index === newnumber.length - 1}
                    <button class="btn btn-primary" id="button-addon2" on:click={handlelatlong}>+</button>
                    {/if}
                  </div>
                {/each}
              </div>
              </div>
              {/if}
              {#if requesttypes.length === 1 && requesttypes.includes("POA") && secondDropdownValue === "Retailer/Dealer Details"}
              
              <div id="flex-container1">
                <div class="flex-item">    
                  {#each newnumber as newno, index}
                    <div class="input-group mb-1 border-0">
                      <input class="form-control" bind:value={newno.POA_Dealer} placeholder="Dealer Details**" 
                      aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"POA_Dealer")}>
                    </div>
                  {/each}
                  </div>
                  <div class="flex-item" style="width: 120px;">    
                    {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.POA_code} placeholder="Dealer code" 
                        aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"POA_code")}>
                      </div>
                    {/each}
                    </div>
                    <div class="flex-item">
                      <!-- From Dates Section -->
                      {#each newnumber as newno, index}
                        <div class="input-group border-0">
                          <div class="dropdown" id={`dropdown-${index}`}>
                            <input type="text" class="form-control" style='margin-top:2px' placeholder="Select Providers" readonly on:click={()=> toggleDropdown(index)} bind:value={newno.ISP}>
                            <div class="dropdown-menu ml-3" style="{newno.showDropdown ? 'display: block;' : 'display: none; margin-left: 0.5rem!important'}">
                              <button type="button" class="clear btn btn-outline-danger ml-1" on:click={()=> clearCheckboxes1(index)}><i class="bi bi-x-square"></i></button>
                              <button type="button" class="clear btn btn-outline-success ml-1" on:click={()=> selectallCheckboxes1(index)}><i class="bi bi-check2-square"></i></button><br>       
                              <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Jio" name="provider[]" value="Jio" on:change={()=> updateSelectedCount(index, 'Jio')}>
                              <label style="display: inline-block;" for="provider_Jio">Jio</label><br>
                              <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Airtel" name="provider[]" value="Airtel" on:change={()=> updateSelectedCount(index, 'Airtel')}>
                              <label style="display: inline-block;" for="provider_Airtel">Airtel</label><br>
                              <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_VI" name="provider[]" value="Vodafone" on:change={()=> updateSelectedCount(index,'Vodafone')}>
                              <label style="display: inline-block;" for="provider_VI">Vodafone</label><br>
                              <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_CO" name="provider[]" value="Cellone" on:change={()=> updateSelectedCount(index,'Cellone')}>
                              <label style="display: inline-block;" for="provider_CO">Cellone</label><br>
                            </div>
                          </div>
                        </div>
                      {/each}
                    </div>
              <div class="flex-item" style="width: 140px;">
                <!-- From Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.From_Date} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                  </div>
                {/each}
              </div>
              <div class="flex-item" style="width: 140px;">
                <!-- To Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.To_Date} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',defaultDate: "today"}} placeholder="Select To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                    {#if newnumber.length > 1}
                    <button class="btn btn-danger" on:click={() => removelatlong(index)}>-</button>
                    {/if}
                    {#if index === newnumber.length - 1}
                    <button class="btn btn-primary" id="button-addon2" on:click={handlelatlong}>+</button>
                    {/if}
                  </div>
                {/each}
              </div>
              </div>
              {/if}
        {/if}
        {/if}
        {#if records.length > 0}
        <div class="col-auto scroll-table">
          <table class="table table-bordered">
               <tr>
                 {#each columnNames as columnName}
                 <th>{columnName}</th>
                 {/each}
                </tr>
                {#each records as record}
                
                   <tr>
                     {#each columnNames as columnName}
                     {#if record[columnName] !== undefined && record[columnName] !== ''}
                     <td>{record[columnName]}</td>
                     {/if}
                     {/each}
                    </tr>
                    
                    {/each}
                  </table>
           </div>
           {/if}
           <div class="uni">
             
          <input type="file" accept=".csv,.xlsx, .xls" on:change={handleFileUpload} id="excel_file"/>
          {#if records.length > 0}
          <p class="ml-2 mb-2" style = "color:green;">File Uploaded......</p>
      {/if}
          </div>
        </div>
      {/if}
      
      
      
  {:else if requestcategory === 'Data Request' || requestcategory === ''}
      <SelectDropdown label={"NEW/UPDATE"} options={["Select","NEW","UPDATE"]} display_func={o => o} bind:value={update} />
        
       
          <div class="row mb-3">
            <label class="col-sm-3 col-form-label">REQUEST TYPE</label>
            <!-- <MultiSelect id='lang'  bind:value={requesttype} on:change={handleFirstDropdownChange}> -->
              <select class="col-sm-4" bind:value={requesttype}  on:change={handleFirstDropdownChange} required>
                <option value="">Select </option>
                <option value="CAF">CAF</option>
                <option value="SDR">SDR</option>
                <option value="CDR">CDR</option>
                <!-- <option value="CAF/CDR">CAF/CDR</option> -->
                <option value="ISD">ISD</option>
                <option value="GPRS">GPRS</option>
                <option value="IPDR">IPDR</option>
                <option value="RH">RH</option>
                <option value="POA">POA</option>
                <option value="IMEI CDR"> IMEI CDR</option>
                <option value="TOWER CDR">TOWER CDR</option>
                <option value="TOWER GPRS">TOWER GPRS</option>
                <option value="TOWER IPDR">TOWER IPDR</option>
                <!-- <option value="POA OF DEALER">POA OF DEALER</option> -->
                
              </select>
              <!-- </MultiSelect> -->
      
      <select class="col-sm-2 second_dd" hidden={!showSecondDropdown} bind:value={secondDropdownValue} required>
      <option value="">Select </option>
      <option value="IPV6">IPV6</option>
      <option value="IPV4">IPV4</option>
      <option value="IMEI">IMEI</option>
      <option value="Phone">Phone</option>
      </select>
      
      <select class="col-sm-2 second_dd" hidden={!showGprssDropdown} bind:value={showGprssDropdownvalue}  required>
      <option value="">Select </option>
      <option value="Phone">Phone No.</option>
      <option value="IMEI">IMEI</option>
      </select>
      {#if requesttype === "TOWER CDR" || requesttype === "TOWER GPRS"||requesttype === "TOWER IPDR"}
      <select class="col-sm-2 ml-1" bind:value={showCdrDropdownvalue} required>
        <option value="">Select </option>
        <option value="CGI">CGI (Cell ID)</option>
        <!-- <option value="Phone">Phone No.</option> -->
        <!-- <option value="Area">Area</option> -->
        <!-- <option value="Co-Ordinates">Co-Ordinates</option> -->
        <!-- <option value="Tower Name">Tower Name</option>   -->
      </select>
      {/if}
      {#if requesttype === "RH"||requesttype === "POA"} 
      <select class="col-sm-2 second_dd" bind:value={showPoaDropdownvalue} required>
        <option value="">Select </option>
        <option value="Phone">PHONE</option>
        <option value="Retailer/Dealer Details">Retailer/Dealer Details</option>
        <!-- <option value="Retailer/Dealer Code*">Retailer/Dealer Code*</option> -->
      </select>
      {/if}
      {#if requesttype === "SDR"}
      <select class="col-sm-2 second_dd" bind:value={sdrdropdown} required>
        <option value="">Select </option>
        <option value="SDR">SDR</option>
        <option value="SDR HISTORY">SDR History</option>
      </select>
      {/if}
      </div>
      <div class="row mb-2">
        <label class="col-sm-3 col-form-label">ENTER INPUTS</label>
        
            
        {#if records.length === 0}
       
        {#if requesttype=== "GPRS" || requesttype==="IPDR"}
        
                  <!-- Phone Numbers Section -->
                  {#if requesttype=== "IPDR" && secondDropdownValue === "IPV6" || requesttype=== "IPDR" && secondDropdownValue === "IPV4"}
                  <div id="flex-container1">
                    <div class="flex-item">    
                  {#each newnumber as newno, index}
                    <div class="input-group mb-1 border-0">
                      {#if requesttype=== "IPDR" && secondDropdownValue === "IPV6"}
                      <input class="form-control" bind:value={newno.IPV6} tabindex={index} placeholder="enter IPV6" 
                      aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"IP_Address")}>
                      {:else if requesttype=== "IPDR" && secondDropdownValue === "IPV4"}
                      <input class="form-control" bind:value={newno.IPV4}  tabindex={index} placeholder="enter IPV4" 
                      aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"IP_Address")}>
                      {:else}
                      <input class="form-control" bind:value={newno.Phno} tabindex={index} placeholder="enter Phone." 
                      aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"Phno")} maxlength="10"
                      on:input={() => {
                        if (!/^[0-9]*$/.test(newno.Phno)) {
                          newno.Phno = newno.Phno.replace(/[^0-9]/g, ''); // Remove non-digit characters
                        }
                      }}>
      
                      {/if}
                  
                    </div>
                  {/each}
                  </div>
                  {#if requesttype=== "IPDR" && secondDropdownValue === "IPV6" || requesttype=== "IPDR" && secondDropdownValue === "IPV4"}
                  <div class="flex-item">
                    <!-- From Dates Section -->
                    {#each newnumber as newno, index}
                      <div class="input-group border-0">
                        <div class="dropdown" id={`dropdown-${index}`}>
                          <input type="text" class="form-control" style='margin-top:2px' placeholder="Select Providers" readonly on:click={()=> toggleDropdown(index)} bind:value={newno.ISP}>
                          <div class="dropdown-menu ml-3" style="{newno.showDropdown ? 'display: block;' : 'display: none; margin-left: 0.5rem!important'}">
                            <button type="button" class="clear btn btn-outline-danger ml-1" on:click={()=> clearCheckboxes1(index)}><i class="bi bi-x-square"></i></button>
                            <button type="button" class="clear btn btn-outline-success ml-1" on:click={()=> selectallCheckboxes1(index)}><i class="bi bi-check2-square"></i></button><br>       
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Jio" name="provider[]" value="Jio" on:change={()=> updateSelectedCount(index, 'Jio')}>
                            <label style="display: inline-block;" for="provider_Jio">Jio</label><br>
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Airtel" name="provider[]" value="Airtel" on:change={()=> updateSelectedCount(index, 'Airtel')}>
                            <label style="display: inline-block;" for="provider_Airtel">Airtel</label><br>
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_VI" name="provider[]" value="Vodafone" on:change={()=> updateSelectedCount(index,'Vodafone')}>
                            <label style="display: inline-block;" for="provider_VI">Vodafone</label><br>
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_CO" name="provider[]" value="Cellone" on:change={()=> updateSelectedCount(index,'Cellone')}>
                            <label style="display: inline-block;" for="provider_CO">Cellone</label><br>
                          </div>
                        </div>
                      </div>
                    {/each}
                  </div>
                  {/if}
                  <div class="flex-item" style="width:110px;">
                  {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.From_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today'}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                      </div>
                    {/each}
                  </div>
                  <div class="flex-item"  style="width:100px;">
                    <!-- From Dates Section -->
                    {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.From_Time} tabindex={index} use:flatpickr={{ dateFormat: "H:i",enableTime:true,noCalendar: true}} placeholder="FromTime" on:input={(event) => handleInputs(event, index,"From_Time")} >
                      </div>
                    {/each}
                  </div>
                  <div class="flex-item"  style="width:120px;">
                    <!-- From Dates Section -->
                    {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.To_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',defaultDate: "today"}} placeholder="To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                      </div>
                      {/each}
                    </div>
                    <div class="flex-item"  style="width:120px;">
                      <!-- To Dates Section -->
                      {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.To_Time} tabindex={index} use:flatpickr={{ dateFormat: "H:i",enableTime:true,noCalendar: true}} placeholder="ToTime" on:input={(event) => handleInputs(event, index,"To_Time")} >
                        {#if newnumber.length > 1}
                        <button class="btn btn-danger" on:click={() => remove(index)}>-</button>
                        {/if}
                        {#if index === newnumber.length - 1}
                        <button class="btn btn-primary" id="button-addon2" on:click={handleInput}>+</button>
                        {/if}
                      </div>
                    {/each}
                  </div>
                  </div>
                  {/if}
                  {#if requesttype=== "IPDR" && secondDropdownValue === "Phone" || requesttype==="GPRS" && showGprssDropdownvalue === "Phone"}
                  <div id="flex-container1" style='margin-left:50px'>
                    <div class="flex-item">    
                  {#each newnumber as newno, index}
                    <div class="input-group mb-1 border-0">
                      <input class="form-control" bind:value={newno.Phno} tabindex={index} placeholder="Enter Phone" 
                      aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"Phno")} maxlength="10"
                      on:input={() => {
                       if (!/^[0-9]*$/.test(newno.Phno)) {
                        newno.Phno = newno.Phno.replace(/[^0-9]/g, ''); // Remove non-digit characters
                          }
                        }}>
                    
                    </div>
                  {/each}
                  </div>
                  <div class="flex-item" style="width: 110px;">
                    <!-- From Dates Section -->
                    {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" id="fetchnickname{index}" tabindex={index} bind:value={newno.Nickname} placeholder="Nickname." 
                        aria-label="enter Nickname" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"Nickname")}>
                      </div>
                    {/each}
                  </div>
                  <div class="flex-item" style="width:110px;">
                  {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.From_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today'}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                      </div>
                    {/each}
                  </div>
                  <div class="flex-item"  style="width:100px;">
                    <!-- From Dates Section -->
                    {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.From_Time} tabindex={index} use:flatpickr={{ dateFormat: "H:i",enableTime:true,noCalendar: true}} placeholder="FromTime" on:input={(event) => handleInputs(event, index,"From_Time")} >
                      </div>
                    {/each}
                  </div>
                  <div class="flex-item"  style="width:120px;">
                    <!-- From Dates Section -->
                    {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.To_Date}  tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',defaultDate: "today"}} placeholder="To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                      </div>
                      {/each}
                    </div>
                    <div class="flex-item"  style="width:120px;">
                      <!-- To Dates Section -->
                      {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.To_Time} tabindex={index} use:flatpickr={{ dateFormat: "H:i",enableTime:true,noCalendar: true}} placeholder="ToTime" on:input={(event) => handleInputs(event, index,"To_Time")} >
                        {#if newnumber.length > 1}
                        <button class="btn btn-danger" on:click={() => remove(index)}>-</button>
                        {/if}
                        {#if index === newnumber.length - 1}
                        <button class="btn btn-primary" id="button-addon2" on:click={handleInput}>+</button>
                        {/if}
                      </div>
                    {/each}
                  </div>
                </div>
                  {/if}
                  
                  {#if requesttype=== "IPDR" && secondDropdownValue === "IMEI" || requesttype==="GPRS" &&showGprssDropdownvalue === "IMEI"}
                  <div id="flex-container1">
                    <div class="flex-item">    
                  {#each newnumber as newno, index}
                    <div class="input-group mb-1 border-0">
                      <input class="form-control" bind:value={newno.IMEI} tabindex={index} placeholder="IMEI" 
                      aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"IMEI")} on:input={() => {
                        if (!/^[0-9]*$/.test(newno.IMEI)) {
                         newno.IMEI = newno.IMEI.replace(/[^0-9]/g, ''); // Remove non-digit characters
                           }
                         }}
                      maxlength="15">
                    </div>
                  {/each}
                  </div>
                  <div class="flex-item">
                    <!-- From Dates Section -->
                    {#each newnumber as newno, index}
                      <div class="input-group border-0">
                        <div class="dropdown" id={`dropdown-${index}`}>
                          <input type="text" class="form-control" style='margin-top:2px' placeholder="Select Providers" readonly on:click={()=> toggleDropdown(index)} bind:value={newno.ISP}>
                          <div class="dropdown-menu ml-3" style="{newno.showDropdown ? 'display: block;' : 'display: none; margin-left: 0.5rem!important'}">
                            <button type="button" class="clear btn btn-outline-danger ml-1" on:click={()=> clearCheckboxes1(index)}><i class="bi bi-x-square"></i></button>
                            <button type="button" class="clear btn btn-outline-success ml-1" on:click={()=> selectallCheckboxes1(index)}><i class="bi bi-check2-square"></i></button><br>       
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Jio" name="provider[]" value="Jio" on:change={()=> updateSelectedCount(index, 'Jio')}>
                            <label style="display: inline-block;" for="provider_Jio">Jio</label><br>
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Airtel" name="provider[]" value="Airtel" on:change={()=> updateSelectedCount(index, 'Airtel')}>
                            <label style="display: inline-block;" for="provider_Airtel">Airtel</label><br>
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_VI" name="provider[]" value="Vodafone" on:change={()=> updateSelectedCount(index,'Vodafone')}>
                            <label style="display: inline-block;" for="provider_VI">Vodafone</label><br>
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_CO" name="provider[]" value="Cellone" on:change={()=> updateSelectedCount(index,'Cellone')}>
                            <label style="display: inline-block;" for="provider_CO">Cellone</label><br>
                          </div>
                        </div>
                      </div>
                    {/each}
                  </div>
                  <div class="flex-item" style="width:110px;">
                    <!-- From Dates Section -->
                    {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.From_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today'}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                      </div>
                    {/each}
                  </div>
                  <div class="flex-item"  style="width:100px;">
                    <!-- From Dates Section -->
                    {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.From_Time} tabindex={index} use:flatpickr={{ dateFormat: "H:i",enableTime:true,noCalendar: true}} placeholder="FromTime" on:input={(event) => handleInputs(event, index,"From_Time")} >
                      </div>
                    {/each}
                  </div>
                  <div class="flex-item"  style="width:120px;">
                    <!-- From Dates Section -->
                    {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.To_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',defaultDate: "today"}} placeholder="To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                      </div>
                      {/each}
                    </div>
                    <div class="flex-item"  style="width:120px;">
                      <!-- To Dates Section -->
                      {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.To_Time} tabindex={index} use:flatpickr={{ dateFormat: "H:i",enableTime:true,noCalendar: true}} placeholder="ToTime" on:input={(event) => handleInputs(event, index,"To_Time")} >
                        {#if newnumber.length > 1}
                        <button class="btn btn-danger" on:click={() => remove(index)}>-</button>
                        {/if}
                        {#if index === newnumber.length - 1}
                        <button class="btn btn-primary" id="button-addon2" on:click={handleInput}>+</button>
                        {/if}
                      </div>
                    {/each}
                  </div>
                  </div>
                  {/if}
              {/if}
      <!-- CGI ID -->
            {#if requesttype=== "TOWER CDR" && showCdrDropdownvalue === "CGI" || requesttype=== "TOWER GPRS" && showCdrDropdownvalue === "CGI" || requesttype=== "TOWER IPDR" && showCdrDropdownvalue === "CGI" }
                <div id="flex-container1">
                  <div class="flex-item">    
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.CGI} tabindex={index} placeholder="Enter CGI ID" 
                    aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"CGI")}/>
                  </div>
                {/each}
                </div>
                <div class="flex-item">
                  <!-- From Dates Section -->
                  {#each newnumber as newno, index}
                    <div class="input-group border-0">
                      <div class="dropdown" id={`dropdown-${index}`}>
                        <input type="text" class="form-control" style='margin-top:2px' placeholder="Select Providers" readonly on:click={()=> toggleDropdown(index)} bind:value={newno.ISP}>
                        <div class="dropdown-menu ml-3" style="{newno.showDropdown ? 'display: block;' : 'display: none; margin-left: 0.5rem!important'}">
                          <button type="button" class="clear btn btn-outline-danger ml-1" on:click={()=> clearCheckboxes1(index)}><i class="bi bi-x-square"></i></button>
                          <button type="button" class="clear btn btn-outline-success ml-1" on:click={()=> selectallCheckboxes1(index)}><i class="bi bi-check2-square"></i></button><br>       
                          <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Jio" name="provider[]" value="Jio" on:change={()=> updateSelectedCount(index, 'Jio')}>
                          <label style="display: inline-block;" for="provider_Jio">Jio</label><br>
                          <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Airtel" name="provider[]" value="Airtel" on:change={()=> updateSelectedCount(index, 'Airtel')}>
                          <label style="display: inline-block;" for="provider_Airtel">Airtel</label><br>
                          <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_VI" name="provider[]" value="Vodafone" on:change={()=> updateSelectedCount(index,'Vodafone')}>
                          <label style="display: inline-block;" for="provider_VI">Vodafone</label><br>
                          <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_CO" name="provider[]" value="Cellone" on:change={()=> updateSelectedCount(index,'Cellone')}>
                          <label style="display: inline-block;" for="provider_CO">Cellone</label><br>
                        </div>
                      </div>
                    </div>
                  {/each}
                </div>

              <div class="flex-item">
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.From_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today'}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                  </div>
                {/each}
              </div>
              <div class="flex-item">
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.To_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',defaultDate: "today"}} placeholder="Select To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                    {#if newnumber.length > 1}
                    <button class="btn btn-danger" on:click={() => removelatlong(index)}>-</button>
                    {/if}
                    {#if index === newnumber.length - 1}
                    <button class="btn btn-primary" id="button-addon2" on:click={handlelatlong}>+</button>
                    {/if}
                  </div>
                {/each}
              </div>
              </div>
              {/if}
      
              {#if requesttype === "CDR"}
              <div id="flex-container1">
                <div class="flex-item">
                  {#each newnumber as newno, index}
                    <div class="input-group mb-1 border-0">
                      <input class="form-control" bind:value={newno.Phno} placeholder="Enter Phone" 
                        aria-label="enter phone number" aria-describedby="button-addon2" tabindex={index}
                                              on:input={(event) => handleInputs(event, index, "Phno")} 
                        maxlength="10"
                  on:input={() => {
                   if (!/^[0-9]*$/.test(newno.Phno)) {
                    newno.Phno = newno.Phno.replace(/[^0-9]/g, ''); // Remove non-digit characters
                      }
                    }}>
                    </div>
                    
                  {/each}
                </div> 
              <div class="flex-item">
              <!-- From Dates Section -->
              {#each newnumber as newno, index}
             
            <div class="input-group mb-1 border-0">
              <input class="form-control" id="fetchnickname{index}" bind:value={newno.Nickname} placeholder="enter Nickname." 
                aria-label="enter Nickname" aria-describedby="button-addon2" tabindex={index} on:input={(event) => handleInputs(event, index,"Nickname")}>
            </div>
                <!-- {/if} -->
              {/each}
            </div>
          <div class="flex-item">
            <!-- From Dates Section -->
            {#each newnumber as newno, index}
              <div class="input-group mb-1 border-0">
                <input class="form-control" bind:value={newno.From_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
              </div>
            {/each}
          </div>
          <div class="flex-item">
            <!-- To Dates Section -->
            {#each newnumber as newno, index}
              <div class="input-group mb-1 border-0">
                <input class="form-control" bind:value={newno.To_Date} tabindex={index} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',defaultDate: "today"}} placeholder="Select To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                {#if newnumber.length > 1}
                <button class="btn btn-danger" on:click={() => removelatlong(index)}>-</button>
                {/if}
                {#if index === newnumber.length - 1}
                <button class="btn btn-primary" id="button-addon2" on:click={handlelatlong}>+</button>
                <!-- <button class="btn btn-warning" id="button-addon2" on:click={phone_match(newno.Phno)}>Check</button> -->
                {/if}
              </div>
            {/each}
           
          </div>
          </div>
          {/if}
              {#if requesttype=== "RH" && showPoaDropdownvalue === "Phone" || requesttype=== "POA" && showPoaDropdownvalue === "Phone"}
              <div id="flex-container1">
                  <div class="flex-item">    
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.Phno} placeholder="Enter Phone" 
                    aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"Phno")} maxlength="10"
                    on:input={() => {
                     if (!/^[0-9]*$/.test(newno.Phno)) {
                      newno.Phno = newno.Phno.replace(/[^0-9]/g, ''); // Remove non-digit characters
                        }
                      }}>
                  </div>
                  {#if newno.Phno.length <10}
                  <p style="color: red;font-weight:bold">Enter 10 Digits Only</p>
                  {/if}
      
                {/each}
                </div>
                <div class="flex-item">
                  <!-- From Dates Section -->
                  {#each newnumber as newno, index}
                    <div class="input-group mb-1 border-0">
                      <input class="form-control" id="fetchnickname{index}" bind:value={newno.Nickname} placeholder="Nickname." 
                      aria-label="enter Nickname" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"Nickname")}>
                    </div>
                  {/each}
                </div>
              <div class="flex-item">
                <!-- From Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.From_Date} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                  </div>
                {/each}
              </div>
              <div class="flex-item">
                <!-- To Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.To_Date} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',defaultDate: "today"}} placeholder="Select To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                    {#if newnumber.length > 1}
                    <button class="btn btn-danger" on:click={() => removelatlong(index)}>-</button>
                    {/if}
                    {#if index === newnumber.length - 1}
                    <button class="btn btn-primary" id="button-addon2" on:click={handlelatlong}>+</button>
                    {/if}
                  </div>
                {/each}
              </div>
              </div>
              {/if}
              
              {#if requesttype=== "RH" && showPoaDropdownvalue === "Retailer/Dealer Details" || requesttype=== "POA" && showPoaDropdownvalue === "Retailer/Dealer Details"}
                {#if requesttype=== "RH" && showPoaDropdownvalue === "Retailer/Dealer Details"}
                <div id="flex-container1">
                  <div class="flex-item">    
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.RH_Dealer} placeholder="Dealer Details**" 
                    aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"RH_Dealer")}>
                  </div>
                {/each}
                </div>
                <div class="flex-item" style="width: 120px;">    
                  {#each newnumber as newno, index}
                    <div class="input-group mb-1 border-0">
                      <input class="form-control" bind:value={newno.RH_code} placeholder="Dealer code" 
                      aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"RH_code")}>
                    </div>
                  {/each}
                  </div>
                  <div class="flex-item">
                    <!-- From Dates Section -->
                    {#each newnumber as newno, index}
                      <div class="input-group border-0">
                        <div class="dropdown" id={`dropdown-${index}`}>
                          <input type="text" class="form-control" style='margin-top:2px' placeholder="Select Providers" readonly on:click={()=> toggleDropdown(index)} bind:value={newno.ISP}>
                          <div class="dropdown-menu ml-3" style="{newno.showDropdown ? 'display: block;' : 'display: none; margin-left: 0.5rem!important'}">
                            <button type="button" class="clear btn btn-outline-danger ml-1" on:click={()=> clearCheckboxes1(index)}><i class="bi bi-x-square"></i></button>
                              <button type="button" class="clear btn btn-outline-success ml-1" on:click={()=> selectallCheckboxes1(index)}><i class="bi bi-check2-square"></i></button><br>       
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Jio" name="provider[]" value="Jio" on:change={()=> updateSelectedCount(index, 'Jio')}>
                            <label style="display: inline-block;" for="provider_Jio">Jio</label><br>
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Airtel" name="provider[]" value="Airtel" on:change={()=> updateSelectedCount(index, 'Airtel')}>
                            <label style="display: inline-block;" for="provider_Airtel">Airtel</label><br>
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_VI" name="provider[]" value="Vodafone" on:change={()=> updateSelectedCount(index,'Vodafone')}>
                            <label style="display: inline-block;" for="provider_VI">Vodafone</label><br>
                            <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_CO" name="provider[]" value="Cellone" on:change={()=> updateSelectedCount(index,'Cellone')}>
                            <label style="display: inline-block;" for="provider_CO">Cellone</label><br>
                          </div>
                        </div>
                      </div>
                    {/each}
                  </div>
              <div class="flex-item"  style="width: 140px;">
                <!-- From Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.From_Date} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                  </div>
                {/each}
              </div>
              <div class="flex-item"  style="width: 140px;">
                <!-- To Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.To_Date} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',defaultDate: "today"}} placeholder="To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                    {#if newnumber.length > 1}
                    <button class="btn btn-danger" on:click={() => removelatlong(index)}>-</button>
                    {/if}
                    {#if index === newnumber.length - 1}
                    <button class="btn btn-primary" id="button-addon2" on:click={handlelatlong}>+</button>
                    {/if}
                  </div>
                {/each}
              </div>
              </div>
              {/if}
              {#if requesttype=== "POA" && showPoaDropdownvalue === "Retailer/Dealer Details"}
              
              <div id="flex-container1">
                <div class="flex-item">    
                  {#each newnumber as newno, index}
                    <div class="input-group mb-1 border-0">
                      <input class="form-control" bind:value={newno.POA_Dealer} placeholder="Dealer Details**" 
                      aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"POA_Dealer")}>
                    </div>
                  {/each}
                  </div>
                  <div class="flex-item" style="width: 120px;">    
                    {#each newnumber as newno, index}
                      <div class="input-group mb-1 border-0">
                        <input class="form-control" bind:value={newno.POA_code} placeholder="Dealer code" 
                        aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"POA_code")}>
                      </div>
                    {/each}
                    </div>
                    <div class="flex-item">
                      <!-- From Dates Section -->
                      {#each newnumber as newno, index}
                        <div class="input-group border-0">
                          <div class="dropdown" id={`dropdown-${index}`}>
                            <input type="text" class="form-control" style='margin-top:2px' placeholder="Select Providers" readonly on:click={()=> toggleDropdown(index)} bind:value={newno.ISP}>
                            <div class="dropdown-menu ml-3" style="{newno.showDropdown ? 'display: block;' : 'display: none; margin-left: 0.5rem!important'}">
                              <button type="button" class="clear btn btn-outline-danger ml-1" on:click={()=> clearCheckboxes1(index)}><i class="bi bi-x-square"></i></button>
                              <button type="button" class="clear btn btn-outline-success ml-1" on:click={()=> selectallCheckboxes1(index)}><i class="bi bi-check2-square"></i></button><br>       
                              <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Jio" name="provider[]" value="Jio" on:change={()=> updateSelectedCount(index, 'Jio')}>
                              <label style="display: inline-block;" for="provider_Jio">Jio</label><br>
                              <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Airtel" name="provider[]" value="Airtel" on:change={()=> updateSelectedCount(index, 'Airtel')}>
                              <label style="display: inline-block;" for="provider_Airtel">Airtel</label><br>
                              <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_VI" name="provider[]" value="Vodafone" on:change={()=> updateSelectedCount(index,'Vodafone')}>
                              <label style="display: inline-block;" for="provider_VI">Vodafone</label><br>
                              <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_CO" name="provider[]" value="Cellone" on:change={()=> updateSelectedCount(index,'Cellone')}>
                              <label style="display: inline-block;" for="provider_CO">Cellone</label><br>
                            </div>
                          </div>
                        </div>
                      {/each}
                    </div>
              <div class="flex-item" style="width: 140px;">
                <!-- From Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.From_Date} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                  </div>
                {/each}
              </div>
              <div class="flex-item" style="width: 140px;">
                <!-- To Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.To_Date} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',defaultDate: "today"}} placeholder="Select To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                    {#if newnumber.length > 1}
                    <button class="btn btn-danger" on:click={() => removelatlong(index)}>-</button>
                    {/if}
                    {#if index === newnumber.length - 1}
                    <button class="btn btn-primary" id="button-addon2" on:click={handlelatlong}>+</button>
                    {/if}
                  </div>
                {/each}
              </div>
              </div>
              {/if}
              {/if}
      
              {#if requesttype=== "CAF"}
              
              <div id="flex-container-caf">
                <div class="flex-item">    
                  {#each newnumber as newno, index}
                    <div class="input-group mb-1 border-0">
                      <input class="form-control" bind:value={newno.Phno} placeholder="Enter Phno." 
                      aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"Phno")} maxlength="10"
                      on:input={() => {
                       if (!/^[0-9]*$/.test(newno.Phno)) {
                        newno.Phno = newno.Phno.replace(/[^0-9]/g, ''); // Remove non-digit characters
                          }
                        }}>
                    </div>
                    {#if newno.Phno.length <10}
                    <p style="color: red;font-weight:bold">Enter 10 Digits Only</p>
                    {/if}
                  {/each}
                  </div>
              <div class="flex-item">
                <!-- To Dates Section -->
                {#each newnumber as newno, index}
                <div class="input-group mb-1 border-0">
                  <input class="form-control" bind:value={newno.CAF} placeholder="Enter CAF No." 
                  aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"CAF")}>
                {#if newnumber.length > 1}
                    <button class="btn btn-danger" on:click={() => removelatlong(index)}>-</button>
                    {/if}
                    {#if index === newnumber.length - 1}
                    <button class="btn btn-primary" id="button-addon2" on:click={for_caf}>+</button>
                    {/if}
                  </div>
                {/each}
              </div>
              </div>
              {/if}
              {#if requesttype=== "SDR" && (sdrdropdown === "SDR" || sdrdropdown === "SDR HISTORY") || requesttype === "ISD"}
              
              <div id="flex-container-caf">
                <div class="flex-item" style="width: 35%;">    
                  {#each newnumber as newno, index}
                    <div class="input-group mb-1 border-0">
                      <input class="form-control" bind:value={newno.Phno} placeholder="Enter Phno." 
                      aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"Phno")} maxlength="10"
                      on:input={() => {
                       if (!/^[0-9]*$/.test(newno.Phno)) {
                        newno.Phno = newno.Phno.replace(/[^0-9]/g, ''); // Remove non-digit characters
                          }
                        }}>
                {#if newnumber.length > 1}
                <button class="btn btn-danger" on:click={() => removelatlong(index)}>-</button>
                {/if}
                {#if index === newnumber.length - 1}
                <button class="btn btn-primary" id="button-addon2" on:click={for_caf}>+</button>
                {/if}
              </div>
              {#if newno.Phno.length <10}
              <p style="color: red;font-weight:bold">Enter 10 Digits Only</p>
              {/if}
                {/each}
              </div>
              </div>
              {/if}
      
              {#if requesttype=== "CAF/CDR"}
              
              <div id="flex-container">
                <div class="flex-item">    
                  {#each newnumber as newno, index}
                    <div class="input-group mb-1 border-0">
                      <input class="form-control" bind:value={newno.Phno} placeholder="Enter Phno/CAF No." 
                      aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"Phno")} maxlength="10"
                      on:input={() => {
                       if (!/^[0-9]*$/.test(newno.Phno)) {
                        newno.Phno = newno.Phno.replace(/[^0-9]/g, ''); // Remove non-digit characters
                          }
                        }}>
                    </div>
                    {#if newno.Phno.length <10}
                    <p style="color: red;font-weight:bold">Enter 10 Digits Only</p>
                    {/if}
                  {/each}
                  </div>
              <div class="flex-item">
                <!-- From Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.From_Date} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today'}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                  </div>
                {/each}
              </div>
              <div class="flex-item">
                <!-- To Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.To_Date} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',defaultDate: "today"}} placeholder="Select To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                    {#if newnumber.length > 1}
                    <button class="btn btn-danger" on:click={() => remove(index)}>-</button>
                    {/if}
                    {#if index === newnumber.length - 1}
                    <button class="btn btn-primary" id="button-addon2" on:click={for_caf}>+</button>
                    {/if}
                  </div>
                {/each}
              </div>
              </div>
              {/if}
      
      
              {#if requesttype=== "IMEI CDR"}
              <div id="flex-container1">
                <div class="flex-item">    
              {#each newnumber as newno, index}
                <div class="input-group mb-1 border-0">
                  <input class="form-control" bind:value={newno.IMEI} placeholder="enter IMEI" 
                  aria-label="enter phone number" aria-describedby="button-addon2" on:input={(event) => handleInputs(event, index,"IMEI")} on:input={() => {
                    if (!/^[0-9]*$/.test(newno.IMEI)) {
                     newno.IMEI = newno.IMEI.replace(/[^0-9]/g, ''); // Remove non-digit characters
                       }
                     }}
                  maxlength="15">
                </div>
              {/each}
              </div>
              <div class="flex-item">
                <!-- From Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group border-0">
                    <div class="dropdown" id={`dropdown-${index}`}>
                      <input type="text" class="form-control" style='margin-top:2px' placeholder="Select Providers" readonly on:click={()=> toggleDropdown(index)} bind:value={newno.ISP}>
                      <div class="dropdown-menu ml-3" style="{newno.showDropdown ? 'display: block;' : 'display: none; margin-left: 0.5rem!important'}">
                        <button type="button" class="clear btn btn-outline-danger ml-1" on:click={()=> clearCheckboxes1(index)}><i class="bi bi-x-square"></i></button>
                        <button type="button" class="clear btn btn-outline-success ml-1" on:click={()=> selectallCheckboxes1(index)}><i class="bi bi-check2-square"></i></button><br>       
                        <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Jio" name="provider[]" value="Jio" on:change={()=> updateSelectedCount(index, 'Jio')}>
                        <label style="display: inline-block;" for="provider_Jio">Jio</label><br>
                        <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_Airtel" name="provider[]" value="Airtel" on:change={()=> updateSelectedCount(index, 'Airtel')}>
                        <label style="display: inline-block;" for="provider_Airtel">Airtel</label><br>
                        <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_VI" name="provider[]" value="Vodafone" on:change={()=> updateSelectedCount(index,'Vodafone')}>
                        <label style="display: inline-block;" for="provider_VI">Vodafone</label><br>
                        <input class="check2 ml-2" style="margin-left: 0.5rem!important" type="checkbox" id="provider_CO" name="provider[]" value="Cellone" on:change={()=> updateSelectedCount(index,'Cellone')}>
                        <label style="display: inline-block;" for="provider_CO">Cellone</label><br>
                      </div>
                    </div>
                  </div>
                {/each}
              </div>
      
              <div class="flex-item">
                <!-- From Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.From_Date} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today'}} placeholder="From Date" on:input={(event) => handleInputs(event, index,"From_Date")} >
                  </div>
                {/each}
              </div>
              <div class="flex-item">
                <!-- To Dates Section -->
                {#each newnumber as newno, index}
                  <div class="input-group mb-1 border-0">
                    <input class="form-control" bind:value={newno.To_Date} use:flatpickr={{ dateFormat: "d/m/Y",minDate: mindate,maxDate: 'today',defaultDate: "today"}} placeholder="Select To Date" on:input={(event) => handleInputs(event, index,"To_Date")} >
                    {#if newnumber.length > 1}
                    <button class="btn btn-danger" on:click={() => remove(index)}>-</button>
                    {/if}
                    {#if index === newnumber.length - 1}
                    <button class="btn btn-primary" id="button-addon2" on:click={handleInput}>+</button>
                    {/if}
                  </div>
                {/each}
              </div>
              </div>
              {/if}
       
      {/if} 
      
           
      {#if requesttype === "CDR" || newtype === 'Phone'}     
        {#if records.length > 0}
              <div class="col-auto scroll-table">
                <table class="table table-bordered">
                  <tr>
                      <th>Phone</th>
                      <th>Nickname</th>
                      <th>From_Date</th>
                      {#if requesttype === "GPRS" || requesttype === "IPDR"}
                      <th>From_Time</th>
                      <th>To_Time</th>
                      {/if}
                      <th>To_Date</th>
                      <th></th>
                  </tr>
                  {#each records as record, index}
                      <tr>
                          <td> {record.Phno}</td>
                          <td><input type="text" style="margin-top: -1px;" class="border-0" id="fetchnickname{index}" bind:value={newnumber[index]["Nickname"]}></td>
                          <td>{record.From_Date}</td>
                          {#if requesttype === "GPRS" || requesttype === "IPDR"}
                          <td>{record.From_Time}</td>
                          <td>{record.To_Time}</td>
                          {/if}
                          <td>{record.To_Date}</td>
                          <td>
                            {#if newnumber[index]["Nickname"] === '' || newnumber[index]["Nickname"] === '___'}
                            <div class="spinner-border text-primary" role="status" id='fetchnickname{index}'>
                              <span class="sr-only"></span>
                            </div>
                            {/if}
                          </td>
                      </tr>
                    
                  {/each}
                </table>
              </div>
          {/if}
      {:else if requesttype === "SDR"}
         {#if records.length > 0}
         <div class="col-auto scroll-table">
              <table class="table table-bordered">
                <tr>
                    <th>Phone</th>
                    <th>MNP</th>
                </tr>
                {#each records as record}
                    <tr>
                      <td> {record.Phno}</td>
                      <td> {record.MNP}</td>
                    </tr>
                {/each}
              </table>
            </div>
          {/if}
      {:else if requesttype === "CAF"}
          {#if records.length > 0}
          <div class="col-auto scroll-table">
                <table class="table table-bordered">
                  <tr>
                      <th>Phone</th>
                      <th>CAF</th>
                      <th>MNP</th>
                  </tr>
                  {#each records as record}
                      <tr>
                        <td> {record.Phno}</td>
                        <td> {record.CAF}</td>
                        <td> {record.MNP}</td>
                      </tr>
                  {/each}
                </table>
              </div>
            {/if}
      {:else if requesttype === "IMEI CDR" || newtype === 'IMEI'}
          {#if records.length > 0}
          <div class="col-auto scroll-table">
                <table class="table table-bordered">
                  <tr>
                      <th>IMEI</th>
                      <th>ISP</th>
                      {#if requesttype === 'GPRS' || requesttype === 'IPDR'}
                      <th>From Time</th>
                      <th>To Time</th>
                      {/if}
                      <th>From Date</th>
                      <th>To Date</th>
                  </tr>
                  {#each records as record}
                      <tr>
                        <td> {record.IMEI}</td>
                        <td>{record.ISP}</td>
                        {#if requesttype === 'GPRS' || requesttype === 'IPDR'}
                        <td> {record.From_Time}</td>
                        <td> {record.To_Time}</td>
                        {/if}
                        <td> {record.From_Date}</td>
                        <td> {record.To_Date}</td>

                      </tr>
                  {/each}
                </table>
              </div>
            {/if}
      {:else if (requesttype === "GPRS" && (newtype === 'IPV6' || newtype === 'IPV4')) || (requesttype === "IPDR" && (newtype === 'IPV6' || newtype === 'IPV4'))}
          {#if records.length > 0}
          <div class="col-auto scroll-table">
                <table class="table table-bordered">
                  <tr>
                      <th>IP Address</th>
                      <th>ISP</th>
                      <th>From Time</th>
                      <th>To Time</th>
                      <th>From Date</th>
                      <th>To Date</th>
                  </tr>
                  {#each records as record}
                      <tr>
                        <td> {record.IP_Address}</td>
                        <td> {record.ISP}</td>
                        <td> {record.From_Time}</td>
                        <td> {record.To_Time}</td>
                        <td> {record.From_Date}</td>
                        <td> {record.To_Date}</td>
                      </tr>
                  {/each}
                </table>
              </div>
            {/if}
            <!-- (requesttype === "IPDR" && newtype === 'Retailer/Dealer Details' || newtype === 'IPV4')) -->
      {:else if (requesttype === "RH" && newtype === 'Retailer/Dealer Details')}
          {#if records.length > 0}
            <div class="col-auto scroll-table">
                  <table class="table table-bordered">
                    <tr>
                        <th>Dealer Details</th>
                        <th>Dealer Code</th>
                        <th>ISP</th>
                        <th>From Date</th>
                        <th>To Date</th>
                    </tr>
                    {#each records as record}
                        <tr>
                          <td> {record.RH_Dealer}</td>
                          <td> {record.RH_code}</td>
                          <td> {record.ISP}</td>
                          <td> {record.From_Date}</td>
                          <td> {record.To_Date}</td>
                        </tr>
                    {/each}
                  </table>
                </div>
              {/if}
      {:else if requesttype === "POA" && newtype === 'Retailer/Dealer Details'}
          {#if records.length > 0}
              <div class="col-auto scroll-table">
                    <table class="table table-bordered">
                      <tr>
                          <th>Dealer Details</th>
                          <th>Dealer Code</th>
                          <th>ISP</th>
                          <th>From Date</th>
                          <th>To Date</th>
                      </tr>
                      {#each records as record}
                          <tr>
                            <td> {record.POA_Dealer}</td>
                            <td> {record.POA_code}</td>
                            <td> {record.ISP}</td>
                            <td> {record.From_Date}</td>
                            <td> {record.To_Date}</td>
                          </tr>
                      {/each}
                    </table>
                  </div>
              {/if}
      {:else if (requesttype === "TOWER CDR" || requesttype === "TOWER GPRS" || requesttype === "TOWER IPDR") && newtype === 'CGI'}
            {#if records.length > 0}
                <div class="col-auto scroll-table">
                      <table class="table table-bordered">
                        <tr>
                            <th>CGI</th>
                            <th>ISP</th>
                            <th>From Date</th>
                            <th>To Date</th>
                        </tr>
                        {#each records as record}
                            <tr>
                              <td>{record.CGI}</td>
                              <td>{record.ISP}</td>
                              <td>{record.From_Date}</td>
                              <td>{record.To_Date}</td>
                            </tr>
                        {/each}
                      </table>
                    </div>
                {/if}
      {:else if (requesttype === "TOWER CDR" || requesttype === "TOWER GPRS" || requesttype === "TOWER IPDR") && newtype === 'Co-Ordinates'}
            {#if records.length > 0}
                <div class="col-auto scroll-table">
                      <table class="table table-bordered">
                        <tr>
                            <th>Latitude</th>
                            <th>Longitude</th>
                            <th>Rad</th>
                            <th>From Date</th>
                            <th>To Date</th>
                        </tr>
                        {#each records as record}
                            <tr>
                              <td>{record.Latitude}</td>
                              <td>{record.Longitude}</td>
                              <td>{record.Rad}</td>
                              <td>{record.From_Date}</td>
                              <td>{record.To_Date}</td>
                            </tr>
                        {/each}
                      </table>
                    </div>
                {/if}
      {/if}
          <br>
          <div class="uni">
           
          <input type="file" accept=".csv,.xlsx, .xls" on:change={handleFileUpload} id="excel_file"/>
      {#if records.length > 0}
          <p class="ml-2 mb-2" style = "color:green;">File Uploaded......</p>
      {/if}
          </div>
             
          </div>
          <!-- {#if requesttype !== 'IMEI CDR' && newtype !== 'IMEI'}
          <div class="row mb-3">
            <label class="col-sm-3 col-form-label">MODULE NAME</label>
            {#if userDetails.team === "ISOT"}
            <select class="col-sm-4" bind:value={module} on:change={again_check} >
              <option value="">Select Module Name</option>
              <option value="BJSAC">BJSAC</option>
              <option value="DK">DK</option>
              <option value="NRB">NRB</option>
              <option value="ORSC">ORSC</option>
              <option value="TSC">TSC</option>
              <option value="WGSZC">WGSZC</option>
              <option value="OTHER">OTHER</option>
            </select>
            {:else if userDetails.team === "AP"}
            <select class="col-sm-4 " bind:value={module} on:change={again_check} >
              <option value="">Select Module Name</option>
              <option value="AP">AP</option>
              <option value="OTHER">OTHER</option>
            </select>
            {:else if userDetails.team === "CAT"}
            <select class="col-sm-4 " bind:value={module} on:change={again_check} >
              <option value="">Select Module Name</option>
              <option value="CAT">CAT</option>
              <option value="OTHER">OTHER</option>
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
          </div> -->
          {#if requesttype !== "CDR" && requesttype !== "POA"&& requesttype !== "RH" && requesttype !== "GPRS" && requesttype !== "IPDR" && requesttype !== "TOWER CDR" && requesttype !== "TOWER GPRS" && requesttype !== "TOWER IPDR"}
          <div class="row mb-3">
            <label class="col-sm-3 col-form-label">NICKNAME</label>
            <input class="col-sm-4 border-0" bind:value={nickname} readonly>
          </div>
          {/if}
       
          <!-- <div class="row mb-3">
            <label class="col-sm-3 col-form-label">SUSPECT CATEGORY</label> 
            <select class="col-sm-4" display_func={o => o} bind:value={suspect}>
              <option selected value="">Select </option>
              <option value="A">A</option>
              <option value="B">B</option>
              <option value="C">C</option>
              <option value="D">D</option>
              <option value="UNKNOWN">UNKNOWN</option>      
          </div>
          <div class="row mb-3">
            <label class="col-sm-3 col-form-label">SOURCE TYPE</label> 
            <select class="col-sm-4" display_func={o => o} bind:value={source}>
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
            </div>
          <div class="row mb-3">
            <label class="col-sm-3 col-form-label">REASON FOR OBTAINING</label> 
            <select class="col-sm-4" display_func={o => o} bind:value={reason}>
              <option selected value="">Select</option>
              <option value="FOR FURTHER ANALYSIS">FOR FURTHER ANALYSIS</option>
              <option value="FOR UPDATING">FOR UPDATING</option>
              <option value="FOR ROAMING DATA">FOR ROAMING DATA</option>
              <option value="FOR OTHER PARTY DETAILS">FOR OTHER PARTY DETAILS</option>
              <option value="IMEI">IMEI</option>
              <option value="PICKUP">PICKUP</option>
              <option value="OTHER">OTHER</option>
          </div> -->
          <div class="row mb-3">
            <label class="col-sm-3 col-form-label">REF NO - DATE</label> 
            <input class="col-sm-4 border-0" placeholder="REF NO" type="text" bind:value={refno}> 
            <select class="col-sm-2" style='margin-left:20px' display_func={o => o} bind:value={refdate}>
              <option value="">Select </option>
              <option selected value="{year}">{year}</option>
              <option value="{year-1}">{year-1}</option>
              <option value="{year-2}">{year-2}</option>
              <option value="{year-3}">{year-3}</option>
          </div>
          
            
  {:else if requestcategory === "Note"}
  <div class="row mb-3">
    <label class="col-sm-3 col-form-label"></label> 
    <button class="col-sm-2 btn btn-outline-warning text-dark" style="margin-left:100px;margin-top:20px;font-weight:bold" data-bs-toggle="modal" data-bs-target="#note"> Generate Note</button>
  </div>
  {#if save !== ''}
  <div class="row mb-3">
    <label class="col-sm-3 col-form-label"></label> 
    <p class="col-sm-3" style="margin-left:100px;margin-top:20px;color: green;font-weight:bold">{save}</p>
    </div>
  {/if}
      <div class="modal fade" id="note" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" style="max-width: 1774px;">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="staticBackdropLabel">Analysis Note Generation</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <div class="container-xl">
                <div class="tophead d-flex justify-content-end">
                  <p>Secret</p>
                </div>
                <div class="form-header">
                  <div class="left-header" style="margin-top: -50px;margin-left: 20px;">No: <input placeholder="Enter No." type="text" bind:value={note_refno} class="refno"></div>
                  <div class="right-header" style="margin-top: -50px;margin-right: 20px;">Date: {formattedDate}</div>
                </div>
                <div></div>
                <div class="reciever">
                  <div class="d-flex">
                    <p>ANALYSIS TYPE</p><p style="margin-left: 74px;">:</p>
                    <input type="text" class="form-control Analysis-input" bind:value={analysis_type} placeholder="Analysis Type"/>
                  </div>
                  <div class="d-flex">
                    <p>ANALYST</p><p style="margin-left: 122px;">:</p>
                    <input type="text" class="form-control Analysis-input" placeholder="Officer Name" bind:value={userDetails.officername}/>
                  </div>
                  <div class="d-flex">
                    <p>INPUT/REQUEST RAISED</p><p style="margin-left: 10px;">:</p>
                   <input type="text" class="form-control Analysis-input" bind:value={user_details}>
                  </div>
                </div>
                <div class="summury1">
                  <textarea class="form-control textarea1" bind:value={summary1}  placeholder="Enter Summary"></textarea>
                </div>
                <div class="table-container">
                          <table class="table table-bordered" style="border-color: black;border:1px solid black;user-select:none;">
                            <thead style="text-align: center;vertical-align:middle;border-bottom:black">
                              <tr>
                                <th>S.No.</th>
                                <th>PHONE</th>
                                <th>SDR</th>
                                <th>TARGET PHONE NUMBER</th>
                                <th>VOIP DETAILS</th>
                                <th>SDB CNTS</th>
                                <th>MOST FREQUENT LOCATIONS /SUSPECT LOCATIONS</th>
                                <th>REMARKS</th>
                                <th>CATEGORY</th>
                              </tr>
                            </thead>
                            {#each proforma_data as newno, i}
                              <tr>
                                <td>{i + 1}</td>
                                <td><input  class="form-control" bind:value={newno.phone} placeholder="Enter Phone No." on:input={() => {
                                  if (!/^[0-9]*$/.test(newno.IMEI)) {
                                   newno.IMEI = newno.phone.replace(/[^0-9]/g, ''); // Remove non-digit characters
                                     }
                                   }}
                                maxlength="10"></td>
                                <td>
                                  <textarea class="form-control textarea" on:input={resizeTextarea} bind:value={newno.sdr} placeholder="Enter SDR"></textarea>
                                </td>
                                <td>
                                  <textarea class="form-control textarea" on:input={resizeTextarea} bind:value={newno.target_number} placeholder="Enter Target Number"></textarea>
                                </td>
                                <td>
                                  <textarea class="form-control textarea" on:input={resizeTextarea} bind:value={newno.voip} placeholder="Enter VOIP"></textarea>
                                </td>
                                <td>
                                  <textarea class="form-control textarea" on:input={resizeTextarea} bind:value={newno.sdb} placeholder="Enter SDB"></textarea>
                                </td>
                                <td>
                                  <textarea class="form-control textarea" on:input={resizeTextarea} bind:value={newno.FLSL} placeholder="Enter FLSL"></textarea>
                                </td>
                                <td>
                                  <textarea class="form-control textarea" on:input={resizeTextarea} bind:value={newno.remarks} placeholder="Enter Remarks"></textarea>
                                </td>
                                <td>
                                  <div class="d-flex">
                                    <textarea class="form-control textarea" on:input={resizeTextarea} bind:value={newno.category} placeholder="Enter Category"></textarea>
                                    <div style="margin-left: 1px;">
                                      {#if proforma_data.length > 1}
                                        <button class="btn btn-danger" on:click={() => remove2(i)}>-</button>
                                      {/if}
                                    </div>
                                    <div style="margin-left: 1px;">
                                      {#if i === proforma_data.length - 1}
                                        <button class="btn btn-primary" id="button-addon2" on:click={handleInput2}>+</button>
                                      {/if}
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            {/each}
                          </table>
                    </div>
                    <div class="summury2" style="margin-top: 20px;">
                      <textarea class="form-control textarea1" bind:value={summary2}  placeholder="Enter Summary"></textarea>
                    </div>
                    <div class="form-footer">
                      <div class="left-footer" style="margin-left: 17px;">
                       SP (Admin) :
                        
                      </div>
                      <div class="right-footer" style="margin-left: 254px;">
                        DSP(Tech) :
                      </div>
                    </div>
                    </div>
                    </div>
                    <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                      <button type="button" class="btn btn-primary" data-bs-dismiss="modal" on:click={note_save}>Save</button>
                    </div>
                  </div>
                </div>
      </div>
  {/if}
  <div class="row mb-3">
    <label class="col-sm-3 col-form-label">PRIORITY</label> 
    <select class="col-sm-4" display_func={o => o} bind:value={priority}>
      <option selected value="">Select </option>
      <option value="Normal">Normal</option>
      <option value="High">High</option>
      <option value="Emergency">Emergency</option>
    </select>
  </div>
  <div class="row mb-3">
  </div>
  <div class="row mb-3">
    <label class="col-sm-3 col-form-label">REMARK</label> 
    <textarea class="col-sm-4 border-0" rows="3" id="comment" bind:value={remarks}></textarea>
  </div>
      {#if requestcategory === "Data Request" || requestcategory === ""}
        <div class="text-center">
            <button
            on:click={newform}
            style="box-shadow: 0 .5rem 1rem rgb(0,0,0)!important;"
            class="btn-outline-success rounded mt-5 p-2"
            type="submit">Submit</button>
          </div>
          {:else if requestcategory === "Analysis Request"}
          <div class="text-center">
            <button
            on:click={newanalysis}
            style="box-shadow: 0 .5rem 1rem rgb(0,0,0)!important;"
            class="btn-outline-success rounded mt-5 p-2"
            type="submit">Submit</button>
          </div>
          {:else if requestcategory === "Note"}
          <div class="text-center">
            <button
            on:click={note_create}
            style="box-shadow: 0 .5rem 1rem rgb(0,0,0)!important;"
            class="btn-outline-success rounded mt-5 p-2"
            type="submit">Submit</button>
          </div>
          {/if}
      </form>
      </div>
      </div>
      <div class="flex flex-col container items-center mt-10">
        <ToastContainer let:data={data}>
          <!-- Apply additional styles for width and styling -->
          
          <FlatToast {data}/>
        </ToastContainer>
      </div>
      </main>