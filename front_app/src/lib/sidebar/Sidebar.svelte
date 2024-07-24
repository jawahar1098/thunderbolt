<script>
  // @ts-nocheck
  
    import { userDetailsStore } from "$lib/datastore.js";
    import { onMount, onDestroy } from "svelte";
    import { basepath } from "$lib/config";
    import Vigor from "$lib/profileview/vigor.svelte";
    import { goto } from "$app/navigation";

  //   function clearLocalStorageOnUnload() {
  //   localStorage.clear();
  // }

  // // Add event listener for beforeunload event
  // window.addEventListener('beforeunload', clearLocalStorageOnUnload);
  
    let userDetails;
    let jsonString;
    let encodedData;
    let activelink = "dashboard";
    let isSidebarCollapsed = true;
    let activeLink = "";
    let Nexus = '';
    let vigor = '';
    let CDAT = '';
    let Ticketing = '';
    let Analysis = '';
    let Database = '';
    let DASHBOARD = '';
  
     
  // let activeLink = "";
  
  let dropdowns = {
    cdat: false,
    analysis: false,
    ticket: false,
    dashboard: false,
  };
  

    let getdata = JSON.parse(localStorage.getItem('userDetails'))
    console.log(getdata)

    Nexus = getdata.Model && getdata.Model.includes('Nexus');
    console.log(Nexus)

    vigor = getdata.Model && getdata.Model.includes('VIGOR');
    console.log(vigor)

    CDAT = getdata.Model && getdata.Model.includes('cdat');
    console.log(CDAT)

    DASHBOARD = getdata.Model && getdata.Model.includes('dashboard');
    console.log(DASHBOARD)

    Ticketing = getdata.Model && getdata.Model.includes('ticketing');
    console.log(Ticketing)

    Analysis = getdata.Model && getdata.Model.includes('analysis');
    console.log(Analysis)

    Database = getdata.Model && getdata.Model.includes('database');
    console.log(Database)
  
    function loginToVigor() {
      console.log('vigor')
      const savedEmail =  getdata['email'] 
      const savedPassword = getdata['password'] 
        console.log(savedEmail, savedPassword , "-----")
      if (savedEmail && savedPassword) {
        const vigorURL = `http://192.168.1.14:9000/login?email=${savedEmail}&password=${savedPassword}`;
        window.open(vigorURL, '_blank');
      } else {
        console.log('No saved credentials found.');
      }
    }
    async function logout() {
      const userDetails = JSON.parse(localStorage.getItem("userDetails"));
      const email = userDetails.email;
      await fetch(basepath() + '/logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: email })
      })
      localStorage.setItem("userAuth", false);
      goto('/');
      window.location.reload();
    }
    function close(){
      goto('/')
      window.location.reload();
    }

    let email = '';
  let password = '';
  let newPassword = '';
  let confirmPassword = '';
  let result = '';
  let showPasswordFields = false;

  async function mail_search() {
    const response = await fetch(basepath() + '/mail_search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email: email, pass1: password }),
    });
    result = await response.json();
    if (response.ok && result.result) {
      console.log("Email verified: ", result.result);
      showPasswordFields = true;
    } else {
      console.log("Error: ", result.Error);
      showPasswordFields = false;
    }
  }

  async function updatePassword() {
    if (newPassword !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    const response = await fetch(basepath() + '/password_update', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email: email, pass1: newPassword, pass2: confirmPassword }),
    });
    const responseData = await response.json();
    if (response.ok) {
      if (responseData.Error) {
        alert(responseData.Error);
        return;
      }
      alert("New Password Updated!");
      logout(); // Assuming you have a logout function to handle user logout
    } else {
      alert("Password Not Updated");
    }
  }
  
    function loginToNexus() {
      // console.log('Nexus',getdata['Model']['email'] , getdata['Model']['password']  )
      const savedEmail =  getdata['email'] 
      const savedPassword = getdata['password'] 
        console.log(savedEmail, savedPassword , "-----")
      if (savedEmail && savedPassword) {
        const nexusURL = `http://10.50.50.230:4000/?email=${savedEmail}&password=${savedPassword}`;      // 10.50.50.230:4000
        window.open(nexusURL, '_blank');
      } else {
        console.log('No saved credentials found.');
      }
    }
  

  function toggleDropdown(dropdown) {
    dropdowns = Object.fromEntries(
      Object.entries(dropdowns).map(([key, value]) => [key, key === dropdown ? !value : false])
    );
  }

  userDetailsStore.subscribe((value) => {
    userDetails = value;
    jsonString = JSON.stringify(userDetails);
    console.log(jsonString, "/////////////////////////");
    encodedData = btoa(jsonString);
  });

  function handleLogout() {
    window.location.href = "/";
  }

  function toggleSidebar(do_open=false) {
    console.log(do_open, isSidebarCollapsed)
    if (do_open) {
      isSidebarCollapsed = false;
    } else {
      isSidebarCollapsed = !isSidebarCollapsed;
    }
    dropdowns = Object.fromEntries(Object.keys(dropdowns).map(key => [key, false]));
  }

  function setActiveLink(link) {
    activelink = link;
  }
  </script>
