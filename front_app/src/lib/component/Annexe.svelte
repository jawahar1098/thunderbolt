<script>
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

  // console.log(cases)
  async function logout() {
    await fetch(basepath() + "/logout", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    // Set the authentication to false
    localStorage.setItem("userAuth", false);

    // Redirect the user to the login page after logging out
    goto("/");
  }

  let code;
  // console.log(userDetails.team)
  let paginatedNumbers = [];
  let itemsPerPage = 22;
  let id;
  let st;
  let data = [];
  let cases = [];
  let circle = 'ALL'
  let user = {
    newnumber: "",
  };
  const url = $page.url;
  id = url.search.replace("?user=", "");

  console.log(id);

  async function view_annexure() {
    const response = await fetch(basepath() + `/view_annexure`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id: id,
      }),
    });

    if (response.ok) {
      const result = await response.json();
      cases = result;
      user["newnumber"] = result["newnumber"];
      const mydata = cases.data.filter((user) => user);
      data = mydata[0];
      st = mydata[1];
      console.log(st.state);
      if (st.state === "CH" || st.state === "TN"){
        circle = 'TAMILNADU'        
      }
      if (st.state === "BR" || st.state === "JH"){
        circle = 'BIHAR & JHARKHAND'        
      }
      if (st.state === "MP" || st.state === "CG"){
        circle = 'MADHYA PRADESH & CHHATTISGARH'        
      }
      if (st.state === "MUM" || st.state === "MH"){
        circle = 'MAHARASHTRA'        
      }
      if (st.state === "KO" || st.state === "WB"){
        circle = 'WEST BENGAL'        
      }
      if (st.state === "AP" || st.state === "TS"){
        circle = 'ANDHRA PRADESH'        
      }
      if (st.state === "UE" || st.state === "UW"){
        circle = 'UTTAR PRADESH'        
      }
      if (st.state === "GJ"){
        circle = 'GUJARAT'        
      }
      if (st.state === "AS"){
        circle = 'ASSAM'        
      }
      if (st.state === "DL"){
        circle = 'DELHI'        
      }
      if (st.state === "RJ"){
        circle = 'RAJASTHAN'        
      }
      if (st.state === "OR"){
        circle = 'ORISSA'        
      }
      if (st.state === "KL"){
        circle = 'KERALA'        
      }
      if (st.state === "PB"){
        circle = 'PUNJAB'        
      }
      if (st.state === "KA"){
        circle = 'KARNATAKA'        
      }
      if (st.state === "HR"){
        circle = 'HARYANA'        
      }

      const myst = cases.states.filter((user) => user);
      user.newnumber = myst;
      if (data.team === "CAT") {
        code = "302";
      }
      if (data.team === "AP") {
        code = "225";
      }
      if (data.team === "ISOT") {
        code = "227";
      }
      paginatedNumbers = paginateNumbers(user["newnumber"], itemsPerPage);
      console.log(paginatedNumbers, "//////////////");

      // Navigate to the target page with the data as a route parameter
    } else {
      console.error("fetch failed");
    }
  }

  onMount(() => {
    view_annexure();
  });

  function paginateNumbers(numbers, itemsPerPage) {
    const pages = [];
    let currentIndex = 0;
    let serialNumber = 1;
    while (currentIndex < numbers.length) {
      // const nextPage = numbers.slice(currentIndex, currentIndex + itemsPerPage);
      const nextPage = numbers
        .slice(currentIndex, currentIndex + itemsPerPage)
        .map((number, index) => ({
          ...number,
          serialNumber: serialNumber + index,
        }));
      pages.push(nextPage);
      currentIndex += itemsPerPage;
      serialNumber += itemsPerPage;
      if (currentIndex === itemsPerPage && itemsPerPage === 22) {
        // Increase itemsPerPage to 30 after the first page
        itemsPerPage = 36;
      }
    }
    return pages;
  }

  const today = new Date();
  const year = today.getFullYear(); // Get the four-digit year
  const month = String(today.getMonth() + 1).padStart(2, "0"); // Get the month (0-11) and add leading zero if necessary
  const day = String(today.getDate()).padStart(2, "0"); // Get the day of the month and add leading zero if necessary

  async function generatePDF1() {
    const content = document.querySelector("#pdfContent");
    generatePDF(data,content,circle)
  }
