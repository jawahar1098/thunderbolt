<script> 
  // @ts-nocheck
  
    // import "../global.css";
    import { onMount, onDestroy } from "svelte";
    import { goto } from "$app/navigation";
    import { basepath } from "$lib/config";
    import { generatePDF } from "$lib/annexe";
    import { page } from "$app/stores";
  
    import { userDetailsStore } from "$lib/datastore.js";
    console.log("userDetailsStore", userDetailsStore);
    let userDetails;
  
    userDetailsStore.subscribe((value) => {
      userDetails = value;
      console.log("value", value);
    });
  
    console.log("demo", userDetails);
    onMount(() => {
      // beware of truthy and falsy values
      if (localStorage.getItem("userAuth") === "true") {
        // console.log("jsno",localStorage.getItem("userDetails"))
        // console.log('auth is passed')
        userDetailsStore.set(JSON.parse(localStorage.getItem("userDetails")));
      } else {
        goto("/");
      }
    });
  
    onMount(() => {
      // beware of truthy and falsy values
      if (localStorage.getItem("userAuth") === "true") {
        // console.log('auth is passed')
      }
    });
    const today = new Date();
    const year = today.getFullYear(); // Get the four-digit year
    const month = String(today.getMonth() + 1).padStart(2, "0"); // Get the month (0-11) and add leading zero if necessary
    const day = String(today.getDate()).padStart(2, "0"); // Get the day of the month and add leading zero if necessary
    let id;
    const url = $page.url;
    id = url.search.replace("?id=", "");
    console.log(id);
    
    let refno = '';
    let officername = '';
    let analysis_type = '';
    let user_details = '';
    let summary1 = '';
    let summary2 = '';
    let date = ''
    // $: user_details = (`${cases.team} / ${cases.officername} / ${cases.designation} / ${cases.date}`)
    let cases = [];
    let proforma_data = [{
            phone: '',
            sdr: '',
            target_number: '',
            voip: '',
            sdb: '',
            FLSL: '',
            remarks: '',
            category: '',
            summary1: '',
            summary2: '',
            raised_by: '',
          }];
  
  async function analysis_proform() {
    const response = await fetch(basepath() + `/analysis_proform`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id: id,
      }),
    });
  
    if (response.ok) {
      cases = await response.json();
      for (let i = 0; i < cases.newnumber.length; i++) {
        const data = cases.newnumber[i];
  
        // Ensure that proforma_data has enough objects
        if (!proforma_data[i]) {
          proforma_data[i] = {
            phone: '',
            sdr: '',
            target_number: '',
            voip: '',
            sdb: '',
            FLSL: '',
            remarks: '',
            category: '',
          };
        }
  
        proforma_data[i]['phone'] = data.Phno;
      }
      if(cases.hasOwnProperty('proforma_data') && cases.proforma_data.length > 0){
        console.log(cases)
        proforma_data = cases.proforma_data[0]['data'];
        refno = cases.proforma_data[0]['refno'];
        officername = cases.proforma_data[0]['officername'];
        analysis_type = cases.proforma_data[0]['analysistype'];
        summary1 = cases.proforma_data[0]['summary1'];
        summary2 = cases.proforma_data[0]['summary2'];
        user_details = (cases.proforma_data[0]['raised_by'] || (`${cases.team} / ${cases.officername} / ${cases.designation} / ${cases.date}`));
        date = cases.date;
        console.log(cases);
      }
      else{
        user_details = (`${cases.team} / ${cases.officername} / ${cases.designation} / ${cases.date}`)
        date = cases.date;
    }
  }
}
  onMount(() => {
    analysis_proform();
  });
  
    async function analysis_proform_save(){
      const response = await fetch(basepath() + `/analysis_proform_save`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          id: id,
          refno:refno,
          type:analysis_type,
          officer : userDetails.officername,
          summary1: summary1,
          summary2: summary2,
          raised_by: user_details,
          data : proforma_data
        }),
      });
        const result = await response.json();
        if (result.result){
          alert('Analysis Proforma Save Successfully!!!!!')
          goto('/ticketing/Analysisreq/')
        }
        else{
          alert('Please Fill All Fields!!!')
        }
      }
      function close(){
        goto('/ticketing/Analysisreq/');
      }
  </script>
  
  <main>
    {#if userDetails.role === 'Analyst' && userDetails.team === 'CAT' && (cases.pending === 'Report Generated' || cases.pending === '--')}
        <div class="container-xl">
          <div class="tophead d-flex justify-content-end">
            <p>Secret</p>
          </div>
          <div class="form-header">
            <div class="left-header" style="margin-top: 5px;margin-left: 20px;">No: <input placeholder="Enter No." type="text" bind:value={refno} class="refno"></div>
            <div class="right-header" style="margin-top: 5px;margin-right: 20px;">Date: {cases.date}</div>
          </div>
          <div class="head">
            <h5><b>NOTE</b></h5>
          </div>
          <div class="reciever">
            <div class="d-flex">
              <p>ANALYSIS TYPE</p><p style="margin-left: 74px;">:</p>
              <input type="text" class="form-control Analysis-input" bind:value={analysis_type} placeholder="Analysis Type"/>
            </div>
            <div class="d-flex">
              <p>ANALYST</p><p style="margin-left: 122px;">:</p>
              <input type="text" class="form-control Analysis-input" placeholder="Officer Name" bind:value={userDetails.officername} readonly/>
            </div>
            <div class="d-flex">
              <p>INPUT/REQUEST RAISED</p><p style="margin-left: 10px;">:</p>
              <!-- <input type="text" class="form-control Analysis-input" placeholder="team, officer Designation and date" value="{cases.team}"/> -->
              <p class="Analysis-input">
                <input type="text" bind:value={user_details} style="width: 300px;">
              </p>
            </div>
          </div>
          <div class="summury2" style="margin-top: 20px;border:1px solid lightgrey">
            <textarea class="form-control textarea1" bind:value={summary1}  placeholder="Enter Summary"></textarea>
          </div>
  
          <div class="table-container">
            <table class="table table-bordered" style="border-color: black;border:1px solid black;user-select:none;">
              <thead style="text-align: center;vertical-align:middle;border-bottom:black">
                <tr>
                  <th>S.No.</th>
                  <th style="width: 100px;">PHONE</th>
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
                  <td>{newno.phone}</td>
                  <td>
                    <textarea class="form-control" bind:value={newno.sdr} placeholder="Enter SDR"></textarea>
                  </td>
                  <td>
                    <textarea class="form-control" bind:value={newno.target_number} placeholder="Enter Target Number"></textarea>
                  </td>
                  <td>
                    <textarea class="form-control" bind:value={newno.voip} placeholder="Enter VOIP"></textarea>
                  </td>
                  <td>
                    <textarea class="form-control" bind:value={newno.sdb} placeholder="Enter SDB"></textarea>
                  </td>
                  <td>
                    <textarea class="form-control" bind:value={newno.FLSL} placeholder="Enter FLSL"></textarea>
                  </td>
                  <td>
                    <textarea class="form-control" bind:value={newno.remarks} placeholder="Enter Remarks"></textarea>
                  </td>
                  <td>
                    <textarea class="form-control" bind:value={newno.category} placeholder="Enter Category"></textarea>
                  </td>
                </tr>
              {/each}
            </table>
          </div>
          <div class="summury2" style="margin-top: 57px; border:1px solid lightgrey;">
            <textarea class="form-control textarea1" bind:value={summary2}  placeholder="Enter Summary"></textarea>
          </div>
          <div class="form-footer">
            <div class="left-footer" style="margin-left: 20px;">
             SP (Admin) :
            </div>
            <div class="right-footer" style="user-select:none;">
              DSP(Tech) :
            </div>
          </div>
          <div style="margin-top: -5px;padding:50px" class="d-flex justify-content-end">
            <span>1</span>
          </div>
          <div class="d-flex" style="justify-content: center;">
            <div>
              <button class="btn btn-outline-success" style="width: 80px;" on:click={analysis_proform_save}><i class="bi bi-floppy-fill"></i> Save</button>
            </div>
            <div>
              <button class="btn btn-outline-danger" style="width: 90px;" on:click={close}><i class="bi bi-x-square-fill"></i> Close</button>
            </div>
          </div>
        </div>
    
  
    {:else if userDetails.role === 'Analyst' && userDetails.team === 'CAT' && (cases.pending === 'Analysis Note Raised'|| cases.approval === 'Note Approved by SP'  || cases.approval === 'Report Approved by SP' || cases.pending === 'SP Approval Pending' || cases.pending === `${userDetails.superior} Approval Pending` || cases.pending === 'ADDL-SP/DSP Approval Pending') ||
         userDetails.designation === "SP" && userDetails.team === 'ADMIN' ||
         userDetails.designation === 'ADDL-SP/DSP' && userDetails.team === 'CAT' ||
         userDetails.designation === 'INSPR' && userDetails.team === 'CAT'}
        <div class="container-xl ">
          <div class="tophead d-flex justify-content-end">
            <p>Secret</p>
          </div>
          <div class="form-header">
            <div class="left-header" style="margin-top: 5px;margin-left: 20px;">No: {refno}</div>
            <div class="right-header" style="margin-top: 5px;margin-right: 20px;">Date: {date}</div>
          </div>
          <div class="head">
            <h5><b>NOTE</b></h5>
          </div>
          <div class="reciever">
            <div class="d-flex">
              <p>ANALYSIS TYPE</p><p style="margin-left: 74px;">: {analysis_type}</p>
              <!-- <input type="text" class="form-control Analysis-input" bind:value={analysis_type} placeholder="Analysis Type"/> -->
            </div>
            <div class="d-flex">
              <p>ANALYST</p><p style="margin-left: 122px;">: {officername}</p>
              <!-- <input type="text" class="form-control Analysis-input" placeholder="Officer Name" bind:value={userDetails.officername} readonly/> -->
            </div>
            <div class="d-flex">
              <p>INPUT/REQUEST RAISED</p><p style="margin-left: 10px;">: {user_details}</p>
              <!-- <input type="text" class="form-control Analysis-input" placeholder="team, officer Designation and date" value="{cases.team}"/> -->
              <!-- <p class="Analysis-input">{cases.team} / {cases.officername} / {cases.designation} / {cases.date}</p> -->
              
            </div>
          </div>
          <div class="summury2" style="margin-top: 20px;border:1px solid lightgrey">
            <textarea class="form-control textarea1" bind:value={summary1}  placeholder="Enter Summary" readonly></textarea>
          </div>
          <div class="table-container">
            <table class="table table-bordered" style="border-color: black;border:1px solid black;user-select:none;">
              <thead style="text-align: center;vertical-align:middle;border-bottom:black">
                <tr>
                  <th>S.No.</th>
                  <th style="width: 100px;">PHONE</th>
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
                  <td>{newno.phone}</td>
                  <td class="td">
                    {newno.sdr}
                    <!-- <textarea class="form-control" bind:value={newno.sdr} placeholder="Enter SDR"></textarea> -->
                  </td>
                  <td class="td">
                    {newno.target_number}
                    <!-- <textarea class="form-control" bind:value={newno.target_number} placeholder="Enter Target Number"></textarea> -->
                  </td>
                  <td class="td">
                    {newno.voip}
                    <!-- <textarea class="form-control" bind:value={newno.voip} placeholder="Enter VOIP"></textarea> -->
                  </td>
                  <td class="td">
                    {newno.sdb}
                    <!-- <textarea class="form-control" bind:value={newno.sdb} placeholder="Enter SDB"></textarea> -->
                  </td>
                  <td class="td">
                    {newno.FLSL}
                    <!-- <textarea class="form-control" bind:value={newno.FLSL} placeholder="Enter FLSL"></textarea> -->
                  </td>
                  <td class="td">
                    {newno.remarks}
                    <!-- <textarea class="form-control" bind:value={newno.remarks} placeholder="Enter Remarks"></textarea> -->
                  </td>
                  <td class="td">
                    {newno.category}
                    <!-- <textarea class="form-control" bind:value={newno.category} placeholder="Enter Category"></textarea> -->
                  </td>
                </tr>
              {/each}
            </table>
          </div>
          <div class="summury2" style="margin-top: 57px; border:1px solid lightgrey;">
            <textarea class="form-control textarea1" bind:value={summary2}  placeholder="Enter Summary" readonly></textarea>
          </div>
          <div class="form-footer">
            <div class="left-footer"></div>
            <div class="right-footer">
              DSP(Tech) :
            {#if cases.approval === 'Report Approved by SP' || cases.approval === 'Note Approved by SP' || cases.approval === 'Report Approved by ADDL-SP/DSP' || cases.approval === 'Approved by ADDL-SP/DSP'}
            <div class="sign1">
              <img
              src="../src/public/Images/dsp_sign.png"
              alt="DSP SIGN"
              width="120"
              height="120"
              />
            </div>
            {/if}
             </div>
          </div>
          <div class="left-footer1" style="margin-left: 20px;">
            SP (Admin) :
            {#if cases.approval === 'Report Approved by SP' || cases.approval === 'Note Approved by SP'}
            <div class="sign1">
              <img
              src="../src/public/Images/sp_sign.png"
              alt="SP SIGN"
              width="120"
              height="120"
              />
            </div>
            {/if}
          </div>
          <div style="margin-top: -5px;padding:50px" class="d-flex justify-content-end">
            <span>1</span>
          </div>
          <div>
            <button class="btn btn-outline-danger" style="width: 90px;" on:click={close}><i class="bi bi-x-square-fill"></i> Close</button>
          </div>
        </div>
    {/if}
  
  </main>
    
  <style>
    .td{
      text-wrap: wrap;
      text-align: center;
    }
    .refno{
      width: 200px;
    }

    .form-control{
      background-color: transparent !important;
      border: none;
    }
    .tophead{
      margin-right: 190px;
      padding: 30px;
      margin-top: 50px;
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
.container {
    margin-top: 100px;
    width: 550% !important;
    box-shadow: 0 0.5rem 1rem rgb(0, 0, 0) !important;
    background-color: #f4f1f1;
    border-radius: 5px;
    margin-bottom: 50px;
    padding: 1 1 1 1;
  }
  .form-header {
    display: flex;
    margin-top: -10px;
    /* padding: 50px; */
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
    justify-content: space-between;
    margin-top: 190px;
  }

  .left-footer1 {
    margin-top: 65px;
    margin-left: 25px;
  }
  .left-footer2{
    margin-top: 260px;
  }
  .left-footer {
    flex: 1;
    margin-top: 10px;
  }
  .right-footer {
    /* color:#5961d8; */
    flex: 1;
    position: relative;
    display: inline-block;
    margin-top: -130px;
    text-align: center;
    margin-left: 530px;
  }
  .right-footer img {
    position: absolute;
    top: -66px;
    left: 50%;
    margin-top: -20px;
    margin-left: 20px;
    transform: translateX(-50%);
  }
  .head {
    text-align: center;
    margin-top: 5px;
    font-family: 'Times New Roman', Times, serif;
  }
  .subject {
    text-align: left;
    text-wrap: wrap;
    margin-left: 20px;
    margin-top: 10px;
    margin-bottom: 10px;
  }
  .sign1 {
    margin-top: -110px !important;
  }
  table,
  th,
  td {
    /* padding: 0 0 0 0; */
    border: 1px solid black;
    margin-left: 20px;
    margin-right: 20px;
  }

  .table-container {
    display: flex;
    width: 1147px;
    margin-left: -18px;
    margin-right: 20px;
    margin-top: 50px;
    }
  .reciever {
    margin-top: 50px;
    margin-bottom: 10px;
    margin-left: 50px;
  }
  button {
    margin-left: 48%;
    margin-bottom: 20px;
    margin-top: 10px;
  }
  main{
  user-select: none;
  /* background-color: lightgoldenrodyellow; */
  }
.demo{
  font-family:kafenot;
  transform: rotate(-45deg);
  position: absolute;
    top: -30px;
    /* left: 50%; */
    margin-top: 20px;
    margin-left: 130px;
  color:#3600AD;
  font-weight: bold;
}

.date_flex{
  transform: rotate(-45deg);
  margin-top: -66px;
  margin-left: 60px;
  /* margin-right: -20px; */
  /* text-align:center; */
  color:#3600AD;
  font-weight: bold;
}
.date_flex_2{
  transform: rotate(-45deg);
  margin-top: -26px;
  margin-left: 590px;
  margin-right: -20px;
  /* text-align:center; */
  color:#3600AD;
  font-weight: bold;
}

.dates{
  /* display: flex; */
  width: 14px;
}
.dash{
  /* display: flex; */
  width: 10px;
}
  </style>