<main class="{isSidebarCollapsed ? 'close': ''}" on:mouseenter={() => toggleSidebar(true)} on:mouseleave ={() => toggleSidebar(false)}>
  <div
    class="sidebar {isSidebarCollapsed ? 'close': ''} position-fixed top-0 start-0 bottom-0 bg-light border-end">
    <ul class="sidebar-menu p-3 m-0 mb-0">
      <li class="sidebar-menu-item-logo">
        <!-- svelte-ignore a11y-invalid-attribute -->
        <a href="" style="color: var(--bs-indigo);">
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <!-- svelte-ignore a11y-no-static-element-interactions -->
          <i
            class="bi bi-lightning-charge-fill sidebar-menu-item-icon logo"
            style="color: var(--bs-indigo);"
            on:click={toggleSidebar}
          ></i>
          <span class="link_name" style="color: var(--bs-indigo);">Thunderbolt</span>
        </a>
      </li> 
      
      {#if userDetails.designation !== 'Administrator'}
      <li class="sidebar-menu-item">
        <a href="/dashboard" class="{activelink === 'dashboard' ? 'active' : ''}">
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <!-- svelte-ignore a11y-no-static-element-interactions -->
          <i class="bi bi-grid-fill sidebar-menu-item-icon" on:click={toggleSidebar}></i>
          DASHBOARD
        </a>
      </li>
      {/if}
      <!-- {#if userDetails.designation === 'Administrator'}
      <li class="sidebar-menu-item">
        <a href="/ticketing/superadmin/" on:click={() => setActiveLink("user_creation")} class="{activelink === 'user_creation' ? 'active' : ''}" >
          <i class="bi bi-person-plus-fill sidebar-menu-item-icon" on:click={toggleSidebar}></i>
          USER CREATION
        </a>
      </li>
      {/if} -->
      
      {#if userDetails.designation === 'Administrator'}
      <li
        class= "sidebar-menu-item" on:click={() => toggleDropdown("dashboard")}>
        <a href="/dashboard" on:click={() => setActiveLink("dashboard")} class="{activelink === 'dashboard' ? 'active' : ''}">
          <!-- svelte-ignore a11y-no-static-element-interactions -->
          <i class="bi bi-grid-fill sidebar-menu-item-icon" on:click={toggleSidebar}></i>
          DASHBOARD
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <!-- svelte-ignore a11y-no-static-element-interactions -->
          <i
            class={dropdowns.dashboard
              ? "bi bi-chevron-down arrow sidebar-menu-item-accordion ms-auto rotated"
              : "bi bi-chevron-down arrow sidebar-menu-item-accordion ms-auto"}     ></i>
        </a>
        <ul
          class={dropdowns.dashboard
            ? "sidebar-dropdown-menu"
            : "sidebar-dropdown-menu hidden"} >
          <li class="sidebar-dropdown-menu-item blank">
            <a
              href="/ticketing/superadmin/"
              class:selected={activelink === "user-creation"}
              on:click={() => setActiveLink("user-creation")}>USER CREATION</a
            >
          </li>     
        </ul>
      </li>
      {/if}


      {#if userDetails.designation === "Administrator"}
      <li
        class= "sidebar-menu-item" on:click={() => toggleDropdown("cdat")}
      >
        <a href="" on:click={() => setActiveLink("cdat")} class="{activelink === 'cdat' ? 'active' : ''}">
          <!-- svelte-ignore a11y-no-static-element-interactions -->
          <i class="bi bi-telephone-fill sidebar-menu-item-icon" on:click={toggleSidebar}></i>
          CDAT
          <i
            class={dropdowns.cdat
              ? "bi bi-chevron-down arrow sidebar-menu-item-accordion ms-auto rotated"
              : "bi bi-chevron-down arrow sidebar-menu-item-accordion ms-auto"}
            
          ></i>
        </a>

        <ul
          class={dropdowns.cdat
            ? "sidebar-dropdown-menu"
            : "sidebar-dropdown-menu hidden"}
        >
          <li class="sidebar-dropdown-menu-item blank">
            <a
              href="/cdat/profile"
              class:selected={activelink === "cdat-profile"}
              on:click={() => setActiveLink("cdat-profile")}>Profile</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              href="/cdat/summary"
              class:selected={activelink === "cdat-summary"}
              on:click={() => setActiveLink("cdat-summary")}>SUMMARY</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              href="/cdat/calldetails"
              class:selected={activelink === "cdat-calldetails"}
              on:click={() => setActiveLink("cdat-calldetails")}>CALL DETAILS</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              href="/cdat/locations"
              class:selected={activelink === "cdat-locations"}
              on:click={() => setActiveLink("cdat-locations")}>LOCATION</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              href="/cdat/suspecteddb"
              class:selected={activelink === "cdat-suspecteddb"}
              on:click={() => setActiveLink("cdat-suspecteddb")}>SUSPECTED DB</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              href="/cdat/search"
              class:selected={activelink === "cdat-search"}
              on:click={() => setActiveLink("cdat-search")}>SEARCH</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              href="/cdat/imeisearch"
              class:selected={activelink === "cdat-imeisearch"}
              on:click={() => setActiveLink("cdat-imeisearch")}>IMEI SEARCH</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              href="/cdat/number_analysis"
              class:selected={activelink === "number-analysis"}
              on:click={() => setActiveLink("number-analysis")}>NUMBER ANALYSIS</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              href="/cdat/summary_ipdr"
              class:selected={activelink === "cdat-summary_ipdr"}
              on:click={() => setActiveLink("cdat-summary_ipdr")}
              >IPDR SUMMARY</a
            >
          </li>
        </ul>
      </li>
      {:else if getdata.Model && getdata.Model.includes('CDAT') && userDetails.designation !== 'Administrator'}
      <li
        class= "sidebar-menu-item" on:click={() => toggleDropdown("cdat")}
      >
        <!-- svelte-ignore a11y-invalid-attribute -->
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <a href="" on:click={() => setActiveLink("cdat")} class="{activelink === 'cdat' ? 'active' : ''}">
          <!-- svelte-ignore a11y-no-static-element-interactions -->
          <i class="bi bi-telephone-fill sidebar-menu-item-icon" on:click={toggleSidebar}></i>
          CDAT
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <!-- svelte-ignore a11y-no-static-element-interactions -->
          <i
            class={dropdowns.cdat
              ? "bi bi-chevron-down arrow sidebar-menu-item-accordion ms-auto rotated"
              : "bi bi-chevron-down arrow sidebar-menu-item-accordion ms-auto"}
            
          ></i>
        </a>

        <ul
          class={dropdowns.cdat
            ? "sidebar-dropdown-menu"
            : "sidebar-dropdown-menu hidden"}
        >
          <!-- <li class="sidebar-dropdown-menu-item">
            <a class="link_name" href="/cdat">CDAT</a>
          </li> -->
          <li class="sidebar-dropdown-menu-item blank">
            <a
              href="/cdat/profile"
              class:selected={activelink === "cdat-profile"}
              on:click={() => setActiveLink("cdat-profile")}>Profile</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              href="/cdat/summary"
              class:selected={activelink === "cdat-summary"}
              on:click={() => setActiveLink("cdat-summary")}>SUMMARY</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              href="/cdat/calldetails"
              class:selected={activelink === "cdat-calldetails"}
              on:click={() => setActiveLink("cdat-calldetails")}>CALL DETAILS</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              href="/cdat/locations"
              class:selected={activelink === "cdat-locations"}
              on:click={() => setActiveLink("cdat-locations")}>LOCATION</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              href="/cdat/suspecteddb"
              class:selected={activelink === "cdat-suspecteddb"}
              on:click={() => setActiveLink("cdat-suspecteddb")}>SUSPECTED DB</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              href="/cdat/search"
              class:selected={activelink === "cdat-search"}
              on:click={() => setActiveLink("cdat-search")}>SEARCH</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              href="/cdat/imeisearch"
              class:selected={activelink === "cdat-imeisearch"}
              on:click={() => setActiveLink("cdat-imeisearch")}>IMEI SEARCH</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              href="/cdat/number_analysis"
              class:selected={activelink === "number-analysis"}
              on:click={() => setActiveLink("number-analysis")}>NUMBER ANALYSIS</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              href="/cdat/summary_ipdr"
              class:selected={activelink === "cdat-summary_ipdr"}
              on:click={() => setActiveLink("cdat-summary_ipdr")}
              >IPDR SUMMARY</a
            >
          </li>
        </ul>
      </li>
      {/if}

     
      {#if userDetails.designation === "Administrator"}
      <li class="sidebar-menu-item">
        <a on:click={loginToNexus}>
          <i class="bi bi-reception-4 sidebar-menu-item-icon" on:click={toggleSidebar}></i>
          NEXUS
        </a>
      </li>
      {:else if getdata.Model && getdata.Model.includes('NEXUS') && userDetails.designation !== 'Administrator'}
      <li class="sidebar-menu-item">
        <a on:click={loginToNexus}>
          <i class="bi bi-reception-4 sidebar-menu-item-icon" on:click={toggleSidebar}></i>
          NEXUS
        </a>
      </li>
      {/if}
    

              {#if getdata.Model && getdata.Model.includes('TICKETING') && userDetails.designation !== 'Administrator'}
              <li class={dropdowns.ticket ? "sidebar-menu-item has-dropdown focused" : "sidebar-menu-item has-dropdown"}>
                <a href="#" on:click={() => toggleDropdown("ticket")} class="{activelink === 'analysis' ? 'ticket' : ''}">
                  <i class="bi bi-ticket-detailed-fill sidebar-menu-item-icon" on:click={toggleSidebar}></i>
                  TICKETING
                  <i
                    class={dropdowns.ticket
                      ? "bi bi-chevron-down arrow sidebar-menu-item-accordion ms-auto rotated"
                      : "bi bi-chevron-down arrow sidebar-menu-item-accordion ms-auto"}
                    on:click={() => toggleDropdown("ticket")}
                  ></i>
                </a>
                <ul  class={dropdowns.ticket ? "sidebar-dropdown-menu": "sidebar-dropdown-menu hidden"}>
                  <li class="sidebar-dropdown-menu-item">
                    <a href="/ticketing/Datareq/">Data Tickets</a>
                  </li>
                  <li class="sidebar-dropdown-menu-item">
                    <a href="/ticketing/Analysisreq/">Analysis Tickets</a>
                  </li>
                
                  <li class="sidebar-dropdown-menu-item">
                    <a href="/ticketing/Dashboard">Report</a>
                  </li>
                </ul>
              </li>
              {/if}

        {#if userDetails.designation === "Administrator"}
        <li class="sidebar-menu-item">
          <a href="/vigor" on:click={() => setActiveLink("vigor")} class="{activelink === 'vigor' ? 'active' : ''}">
            <i class="bi bi-record-btn-fill sidebar-menu-item-icon" on:click={toggleSidebar}></i>
            VIGOR
          </a>              
        </li>
        {:else if getdata.Model && getdata.Model.includes('VIGOR') && userDetails.designation !== 'Administrator'}
        <li class="sidebar-menu-item">
          <a href="/vigor" on:click={() => setActiveLink("vigor")} class="{activelink === 'vigor' ? 'active' : ''}">
            <i class="bi bi-record-btn-fill sidebar-menu-item-icon" on:click={toggleSidebar}></i>
            VIGOR
          </a>              
        </li>
        {/if}

        {#if userDetails.designation === "Administrator"}
      <li class="sidebar-menu-item has-dropdown" on:click={() => toggleDropdown("analysis")}>
        <a href="" on:click={() => setActiveLink("analysis")} class="{activelink === 'analysis' ? 'active' : ''}">
          <i class="bi bi-graph-up sidebar-menu-item-icon" on:click={toggleSidebar}></i>
          ANALYSIS
          <i
            class="bi bi-chevron-down arrow sidebar-menu-item-accordion ms-auto"
            
          ></i>
        </a>
        <ul
          class={dropdowns.analysis
            ? "sidebar-dropdown-menu"
            : "sidebar-dropdown-menu hidden"}
        >
          <li class="sidebar-dropdown-menu-item">
            <a
              class:selected={activelink === "cases"}
              on:click={() => setActiveLink("cases")}
              href="/analysis/cases">Cases</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              class:selected={activelink === "Map"}
              on:click={() => setActiveLink("Map")}
              href="/analysis/map">Map</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              class:selected={activelink === "tower-map"}
              on:click={() => setActiveLink("tower-map")}
              href="/analysis/tower_map">Tower Map</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              class:selected={activelink === "common-link"}
              on:click={() => setActiveLink("common-link")}
              href="/analysis/common_link">Common Link</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              class:selected={activelink === "common-map"}
              on:click={() => setActiveLink("common-map")}
              href="/analysis/common_map">Common Map</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              class:selected={activelink === "tower-analysis"}
              on:click={() => setActiveLink("tower-analysis")}
              href="/analysis/tower_analysis">Tower Analysis</a
            >
          </li>
        </ul>
      </li>


      {:else if getdata.Model && getdata.Model.includes('ANALYSIS') && userDetails.designation !== 'Administrator'}
      <li class="sidebar-menu-item has-dropdown" on:click={() => toggleDropdown("analysis")}>
        <a href="" on:click={() => setActiveLink("analysis")} class="{activelink === 'analysis' ? 'active' : ''}">
          <i class="bi bi-graph-up sidebar-menu-item-icon" on:click={toggleSidebar}></i>
          ANALYSIS
          <i
            class="bi bi-chevron-down arrow sidebar-menu-item-accordion ms-auto"
            
          ></i>
        </a>
        <ul
          class={dropdowns.analysis
            ? "sidebar-dropdown-menu"
            : "sidebar-dropdown-menu hidden"}
        >
          <li class="sidebar-dropdown-menu-item">
            <a
              class:selected={activelink === "cases"}
              on:click={() => setActiveLink("cases")}
              href="/analysis/cases">Cases</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              class:selected={activelink === "Map"}
              on:click={() => setActiveLink("Map")}
              href="/analysis/map">Map</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              class:selected={activelink === "tower-map"}
              on:click={() => setActiveLink("tower-map")}
              href="/analysis/tower_map">Tower Map</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              class:selected={activelink === "common-link"}
              on:click={() => setActiveLink("common-link")}
              href="/analysis/common_link">Common Link</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              class:selected={activelink === "common-map"}
              on:click={() => setActiveLink("common-map")}
              href="/analysis/common_map">Common Map</a
            >
          </li>
          <li class="sidebar-dropdown-menu-item">
            <a
              class:selected={activelink === "tower-analysis"}
              on:click={() => setActiveLink("tower-analysis")}
              href="/analysis/tower_analysis">Tower Analysis</a
            >
          </li>
        </ul>
      </li>
      {/if}


      <li class="sidebar-menu-item">
        <a href="/ticketing/Nickname/" on:click={() => setActiveLink("nickname")} class="{activelink === 'nickname' ? 'active' : ''}">
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <!-- svelte-ignore a11y-no-static-element-interactions -->
          <i class="bi bi-journals sidebar-menu-item-icon" on:click={toggleSidebar}></i>
          NICKNAME
        </a>
      </li>

      {#if userDetails.designation === 'Administrator'}
      <li class="sidebar-menu-item">
        <a href="/database" on:click={() => setActiveLink("data")} class="{activelink === 'data' ? 'active' : ''}">
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <!-- svelte-ignore a11y-no-static-element-interactions -->
          <i class="bi bi-database-add sidebar-menu-item-icon" on:click={toggleSidebar}></i>
          DATABASE
        </a>
      </li>
      {:else if getdata.Model && getdata.Model.includes('DATABASE') && userDetails.designation !== 'Administrator'}
      <li class="sidebar-menu-item">
        <a href="/database" on:click={() => setActiveLink("data")} class="{activelink === 'data' ? 'active' : ''}">
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <!-- svelte-ignore a11y-no-static-element-interactions -->
          <i class="bi bi-database-add sidebar-menu-item-icon" on:click={toggleSidebar}></i>
          DATABASE
        </a>
      </li>
      {/if}
     

    </ul>
    <div class="p-2 bd-highlight">
      <button type="button" class="btn text-dark" data-bs-toggle="modal" data-bs-target="#myModal1"><i class="bi bi-person-circle"></i></button>
    </div>
    <!-- <div class="logout">
      <a href="#" on:click={handleLogout}>
        <i class="bi bi-box-arrow-right sidebar-menu-item-icon"></i>
      </a>
    </div> -->
  </div>
  <div class="toggle-sidebar">
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    <i class={isSidebarCollapsed ? "bi bi-caret-right-fill sidebar-menu-item-icon" : "bi bi-caret-right-fill sidebar-menu-item-icon rotated"} on:click={toggleSidebar}></i>
  </div>
  
</main>
<div class="modal fade" id="myModal1" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog position-absolute" style="bottom: 10px; width: 400px;margin-left:4%">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title text-dark" id="exampleModalLabel">{userDetails.officername} Profile</h5>
        </div>
        <div class="modal-body text-dark">
          <div class="container">
            <div class="row">
              <div class="col-12">
                <div class="row">
                  <div class="d-flex justify-content-end align-items-center">
                    <img src="/logo.png" alt="Generic placeholder image" class="img-fluid" style="width: 100px; border-radius: 100px;">
                      <div class="row">
                    <h5>{userDetails.officername}</h5>
                    <span><b>Designation :</b> {userDetails.designation}</span>
                    <span><b>Email :</b> {userDetails.email}</span>
                    <span><b>Team : </b>{userDetails.team}</span>
                    <span><b>Modules : </b>{userDetails.modules}</span>
                    <span><b>Role : </b>{userDetails.role}</span>
                    <span><b>Superior : </b>{userDetails.superior}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>  
        </div>
        <div class="modal-footer">
          <button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">Edit Password</button>
          <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
            <div class="offcanvas-header">
              <h5 id="offcanvasRightLabel">Reset Password</h5>
              <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
            </div>
            <div class="offcanvas-body">
              <label class="mb-3">Enter Current Email</label>
                <div class="input-group mb-3">
                  <input type="text" class="form-control" placeholder="Enter Current Email" bind:value={email} aria-label="Enter Current email" aria-describedby="button-addon2">
                  <input type="password" class="form-control" placeholder="Enter Current Password" bind:value={password} aria-label="Enter Current Password" aria-describedby="button-addon2">
                  <button class="btn btn-outline-warning" type="button" id="button-addon2" on:click={mail_search}><i class="bi bi-search"></i></button>
                </div>
                {#if result && result.result}
                  <p style="color: green; font-weight:bold">Welcome {result.result.officername}</p>
                {:else if result && result.Error}
                  <p style="color: red; font-weight:bold">{result.Error}</p>
                {/if}
                {#if showPasswordFields}
                  <div>
                    <label class="mb-3">New Password: </label>
                    <div class="input-group mb-3">
                      <input type="password" class="form-control" placeholder="New Password" bind:value={newPassword} aria-label="New Password">
                    </div>
                    <label class="mb-3">Confirm New Password: </label>
                    <div class="input-group mb-3">
                      <input type="password" class="form-control" placeholder="Confirm New Password" bind:value={confirmPassword} aria-label="Confirm New Password">
                    </div>
                    <button class="btn btn-success" type="button" on:click={updatePassword}>Update Password</button>
                  </div>
                {/if}
            </div>
          </div>
          <button type="button" class="btn btn-outline-primary" data-bs-dismiss="modal">Close</button>
          <button on:click={logout} type="button" class="btn btn-outline-danger">Logout</button>
        </div>
      </div>
    </div>
  </div>
</div>
  
  <style>
   main {
    display: flex;
    height: 100vh;
    position: fixed;
    margin-left: 16rem;
    z-index: 1;
  }
  main.close{
    width: 0px;
    margin-left: 72px;

  }
  .toggle-sidebar .sidebar-menu-item-icon {
  /* background-color: black; */
  color: var(--bs-indigo);
  clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%);
}

  .sidebar.close {
    width: 72px;
    overflow-x: hidden;
  }
  .toggle-sidebar {
    display: flex;
    align-items: center;
    width: 0px;

  }
  .sidebar {
    width: 16rem;
  }

  .hidden {
    display: none;
  }

  .rotated {
    transform: rotate(180deg);
    transition: transform 0.3s ease-in-out;
  }

  .sidebar-menu {
    list-style-type: none;
    height: 90vh;
  }

  .sidebar-menu-item {
    margin-bottom: 0.25rem;
    margin-right: -0.5rem;
    
  }
  .sidebar-menu-item-logo {
    margin-bottom: 1.25rem;
    margin-top: 1rem;
    margin-right: -0.5rem;
    font-weight: bold;
  }
  .sidebar-menu-item a {
    text-decoration: none;
    display: flex;
    align-items: center;
    color: var(--bs-dark);
    padding: 0.375rem 0.75rem;
    border-radius: 0.375rem;
    font-size: 1rem;
  }
  .sidebar-menu-item-logo a {
    text-decoration: none;
    display: flex;
    align-items: center;
    color: var(--bs-indigo);
    padding: 0.375rem 0.75rem;
    border-radius: 0.375rem;
    font-size: 1.5rem;
  }

  .sidebar-menu-item > a:hover {
    background-color: var(--bs-indigo);
    color: var(--bs-light);
  }

  .sidebar-menu-item a.active{
    background-color: var(--bs-indigo);
    color: var(--bs-light);
    box-shadow: 0 0.25rem 0.25rem rgba(0, 0, 0, 0.175);
  }
  .sidebar-menu-item-icon {
    margin-right: 1.5rem;
    font-size: 1.5rem;
    transition: transform 0.2s;
    /* color: black; */
  }
  .sidebar-dropdown-menu-item{
    margin-left: 1rem;
  }
  .sidebar-dropdown-menu-item a {
    /* padding: 0.375rem 0; */
    text-decoration: none;
    padding-right: 0.75rem;
    /* margin-left: 1.5rem; */
    margin-right: 0.5rem;
    text-transform: uppercase;
  }
  .sidebar-dropdown-menu-item:hover {
    background-color: #d4d2d6;
    border-radius: 0.375rem;
  }
  .sidebar-dropdown-menu {
    padding-left: 2rem;
    list-style: none;
    transition: transform 0.3s ease-in-out;
  }
  .sidebar-menu-item.focused > a .sidebar-menu-item-icon {
    transform: rotateZ("180deg");
  }

  .logout {
    margin-left: 1.25em;
    display:flex ;
  }

  .logout a{
    color: black;
  }
   
  </style>