//   onMount(() => {
//   // Delay for 2 seconds (2000 milliseconds) before generating the PDF
//   setTimeout(() => {
//     generatePDF1();
//   }, 1000);
// });
  
</script>

<!-- <button class="btn btn-outline-success" type="button" on:click={convertToPDF}>View PDF</button> -->
<main>
  <!-- <button
    class="btn btn-outline-primary"
    data-bs-toggle="tooltip"
    data-bs-placement="top"
    title="Download PDF"
    on:click={generatePDF1}
  >
    <i class="bi bi-download" />
  </button> -->

  <section>
    <div class="container" style="width: 40%;">
      <div id="pdfContent">
        <div class="form-header">
          <div class="left-header" style="margin-top: 5px;margin-left: 20px;">No: {code}/APSIB/{year}</div>
          <div class="right-header" style="margin-top: 5px;margin-right: 20px;">Date: {data.date}</div>
        </div>

        <div class="head">
          <h5 style="text-decoration: underline;"><b>SECRET</b></h5>
          <p style="text-decoration: underline;margin-top:-5px">
            Annexure - IX
          </p>
          <p style="margin-top: -15px;">
            Proforma to seek Call Data/Deal Record <br />
            (Request under section 92 of the CrPC 1973)
          </p>
        </div>
        <div class="reciever">
          To, <br />
          The Nodal Officer(LEA), <br />
          BSNL, Andhra Pradesh Circle.
        </div>

        <div class="subject">
          {#if data.requesttype === 'CDR'}
          Please provide the <b>ROAMING CDRs</b> of the following Cellone Mobile
          Number(s) in <b>{circle} Circles</b> for the below mentioned period
          
          {:else if data.requesttype === 'IMEI CDR'}
          Please provide the <b>IMEI CDR</b> of the following IMEI Number(s) 
          in <b>{circle} Circles</b> for the below mentioned period

          {:else if data.requesttype === 'IPDR' && data.subtypes === "Phone"}
          Please provide the <b>IPDR Data</b> of the following Cellone Mobile
          Number(s) in <b>{circle} Circles</b> for the below mentioned period

          {:else if data.requesttype === 'RECHARGE HISTORY (RH)' && data.subtypes === "Phone"}
          Please provide the <b>RECHARGE HISTORY (RH) Data</b> of the following Cellone Mobile
          Number(s) in <b>{circle} Circles</b> for the below mentioned period

          {:else if data.requesttype === 'POINT OF ACTIVATION (POA)' && data.subtypes === "Phone"}
          Please provide the <b>POINT OF ACTIVATION (POA) Data</b> of the following Cellone Mobile
          Number(s) in <b>{circle} Circles</b> for the below mentioned period

          {:else if data.requesttype === 'CAF'}
          Please provide the <b>CAF (Customer Application Form) Details and Supported Documents</b> of the following Cellone Mobile
          Number(s) in <b>{circle} Circles</b> for the below mentioned period

          {:else if data.requesttype === 'SDR'}
          Please provide the <b>SDR</b> of the following Cellone Mobile
          Number(s) in <b>{circle} Circles</b> for the below mentioned period
          
          {:else if data.requesttype === 'TOWER CDR' && data.subtypes === "CGI" 
          || data.requesttype === 'TOWER IPDR' && data.subtypes === "CGI" 
          || data.requesttype === 'TOWER GPRS' && data.subtypes === "CGI"}
          Please provide the <b>{data.requesttype}s</b> of the following Cellone Mobile
          Number(s) in <b>{circle} Circles</b> for the below mentioned period
          {/if}
        </div>

        {#each paginatedNumbers as page, pageIndex}
          <div class="body">
            <div class="table-container">
              <table
                class="table table-bordered"
                style="border-color: black;border:1px solid black;user-select:none;"
              >
              {#if data.requesttype === 'CDR' 
              || data.requesttype === 'IPDR' && data.subtypes === "Phone" 
              // || data.requesttype === 'GPRS' && data.subtypes === "Phone" 
              || data.requesttype === 'RECHARGE HISTORY (RH)' && data.subtypes === "Phone" 
              || data.requesttype === 'POINT OF ACTIVATION (POA)' && data.subtypes === "Phone"}
                  <thead style="text-align: center;vertical-align:middle;border-bottom:black">
                    <tr>
                      <th>SL.No</th>
                      <th>Phone/Mobile No.</th>
                      <th>From Date</th>
                      <th>To Date</th>
                      <th>FIR/Case No.</th>
                    </tr>
                  </thead>
                  <tbody class="text-center">
                    {#each page as newno}
                      <tr>
                        <td>{newno.serialNumber}</td>
                        <td>{newno.Phno}</td>
                        <td>{newno.From_Date}</td>
                        <td>{newno.To_Date}</td>
                        <td>{code}/APSIB/{year}</td>
                      </tr>
                    {/each}
                  </tbody>
                  {:else if data.requesttype === 'CAF' || data.requesttype === 'SDR'}
                  <thead style="text-align: center;vertical-align:middle;border-bottom:black">
                    <tr>
                      <th>SL.No</th>
                      <th>Phone/Mobile No.</th>
                      <th>FIR/Case No.</th>
                    </tr>
                  </thead>
                  <tbody class="text-center">
                    {#each page as newno}
                      <tr>
                        <td>{newno.serialNumber}</td>
                        <td>{newno.Phno}</td>
                        <td>{code}/APSIB/{year}</td>
                      </tr>
                    {/each}
                  </tbody>
                  {:else if data.requesttype === 'TOWER CDR' && data.subtypes === "CGI" || data.requesttype === 'TOWER IPDR' && data.subtypes === "CGI" || data.requesttype === 'TOWER GPRS' && data.subtypes === "CGI" }
                  <thead style="text-align: center;vertical-align:middle;border-bottom:black">
                    <tr>
                      <th>SL.No</th>
                      <th>CELLTOWER IDs</th>
                      <th>From Date</th>
                      <th>To Date</th>
                      <th>FIR/Case No.</th>
                    </tr>
                  </thead>
                  <tbody class="text-center">
                    {#each page as newno}
                      <tr>
                        <td>{newno.serialNumber}</td>
                        <td>{newno.Cell_id}</td>
                        <td>{newno.From_Date}</td>
                        <td>{newno.To_Date}</td>
                        <td>{code}/APSIB/{year}</td>
                      </tr>
                    {/each}
                  </tbody>
                  {:else}
                  <thead style="text-align: center;vertical-align:middle;border-bottom:black">
                    <tr>
                      <th>SL.No</th>
                      <th>IMEI No.</th>
                      <th>From Date</th>
                      <th>To Date</th>
                      <th>FIR/Case No.</th>
                    </tr>
                  </thead>
                  <tbody class="text-center">
                    {#each page as newno}
                      <tr>
                        <td>{newno.serialNumber}</td>
                        <td>{newno.IMEI}</td>
                        <td>{newno.From_Date}</td>
                        <td>{newno.To_Date}</td>
                        <td>{code}/APSIB/{year}</td>
                      </tr>
                    {/each}
                  </tbody>
              {/if}
              </table>
            </div>
            {#if (data.pending === "Mail Under Process" && userDetails.team === "CAT") || (data.pending === "Mail Under Process" && userDetails.role === "Mailer")}
              {#if page !== paginatedNumbers[paginatedNumbers.length - 1]}
                <div class="sign1" style="margin-top: 30px;">
                  <img
                    src="../src/public/Images/sign1.png"
                    alt="sign1"
                    width="120"
                    height="120"
                  />
                  <!-- <span>Page {pageIndex + 1}</span> -->
                </div>
              {/if}
            {/if}
          </div>

          {#if page.length < 36 && pageIndex === paginatedNumbers.length - 1}
            <p style="user-select: none; margin-left: 20px;">
              1) The subscriber identity has been ascertained, and it is ensured
              that the person in question is not someone whose call details are
              of a sensitive nature. <br />
              2) These numbers are not subscribed in the name of a sitting MLA/MP/MLC/GOVERNOR.
            </p>
            <div class="form-footer">
              <div class="left-footer" style="margin-left: 20px;">
                Place: VIJAYAWADA <br />
                Date: {data.date}
              </div>
              {#if (data.pending === "Mail Under Process" && userDetails.team === "CAT") || (data.pending === "Mail Under Process" && userDetails.role === "Mailer")}
                <div class="right-footer" style="user-select:none;">
                  <img
                    src="../src/public/Images/sign1.png"
                    alt="sign1"
                    width="120"
                    height="120"
                  /><br />
                  <p style="margin-top: -24px;line-height:1 ">
                    BABUJEE ATTADA, IPS <br />
                    Superintendent of Police <br />
                    AP SIB (Int), VIJAYAWADA <br />
                    Andhra Pradesh<br />
                    Phone No.: 9440231222<br />
                    E-mail ID : lab3.sib@apint.gov.in
                  </p>
                  <p style="margin-top: -18px;color:#5961d8;">
                    <b>BABUJEE ATTADA, IPS</b> <br />
                    Superintendent of Police <br />
                    AP SIB (Int), VIJAYAWADA <br />
                    Special Intelligence Branch (Int.) <br />
                    Andhra Pradesh, Vijayawada
                  </p>
                </div>
              {/if}
            </div>
          {/if}
          {#if (page.length === 22 && pageIndex === 0) || page.length < 22}
            <div style="margin-top: -5px; text-align:center">
              <span>Page {pageIndex + 1}</span>
            </div>
          {:else}
            <div style="margin-top: -35px; text-align:center">
              <span>Page {pageIndex + 1}</span>
            </div>
          {/if}
          <!-- <div style="margin-top: -50px; text-align:center">
        <span>Page {pageIndex + 1}</span>
      </div>      -->
          {#if pageIndex !== paginatedNumbers.length - 1}
            <div style="page-break-before: always;" />
          {/if}
        {/each}
      </div>
    </div>
  </section>
</main>

<style>
  /* main {
    user-select: none;
    text-align: justify;
    text-wrap: wrap;
    margin-left: 20px;
    margin-top: 25px;
  } */
  /* Position and style of page numbers */
  .page1 {
    position: absolute;
    bottom: 10px;
    right: 50%;
  }
  .page2 {
    transform: translateX(-50%);
    position: absolute;
    bottom: -100%;
    right: 50%;
  }
  /* 
  main{
    width: 21cm;
    height: 29.7cm;
    font-family:Arial, Helvetica, sans-serif;
  } */
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
    /* padding: 50px; */
    justify-content: space-between;
    margin-top: 150px;
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
    margin-left: 220px;
  }
  .right-footer img {
    position: absolute;
    top: -50px;
    left: 50%;
    margin-top: -20px;
    margin-left: 20px;
    transform: translateX(-50%);
  }
  .head {
    text-align: center;
    margin-top: 10px;
  }
  .subject {
    text-align: left;
    text-wrap: wrap;
    margin-left: 20px;
    margin-top: 10px;
    margin-bottom: 10px;
  }
  .sign1 {
    text-align: center;
  }
  table,
  th,
  td {
    padding: 0 0 0 0;
    margin-left: 20px;
    margin-right: 20px;
  }

  .table-container {
    display: flex;
    justify-content: center;
    margin-left: 20px;
    margin-right: 20px;
    margin-top: 10px;
  }
  .reciever {
    margin-top: -10px;
    margin-bottom: 10px;
    margin-left: 20px;
  }

  .container {
    box-shadow: 0 0.5rem 1rem rgb(0, 0, 0) !important;
    background-color: #f4f1f1;
    border-radius: 5px;
    margin-bottom: 50px;
    padding: 1 1 1 1;
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
  /* #pdfContent{
    border: 1px solid black;
    padding: 1 1 1 1;
  } */
</style>
