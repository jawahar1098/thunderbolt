<script>
    // @ts-nocheck
 
 //   import '../global.css';
    import {onMount , onDestroy} from 'svelte';
    import {goto} from '$app/navigation';
    import {basepath } from "$lib/config"
    import { userDetailsStore } from '$lib/datastore.js';
    import 'flatpickr/dist/flatpickr.css';
    import Chart from 'chart.js/auto';
 
 
 let mindate;
 const today = new Date();
 
 const year = today.getFullYear(); // Get the four-digit year
 const month = String(today.getMonth() + 1).padStart(2, '0'); // Get the month (0-11) and add leading zero if necessary
 const day = String(today.getDate()).padStart(2, '0'); // Get the day of the month and add leading zero if necessary
 
 mindate = `${String(today.getDate() + 1).padStart(2, '0')}/${month}/${2021}`;
 
 let userDetails;
 
 userDetailsStore.subscribe(value => {
 userDetails = value;
 
 });
 
 
 onMount(() => {
 
 if (localStorage.getItem("userAuth")==="true"){
 
 userDetailsStore.set(JSON.parse(localStorage.getItem("userDetails")))
 
 selected_period('');
 }
 else{
 goto('/');
 }
 })
 
 let cases =[];
 let Total_raise;
 let Total_approval;
 let Total_pending;
 let Total_closed;
 let Total_under_process;
 let types = 'All';
 let status = 'All';
 let period_data = ''
 let date_range = ''
 async function report() {
   try {
     const response = await fetch(basepath() + '/report', {
       method: 'POST',
       headers: {
         'Content-Type': 'application/json'
       },
       body: JSON.stringify({
         team : userDetails.team,
         designation : userDetails.designation,
         role : userDetails.role,
         email : userDetails.email
       })
     });
     
     if (!response.ok) {
       throw new Error('Failed to fetch data');
     }
     
     const data = await response.json();
     cases = data.filter((user) => user)
     console.log(cases)
           Total_raise=cases[0]['Total_raise'].length;
           Total_approval=cases[0]['Total_approval'].length;
           Total_pending=cases[0]['Total_pending'].length;
           Total_closed=cases[0]['Total_close'].length;
           Total_under_process=cases[0]['Total_under_process'].length;
 
 
   status_count();
 
   } catch (error) {
     console.error(error);
   }
 }
 
 onMount(() => {
  
   if (localStorage.getItem("userAuth") === "true") {
   
     report()
   
   } else {
     goto('/Dashboard(T)');
   }
 })
 
 
 let chart;
 let chart2;
 let intervalId;
 
 const data1 = {
   labels: ['Total Raise Tickets', 'Total Approved Tickets', 'Total Pending Tickets','Total Tickets Closed','Total Under Process'],
   datasets: [
     {
       data: [Total_raise, Total_approval, Total_pending,Total_closed,Total_under_process],
       backgroundColor: ['#FFCE56', 'lightgreen', '#FF6384','darkgreen','grey'],
       hoverBackgroundColor: ['#FFCE56', 'lightgreen', '#FF6384','darkgreen','grey'],
     },
   ],
 };
 
 const data2 = {
   labels: ['Total Raise Tickets', 'Total Approved Tickets', 'Total Pending Tickets'],
   datasets: [
     {
       data: [12, 4, 3],
       backgroundColor: ['#FFCE56', 'lightgreen', '#FF6384'],
       hoverBackgroundColor: ['#FFCE56', 'lightgreen', '#FF6384'],
     },
   ],
 };
 
 const updateChartData = () => {
   data1.datasets[0].data = [Total_raise, Total_approval, Total_pending,Total_closed,Total_under_process];
   data2.datasets[0].data = [20, 4, 3];
   chart.update();
   chart2.update();
 };
 
 onMount(() => {
   const ctx = document.getElementById('myPieChart').getContext('2d');
   chart = new Chart(ctx, {
     type: 'doughnut', // Set chart type to doughnut
     data: data1,
     options: {
       cutoutPercentage: 50, // Adjust the cutout percentage to create a donut
       plugins: {
         legend: {
           position: 'right',
           align: 'center',
           labels: {
             boxWidth: 20,
             padding: 10,
           },
         },
       },
     },
   });
 
   const ctx2 = document.getElementById('myPieChart2').getContext('2d');
   chart2 = new Chart(ctx2, {
     type: 'doughnut', // Set chart type to doughnut
     data: data2,
     options: {
       cutoutPercentage: 50, // Adjust the cutout percentage to create a donut
       plugins: {
         legend: {
           position: 'right',
           align: 'center',
           labels: {
             boxWidth: 20,
             padding: 10,
           },
         },
       },
     },
   });
 
   chart.options.onClick = async function (event, elements) {
       if (elements.length > 0) {
         const datasetIndex = elements[0].datasetIndex;
         const index = elements[0].index;
         // Update variables based on the clicked section
         Total_raise = data1.datasets[datasetIndex].data[0];
         Total_approval = data1.datasets[datasetIndex].data[1];
         Total_pending = data1.datasets[datasetIndex].data[2];
 
         // Display information or perform actions as needed
         console.log(Clicked on ${data1.labels[index]}: ${data1.datasets[datasetIndex].data[index]} tickets);
         if (${data1.labels[index]} === 'Total Pending Tickets'){
           try {
                 const response = await fetch(basepath() + '/data_filters', {
                   method: 'POST',
                   headers: {
                     'Content-Type': 'application/json'
                   },
                   body: JSON.stringify({
                     team : userDetails.team,
                     designation : userDetails.designation,
                     role : userDetails.role,
                     email : userDetails.email,
                     types:types,
                     status:'Total_pending',
                     period:period_data,
                     date_range:date_range
                   })
                 });
                     
                 const data = await response.json();
                 filter_data = data
                 console.log(data,'data_filters')
               } catch (error) {
                 console.error(error);
               }
               // status_count();
         }
 
         else if (${data1.labels[index]} === 'Total Approved Tickets'){
           try {
                 const response = await fetch(basepath() + '/data_filters', {
                   method: 'POST',
                   headers: {
                     'Content-Type': 'application/json'
                   },
                   body: JSON.stringify({
                     team : userDetails.team,
                     designation : userDetails.designation,
                     role : userDetails.role,
                     email : userDetails.email,
                     types:types,
                     status:'Total_approval',
                     period:period_data,
                     date_range:date_range
                   })
                 });
                     
                 const data = await response.json();
                 filter_data = data
                 console.log(data,'data_filters')
               } catch (error) {
                 console.error(error);
               }
               // status_count();
         }
         else if (${data1.labels[index]} === 'Total Raise Tickets'){
           try {
                 const response = await fetch(basepath() + '/data_filters', {
                   method: 'POST',
                   headers: {
                     'Content-Type': 'application/json'
                   },
                   body: JSON.stringify({
                     team : userDetails.team,
                     designation : userDetails.designation,
                     role : userDetails.role,
                     email : userDetails.email,
                     types:types,
                     status:'Total_raise',
                     period:period_data,
                     date_range:date_range
                   })
                 });
                     
                 const data = await response.json();
                 filter_data = data
                 console.log(data,'data_filters')
               } catch (error) {
                 console.error(error);
               }
               // status_count();
         }
         else if (${data1.labels[index]} === 'Total Tickets Closed'){
           try {
                 const response = await fetch(basepath() + '/data_filters', {
                   method: 'POST',
                   headers: {
                     'Content-Type': 'application/json'
                   },
                   body: JSON.stringify({
                     team : userDetails.team,
                     designation : userDetails.designation,
                     role : userDetails.role,
                     email : userDetails.email,
                     types:types,
                     status:'Total_close',
                     period:period_data,
                     date_range:date_range
                   })
                 });
                     
                 const data = await response.json();
                 filter_data = data
                 console.log(data,'data_filters')
               } catch (error) {
                 console.error(error);
               }
               // status_count();
         }
 
         else if (${data1.labels[index]} === 'Total Under Process'){
           try {
                 const response = await fetch(basepath() + '/data_filters', {
                   method: 'POST',
                   headers: {
                     'Content-Type': 'application/json'
                   },
                   body: JSON.stringify({
                     team : userDetails.team,
                     designation : userDetails.designation,
                     role : userDetails.role,
                     email : userDetails.email,
                     types:types,
                     status:'Total_under_process',
                     period:period_data,
                     date_range:date_range
                   })
                 });
                     
                 const data = await response.json();
                 filter_data = data
                 console.log(data,'data_filters')
               } catch (error) {
                 console.error(error);
               }
         }
       }
     };
 
 
   intervalId = setInterval(updateChartData, 1000);
 });
 
 onDestroy(() => {
   clearInterval(intervalId);
 });
 
 let count = [];
 function status_count(){
 for (let i = 0; i < cases[0]['Total_raise'].length; i++) {
   const user = cases[0]['Total_raise'][i];
   const counts = [...new Set(user['result'].filter(user => user.status === 'Data_Received'))];
   count.push(counts)
 }
 console.log(count)
 }
 
 function selected_period(period){
   console.log("clear_range")
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
     period_data = ${date1} to ${date2};
     date_range = 'Date Range';
 
     
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
 
   function navigateToReports() {
  
     goto('ticketing/Dashboard');
   }
 
 </script>
 
 
 <main>
     <div class="container">
         <div class="main_card">
           <h2 style="text-align: 30px;">TICKETING Modules</h2>
           <!-- svelte-ignore a11y-no-static-element-interactions -->
           <!-- svelte-ignore a11y-click-events-have-key-events -->
           <div class="main_card2" on:click={() => navigateToReports()}>
             <h3 style="margin-left:50px">Data Requests</h3>
             <div class="pie">
               <canvas id="myPieChart"></canvas>
             </div>
           </div>
           <div class="main_card3" on:click={() => navigateToReports()}>
             <h3 style="margin-left:50px">Analysis Requests</h3>
             <div class="pie">
               <canvas id="myPieChart2"></canvas>
             </div>
           </div>
         </div>
     </div> 
     
     <div class="dashboard" >  
         <div class="board">
             <div class="row">
                 <div class="col-md-3 col-sm-6">
                     <div class="counter">
                         <div class="counter-icon">
                             <i class="bi bi-telephone-outbound-fill"></i>
                         </div>
                         <h3>Total Unique Source Count Cdr</h3>
                         <span class="counter-value">1136</span>
                     </div>
                 </div>
                 <div class="col-md-3 col-sm-6">
                     <div class="counter orange">
                         <div class="counter-icon">
                             <i class="bi bi-person-lines-fill"></i>
                         </div>
                         <h3>Imei Count Cdr</h3>
                         <span class="counter-value">1073</span>
                     </div>
                 </div>
                 <div class="col-md-3 col-sm-6">
                     <div class="counter green">
                         <div class="counter-icon">
                             <i class="bi bi-graph-up-arrow"></i>
                         </div>
                         <h3>Last Update Cdr</h3>
                         <span class="counter-value">1073</span>
                     </div>
                 </div>
                 <!-- <div class="col-md-3 col-sm-6">
                     <div class="counter blue">
                         <div class="counter-icon">
                             <i class="bi bi-globe-central-south-asia"></i>
                         </div>
                         <h3>Last Activation Dates By State Cdr</h3>
                         <span class="counter-value">1073</span>
                     </div>
                 </div> -->
             </div>
         </div>
     
 </main>
 
 <style>
 .container {
   display: flex;
   justify-content: space-around;
   height: 100%;
   margin-left: -80px;
 } 
 .main_card{
   /* border: 1px solid lightgray; */
   width:500px;
   margin-left:20px;
   margin-top: 20px;
   /* background:linear-gradient(#EEEEEE, #FAF8F9, #FFFFFF); */
 }
 .main_card2{
   /* border: 1px solid lightgray; */
   width:400px;
   height: 300px;
   border-right: none;
   border-left: none;
   margin-top: 20px;
   background:linear-gradient(#EEEEEE, #FAF8F9, #FFFFFF);
 }
 .main_card3{
   /* border: 1px solid lightgray; */
   width:400px;
   height: 300px;
   margin-top: 20px;
   border-left: none;
   background:linear-gradient(#EEEEEE, #FAF8F9, #FFFFFF);
 }
 .pie{
   width: 350px;
   height: 350px;
   margin-left: 10px;
   margin-top: -80px;
 }
 
 
  .counter{
     color: #eb3b5a;
     font-family: 'Muli', sans-serif;
     width: 250px;
     height: 250px;
     text-align: center;
     border-radius: 100%;
     padding: 77px 32px 40px;
     margin: 0 auto;
     position: fixed;
     z-index: 1;
     margin-left:700px;
     margin-top: -650px;
 }
 .counter:before,
 .counter:after{
     content: "";
     background: #fff;
     width: 80%;
     height: 80%;
     border-radius: 100%;
     box-shadow: -5px 5px 5px rgba(0,0,0,0.3);
     transform: translateX(-50%)translateY(-50%);
     position: absolute;
     top: 50%;
     left: 50%;
     z-index: -1;
     
 }
 .counter:after{
     background: linear-gradient(45deg,#B81242 49%, #D74A75 50%);
     width: 100%;
     height: 100%;
     box-shadow: none;
     transform: translate(0);
     top: 0;
     left: 0;
     z-index: -2;
     clip-path: polygon(50% 50%, 50% 0, 100% 0, 100% 100%, 0 100%, 0 50%);
 }
 .counter .counter-icon{
     color: #fff;
     background: linear-gradient(45deg,#B81242 49%, #D74A75 50%);
     font-size: 33px;
     line-height: 70px;
     width: 70px;
     height: 70px;
     border-radius: 50%;
     position: absolute;
     top:  0;
     left: 0;
     z-index: 1;
     transition: all 0.3s;
 }
 .counter .counter-icon i.bi{
     transform: rotateX(0deg);
     transition: all 0.3s ease 0s;
 }
 .counter:hover .counter-icon i.bi{ transform: rotateX(360deg); }
 .counter h3{
     font-size: 17px;
     font-weight: 700;
     text-transform: uppercase;
     margin: 0 0 3px;
 }
 .counter .counter-value{
     font-size: 30px;
     font-weight: 700;
 }
 .counter.orange{ color: #F38631; }
 .counter.orange:after,
 .counter.orange .counter-icon{
     background: linear-gradient(45deg,#F38631 49%,#F8A059 50%);
 }
 .counter.green{ color: #88BA1B; }
 .counter.green:after,
 .counter.green .counter-icon{
     background: linear-gradient(45deg,#88BA1B 49%,#ACD352 50%);
 }
 </style>