<script>
  // @ts-nocheck
  
    import { transform } from "ol/proj";
    //@ts-nocheck
  
    import { userDetailsStore } from "$lib/datastore.js";
    import { onMount, onDestroy } from "svelte";
    import { basepath } from "$lib/config";
    import Vigor from "$lib/profileview/vigor.svelte";
    import { goto } from "$app/navigation";
  
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
  
     
  // let activeLink = "";
  
  let dropdowns = {
    cdat: false,
    analysis: false,
    ticket: false,
  };

    let getdata = JSON.parse(localStorage.getItem('userDetails'))
    console.log(getdata)

    Nexus = getdata.Model && getdata.Model.includes('Nexus');
    console.log(Nexus)

    vigor = getdata.Model && getdata.Model.includes('VIGOR');
    console.log(vigor)

    CDAT = getdata.Model && getdata.Model.includes('cdat');
    console.log(CDAT)

    Ticketing = getdata.Model && getdata.Model.includes('ticketing');
    console.log(Ticketing)

    Analysis = getdata.Model && getdata.Model.includes('analysis');
    console.log(Analysis)

    Database = getdata.Model && getdata.Model.includes('database');
    console.log(Database)
  

    // function toggleDropdown(dropdown) {
    //   dropdowns = { ...dropdowns, [dropdown]: !dropdowns[dropdown] };
    // }

    // userDetailsStore.subscribe(value => {
    // userDetails = value;
    // jsonString = JSON.stringify(userDetails);
    // });

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
      await fetch(basepath() + '/logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
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
    let result = '';
    let newPassword = '';
    let confirmPassword = '';
    let passwordMessage = '';
    let demo = ''
    let user_name = '';
    let showPasswordFields = false;

    async function mail_search(){
      const response = await fetch(basepath() +'/mail_search', {
        method: 'POST', 
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email }),
      });
      result = await response.json();
      if(response.ok && result.result){
        console.log("Email verified: ", result.result);
        showPasswordFields = true;
      } else {
        console.log("Error: ", result.Error);
        showPasswordFields = false;
      }
    }

    async function updatePassword() {
      if (newPassword !== confirmPassword ) {
        alert("passwordMismatch");
      }

      const response = await fetch(basepath() +'/password_update', {
        method: 'POST', 
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email, pass1: newPassword, pass2:confirmPassword})
      });
      const responseData = await response.json();
      if (response.ok) {
        if(responseData.error){
          alert(responseData.error);
          return;
        };
        alert("New Password Updated!!!!!!!!!!");
        logout();
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
        const nexusURL = `http://localhost:4000/login?email=${savedEmail}&password=${savedPassword}`;      // 10.50.50.230:4000
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


  <nav class="navbar">
      <div class="p-2 bd-highlight navbar-brand">
        <img src="/ipdr.png" alt="Logo" class="navbar-logo">
        <span class="brand-text">Maze</span>
      </div>
      <div class="p-2 bd-highlight">
        <!-- <img src="{userDetails.profileImageUrl}" class="user-icon" alt="User Image"> -->
        <button type="button" class="btn text-dark" data-bs-toggle="modal" data-bs-target="#myModal1"><i class="bi bi-person-circle"></i></button>
        <div class="modal fade" id="myModal1" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true" data-bs-backdrop="static">
          <div class="modal-dialog position-absolute top-0" style="right: 10px; width: 400px;">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title text-dark" id="exampleModalLabel">{userDetails.officername} Profile</h5>
                <!-- <button data-bs-toggle="tooltip" data-bs-placement="top" title='Reset Password' type="button" class="btn btn-outline-primary">Reset <i class="bi bi-key"></i></button>  -->
              </div>
              <div class="modal-body text-dark">
                <div class="container">
                  <div class="row">
                    <div class="col-12">
                      <div class="row">
                        <div class="d-flex justify-content-end align-items-center">
                          <!-- svelte-ignore a11y-img-redundant-alt -->
                          <img src="/ipdr.png" alt="Generic placeholder image" class="img-fluid" style="width: 100px; border-radius: 100px;">
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
                <button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">Reset Password</button>
                <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
                  <div class="offcanvas-header">
                    <h5 id="offcanvasRightLabel">Reset Password</h5>
                    <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                  </div>
                  <div class="offcanvas-body">
                    <!-- svelte-ignore a11y-label-has-associated-control -->
                    <label class="mb-3">Enter Your Email ID: </label>
                    <div class="input-group mb-3">
                      <input type="text" class="form-control" placeholder="Enter Email ID" bind:value={email} aria-label="Enter Email ID" aria-describedby="button-addon2">
                      <button class="btn btn-outline-warning" type="button" id="button-addon2" on:click={mail_search}><i class="bi bi-search"></i></button>
                    </div>
            
                    {#if result && result.result}
                      <p style="color: green; font-weight:bold">Welcome {result.result.officername}</p>
                    {:else if result && result.Error}
                      <p style="color: red; font-weight:bold">{result.Error}</p>
                    {/if}
            
                    {#if showPasswordFields}
                      <div>
                        <!-- svelte-ignore a11y-label-has-associated-control -->
                        <label class="mb-3">New Password: </label>
                        <div class="input-group mb-3">
                          <input type="password" class="form-control" placeholder="New Password" bind:value={newPassword} aria-label="New Password">
                        </div>
                        <!-- svelte-ignore a11y-label-has-associated-control -->
                        <label class="mb-3">Confirm New Password: </label>
                        <div class="input-group mb-3">
                          <input type="password" class="form-control" placeholder="Confirm New Password" bind:value={confirmPassword} aria-label="Confirm New Password">
                        </div>
                        <p>{passwordMessage}</p>
                        <button class="btn btn-success" type="button" on:click={updatePassword}>Update Password</button>
                      </div>
                    {/if}
                  </div>
                </div>
                <button on:click={close} type="button" class="btn btn-outline-primary">Close</button>
                <button on:click={logout} type="button" class="btn btn-outline-danger">Logout</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
    <main class="{isSidebarCollapsed
      ? 'close'
      : ''}"
      on:mouseenter={() => toggleSidebar(true)}
      on:mouseleave ={() => toggleSidebar(false)}>
      <div
        class="sidebar {isSidebarCollapsed
          ? 'close'
          : ''} position-fixed top-0 start-0 bottom-0 bg-light border-end"
      >
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
              <span class="link_name" style="color: var(--bs-indigo);">Maze</span>
            </a>
          </li>
          <li class="sidebar-menu-item">
            <a href="/dashboard" class="{activelink === 'dashboard' ? 'active' : ''}">
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              <!-- svelte-ignore a11y-no-static-element-interactions -->
              <i class="bi bi-grid-fill sidebar-menu-item-icon" on:click={toggleSidebar}></i>
              DASHBOARD
            </a>
          </li>
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
              <li class="sidebar-dropdown-menu-item">
                <a class="link_name" href="/cdat">CDAT</a>
              </li>
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
                  href="/cdat/analysis"
                  class:selected={activelink === "cdat-analysis"}
                  on:click={() => setActiveLink("cdat-analysis")}>ANALYSIS</a
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
          <li class="sidebar-menu-item">
            <a on:click={loginToNexus}>
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              <!-- svelte-ignore a11y-no-static-element-interactions -->
              <i class="bi bi-reception-4 sidebar-menu-item-icon" on:click={toggleSidebar}></i>
              NEXUS
            </a>
            <!-- <ul class="sidebar-dropdown-menu blank">
              <li><a class="link_name" href="/nexus">NEXUS</a></li>
            </ul> -->
          </li>
          <li class={dropdowns.ticket
            ? "sidebar-menu-item has-dropdown focused"
            : "sidebar-menu-item has-dropdown"}>
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <a href="/ticketing/allinONE" on:click={() => setActiveLink("ticket")} class="{activelink === 'analysis' ? 'ticket' : ''}">
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              <i class="bi bi-ticket-detailed-fill sidebar-menu-item-icon" on:click={toggleSidebar}></i>
              TICKETING
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              <!-- svelte-ignore a11y-no-static-element-interactions -->
              <!-- <i
                class={dropdowns.ticket
                  ? "bi bi-chevron-down arrow sidebar-menu-item-accordion ms-auto rotated"
                  : "bi bi-chevron-down arrow sidebar-menu-item-accordion ms-auto"}
                on:click={() => toggleDropdown("ticket")}
              ></i> -->
            </a>
            <ul  class={dropdowns.ticket
              ? "sidebar-dropdown-menu"
              : "sidebar-dropdown-menu hidden"}>
              <li class="sidebar-dropdown-menu-item">
                <a href="/ticketing/Dashboard">Report</a>
              </li>
            </ul>
          </li>
          <!-- <li class="sidebar-menu-item">
            <a href="/vigor" on:click={() => setActiveLink("vigor")} class="{activelink === 'vigor' ? 'active' : ''}">
              <i class="bi bi-record-btn-fill sidebar-menu-item-icon" on:click={toggleSidebar}></i>
              VIGOR
            </a>
            
          </li> -->
    
          <li class="sidebar-menu-item has-dropdown" on:click={() => toggleDropdown("analysis")}>
            <a href="" on:click={() => setActiveLink("analysis")} class="{activelink === 'analysis' ? 'active' : ''}">
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              <!-- svelte-ignore a11y-no-static-element-interactions -->
              <i class="bi bi-graph-up sidebar-menu-item-icon" on:click={toggleSidebar}></i>
              ANALYSIS
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              <!-- svelte-ignore a11y-no-static-element-interactions -->
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
              <!-- <li class="sidebar-dropdown-menu-item">
                <a
                  class:selected={activelink === "common_link"}
                  on:click={() => setActiveLink("common_link")}
                  href="/analysis/common_link">Visiting Point</a
                >
              </li> -->
              <li class="sidebar-dropdown-menu-item">
                <a
                  class:selected={activelink === "tower-analysis"}
                  on:click={() => setActiveLink("tower-analysis")}
                  href="/analysis/tower_analysis">Tower Analysis</a
                >
              </li>
            </ul>
          </li>
          <li class="sidebar-menu-item">
            <a href="/database" on:click={() => setActiveLink("data")} class="{activelink === 'data' ? 'active' : ''}">
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              <!-- svelte-ignore a11y-no-static-element-interactions -->
              <i class="bi bi-database-add sidebar-menu-item-icon" on:click={toggleSidebar}></i>
              DATABASE
            </a>
          </li>
        </ul>
        <div class="logout">
          <!-- svelte-ignore a11y-invalid-attribute -->
          <a href="#" on:click={handleLogout}>
            <i class="bi bi-box-arrow-right sidebar-menu-item-icon"></i>
          </a>
        </div>
      </div>
      <div class="toggle-sidebar">
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        <i
        class={isSidebarCollapsed
          ? "bi bi-caret-right-fill sidebar-menu-item-icon"
          : "bi bi-caret-right-fill sidebar-menu-item-icon rotated"}
          on:click={toggleSidebar}
        ></i>
      </div>
    </main>
  
  <style>
   main {
    display: flex;
    height: 100vh;
    position: fixed;
    margin-left: 16rem;
    z-index: 1;
  }
  main.close{
    width: 26px;
    margin-left: 72px;

  }
  .toggle-sidebar .sidebar-menu-item-icon {
  /* background-color: black; */
  color: var(--bs-indigo);
  clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%);
}
.sidebar-menu-item-icon .logo{
  color: var(--bs-indigo);
}


  .sidebar.close {
    width: 72px;
    overflow-x: hidden;
  }
  .toggle-sidebar {
    display: flex;
    align-items: center;
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
    height: 94vh;
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
  .sidebar-menu-item.focused > a .sidebar-menu-item-icon,
  .sidebar-menu-item.focused > a .sidebar-menu-item {
    transform: rotateZ("180deg");
  }

  .logout {
    margin-left: 1.25em;
    display:flex ;
  }

  .logout a{
    color: black;
  }


    .navbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      /* background: -webkit-linear-gradient(to top, #4c5088, #7e83a1);  */
      background: linear-gradient(to top, #fbfcfd, #dadbdf);
      color: rgb(23, 23, 24);
      padding: 10px 20px;
      position: fixed;
      top: 0;
      left: 0;
      z-index: 1;
      width: 100%;
      height: 50px;
      /* border: 1px solid; */
    }

    .navbar .nav-links a {
      color: rgb(15, 14, 14);
      text-decoration: none;
      margin-left: 200px;
      font-size: 18px;
    }

    .navbar .nav-links a:hover {
      text-decoration: underline;
    }
    .navbar-brand {
      font-size: 2rem;
      font-weight: bold;
      color: #0e0d0d;
      margin-left: 59px;
      margin-top: -17px;
    }

    .navbar-logo {
      height: 40px;
      width: auto;
      margin-right: 10px;
      margin-top: -17px;
      object-fit: cover;
      border-radius: 50%;
    }

    .brand-text {
      display: inline-block;
      margin-top: -20px;
    }
    
    .bd-highlight {
      margin-top: -13px;
    }
  .modal-body {
    z-index: 2;
  }
  
   
  </style>
























































<!-- <script>
  //@ts-nocheck
  
  import {userDetailsStore} from '$lib/datastore.js';
  import {onMount , onDestroy} from 'svelte';
  import {
    basepath
  } from "$lib/config"
    import { error } from '@sveltejs/kit';
    import { goto } from '$app/navigation';
  let userDetails;
  let jsonString;
  let activelink = "";
  let Nexus = '';
  let vigor = '';
  let CDAT = '';
  let Ticketing = '';
  let Analysis = '';
  let Database = '';

  let getdata = JSON.parse(localStorage.getItem('userDetails'))
  console.log(getdata)

  Nexus = getdata.Model && getdata.Model.includes('Nexus');
  console.log(Nexus)

  vigor = getdata.Model && getdata.Model.includes('VIGOR');
  console.log(vigor)

  CDAT = getdata.Model && getdata.Model.includes('cdat');
  console.log(CDAT)

  Ticketing = getdata.Model && getdata.Model.includes('ticketing');
  console.log(CDAT)

  Analysis = getdata.Model && getdata.Model.includes('analysis');
  console.log(CDAT)

  Database = getdata.Model && getdata.Model.includes('database');
  console.log(CDAT)
  


  userDetailsStore.subscribe(value => {
  userDetails = value;
  jsonString = JSON.stringify(userDetails);
  });
  
  
  onMount(() => {
        if (localStorage.getItem("userAuth")==="true"){
     
          userDetailsStore.set(JSON.parse(localStorage.getItem("userDetails")))
  
        }
        
        })

        
      function handleLogout() {
          window.location.href = '/';
      }
  
  
      onMount(() => {
      let arrow = document.querySelectorAll(".arrow");
      arrow.forEach((arrow) => {
        arrow.addEventListener("click", (e) => {
          let arrowParent = e.target.parentElement.parentElement;
          arrowParent.classList.toggle("showMenu");
        });
      });
  
      let sidebar = document.querySelector(".sidebar");
      let sidebarBtn = document.querySelector(".bi-menu-app");
  
    });
    function setActiveLink(link) {
      activelink = link;
    }

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
        await fetch(basepath() + '/logout', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          }
        })
        localStorage.setItem("userAuth", false);
        goto('/');
        window.location.reload();
      }
      function close(){
        window.location.reload();
      }

    let email = '';
    let result = '';
    let newPassword = '';
    let confirmPassword = '';
    let passwordMessage = '';
    let demo = ''
    let user_name = '';
    let showPasswordFields = false;

    async function mail_search(){
      const response = await fetch(basepath() +'/mail_search', {
        method: 'POST', 
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email }),
      });
      result = await response.json();
      if(response.ok && result.result){
        console.log("Email verified: ", result.result);
        showPasswordFields = true;
      } else {
        console.log("Error: ", result.Error);
        showPasswordFields = false;
      }
    }

    async function updatePassword() {
      if (newPassword !== confirmPassword ) {
        alert("passwordMismatch");
      }

      const response = await fetch(basepath() +'/password_update', {
        method: 'POST', 
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email, pass1: newPassword, pass2:confirmPassword})
      });
      const responseData = await response.json();
      if (response.ok) {
        if(responseData.error){
          alert(responseData.error);
          return;
        };
        alert("New Password Updated!!!!!!!!!!");
        logout();
      } else {
        alert("Password Not Updated");
      }
    }
    


</script> -->
<!-- <main>
  <nav class="navbar navbar-dark">
    <div class="p-2 bd-highlight navbar-brand">
      <img src="/state.png" alt="Logo" class="navbar-logo">
      <span class="brand-text">SIB Andhra Pradesh</span>
    </div>
    <div class="p-2 bd-highlight">
      <img src="{userDetails.profileImageUrl}" class="user-icon" alt="User Image"> 
      <button type="button" class="btn text-white" data-bs-toggle="modal" data-bs-target="#myModal1"><i class="bi bi-person-circle"></i></button>
      <div class="modal fade" id="myModal1" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true" data-bs-backdrop="static">
        <div class="modal-dialog position-absolute top-0" style="right: 10px; width: 400px;">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title text-dark" id="exampleModalLabel">{userDetails.officername} Profile</h5>
              <button data-bs-toggle="tooltip" data-bs-placement="top" title='Reset Password' type="button" class="btn btn-outline-primary">Reset <i class="bi bi-key"></i></button> 
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
              <button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">Reset Password</button>
              <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
                <div class="offcanvas-header">
                  <h5 id="offcanvasRightLabel">Reset Password</h5>
                  <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                </div>
                <div class="offcanvas-body">
                  <label class="mb-3">Enter Your Email ID: </label>
                  <div class="input-group mb-3">
                    <input type="text" class="form-control" placeholder="Enter Email ID" bind:value={email} aria-label="Enter Email ID" aria-describedby="button-addon2">
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
                      <p>{passwordMessage}</p>
                      <button class="btn btn-success" type="button" on:click={updatePassword}>Update Password</button>
                    </div>
                  {/if}
                </div>
              </div>
              <button on:click={close} type="button" class="btn btn-outline-primary">Close</button>
              <button on:click={logout} type="button" class="btn btn-outline-danger">Logout</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
  <div class="sidebar close">
    <ul class="nav-links">
      <li>
        <div class="iocn-link ">
          <a href="/dashboard">
            <i class="bi bi-grid-fill"></i>
            <span class="link_name link-text">Dashboard</span>
          </a>
          <p class="text-white ">Dashboard</p>
        </div>
      </li>
       Rder cdat routes 
      {#if CDAT === true || CDAT === ''}
      <li>
        <div class="iocn-link">
          <a href="/cdat" on:click={() => setActiveLink('cdat')} >
            <i class="bi bi-telephone-fill"></i>
            <span class="link_name">CDAT</span>
          </a>
          <p class="text-white " style="margin-left: 18px;">CDAT</p>
        </div>
        <ul class="sub-menu">
          <li><a class="link_name" href="">CDAT</a></li>
          <li><a href="/cdat/profile" class:selected={activelink === 'cdat-profile'} on:click={() => setActiveLink('cdat-profile')} >Profile</a></li>
          <li><a href="/cdat/summary" class:selected={activelink === 'cdat-summary'} on:click={() => setActiveLink('cdat-summary')} >SUMMARY</a></li>
          <li><a href="/cdat/calldetails" class:selected={activelink === 'cdat-calldetails'} on:click={() => setActiveLink('cdat-calldetails')} >CALL DETAILS</a></li>
          <li><a href="/cdat/locations" class:selected={activelink === 'cdat-locations'} on:click={() => setActiveLink('cdat-locations')} >LOCATION</a></li>
          <li><a href="/cdat/suspecteddb" class:selected={activelink === 'cdat-suspecteddb'} on:click={() => setActiveLink('cdat-suspecteddb')} >SUSPECTED DB</a></li>
          <li><a href="/cdat/search" class:selected={activelink === 'cdat-search'} on:click={() => setActiveLink('cdat-search')} >SEARCH</a></li>
          <li><a href="/cdat/imeisearch" class:selected={activelink === 'cdat-imeisearch'} on:click={() => setActiveLink('cdat-imeisearch')} >IMEI SEARCH</a></li>
          <li><a href="/cdat/summary_ipdr" class:selected={activelink === 'cdat-imeisearch'} on:click={() => setActiveLink('cdat-imeisearch')} >IPDR SUMMARY</a></li>
          <li><a href="/cdat/analysis"  >Analysis</a></li>
        </ul>
      </li>
      {/if}
      {#if Nexus === true || Nexus === ''}
      <li>
        <div class="iocn-link">
          <a href="/nexus">
            <i class="bi bi-reception-4"></i>
            <span class="link_name">NEXUS</span>
          </a>
          <p class="text-white " style="margin-left: 16px;">Nexus</p>
          <i class="bi bi-chevron-down arrow"></i>
        </div>
        <ul class="sub-menu">
          <li><a class="link_name" href="/nexus">NEXUS</a></li>
        </ul>
      </li>
      {/if}
      {#if Ticketing === true || Ticketing === ''}
      <li>
        <div class="icon-link">
          <a href="/ticketing/allinONE">
            <i class="bi bi-ticket-detailed-fill"></i>
            <span class="link_name">TICKETING</span>
          </a>
          <p class="text-white" style="margin-left: 3px;">Ticketing</p>
          <ul class="sub-menu blank">
            <li><a class="link_name" href="/ticketing/Dashboard">Report</a></li>
          </ul>
        </div>
      </li>
      {/if}
      {#if vigor === true || vigor === ''}
      <li>
        <div class="icon-link">
          <a on:click={loginToVigor} >
            <i class="bi bi-record-btn-fill"><a class="link_name" >VIGOR</a></i>
            <span class="link_name">VIGOR</span>
          </a>
          <p class="text-white" style="margin-left: 16px;">Vigor</p>
          <ul class="sub-menu blank">
            <li><a class="link_name" href="/vigor">VIGOR</a></li>
          </ul>
        </div>
      </li>
      {/if}
      {#if Analysis === true || Analysis === ''}
      <li>
        <div class="icon-link">
          <a href="/analysis">
            <i class="bi bi-graph-up"></i>
            <span class="link_name">ANALYSIS</span>
          </a>
          <p class="text-white " style="margin-left: 6px;">Analysis</p>
          <ul class="sub-menu blank">
            <li><a class="link_name" href="/analysis/cases">Cases</a></li>
            <li><a class="link_name" href="/analysis/map">Map</a></li>
            <li><a class="link_name" href="/analysis/tower_map">Tower Map</a></li>
            <li><a class="link_name" href="/analysis/common_map">Common Link</a></li>
            <li><a class="link_name" href="/analysis/analysis">analysis</a></li> 
            <li><a class="link_name" href="/analysis/tower_analysis">Tower Analysis</a></li>
          </ul>
        </div>
      </li>
      {/if}
      {#if Database === true || Database === ''}
      <li>
        <div class="icon-link">
          <a href="/database">
            <i class="bi bi-database-add"></i>
          </a>
          <p class="text-white ">DataBase</p>

        </div>
      </li>
      {/if}
      <li>
        <div class="profile-details">
          <div class="profile-content">
          </div>
          <div class="name-job">
             <div class="profile_name">Prem Shahi</div>
            <div class="job">Web Desginer</div> 
          </div>
          <a href="#" on:click={handleLogout}>
          <i class="bi bi-box-arrow-right"></i>
          </a>
        </div>
      </li>
    </ul>
  </div>
</main> -->


<!-- <style>
  .sidebar{
    position: fixed;
    top: 0;
    left: 0;
    height: 100%;
    width: 300px;
    background: #536976;
    background: -webkit-linear-gradient(to top, #536976, #292e49); /* Chrome 10-25, Safari 5.1-6 */
    background: linear-gradient(to top, #536976, #292e49); 
    z-index: 100;
    transition: all 0.5s ease;
  }
  .sidebar.close{
    width: 78px;
  }
  .sidebar .logo-details i{
    font-size: 30px;
    color: #fff;
    height: 50px;
    width: 100vw;
    background-color: black;
  }
  .sidebar .nav-links{
    height: 100%;
    padding: 30px 0 150px 0;
    overflow: auto;
  }
  .sidebar.close .nav-links{
    overflow: visible;
  }
  .sidebar .nav-links::-webkit-scrollbar{
    display: none;
  }
  .sidebar .nav-links li{
    position: relative;
    list-style: none;
    transition: all 0.4s ease;
  }
  .sidebar .nav-links li .iocn-link{
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .sidebar.close .nav-links li .iocn-link{
    display: block
  }
  .sidebar .nav-links li i{
    height: 50px;
    min-width: 78px;
    text-align: center;
    line-height: 50px;
    color: #fff;
    font-size: 20px;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  .sidebar .nav-links li.showMenu i.arrow{
    transform: rotate(-180deg);
  }
  .sidebar.close .nav-links i.arrow{
    display: none;
  }
  .sidebar .nav-links li a{
    display: flex;
    align-items: center;
    text-decoration: none;
  }
  .sidebar .nav-links li a .link_name{
    font-size: 18px;
    font-weight: 400;
    color: #fff;
    transition: all 0.4s ease;
  }
  .sidebar.close .nav-links li a .link_name{
    opacity: 0;
    pointer-events: none;
  }
  
  .sidebar .nav-links li .sub-menu{
    padding: 6px 6px 14px 80px;
    margin-top: -10px;
    background: #536976;
    border-radius: 20px;
    display: none;
  }
  .sidebar .nav-links li.showMenu .sub-menu{
    display: block;
  }
  .sidebar .nav-links li .sub-menu a{
    color: #fff;
    font-size: 15px;
    padding: 5px 0;
    white-space: nowrap;
    opacity: 0.6;
    transition: all 0.3s ease;
  }
  .sidebar .nav-links li .sub-menu a:hover{
    opacity: 1;
  }
  .sidebar.close .nav-links li .sub-menu{
    position: absolute;
    left: 100%;
    top: -10px;
    margin-top: 0;
    padding: 10px 20px;
    border-radius: 0 6px 6px 0;
    opacity: 0;
    display: block;
    pointer-events: none;
    transition: 0s;
  }
  .sidebar.close .nav-links li:hover .sub-menu{
    top: 0;
    opacity: 1;
    pointer-events: auto;
    transition: all 0.4s ease;
    /* position: fixed; */
  }
  .sidebar .nav-links li .sub-menu .link_name{
    display: none;
  }
  .sidebar.close .nav-links li .sub-menu .link_name{
    font-size: 18px;
    opacity: 1;
    display: block;
  }
  .sidebar .nav-links li .sub-menu.blank{
    opacity: 1;
    pointer-events: auto;
    padding: 3px 20px 6px 16px;
    opacity: 0;
    pointer-events: none;
  }
  .sidebar .nav-links li:hover .sub-menu.blank{
    top: 50%;
    transform: translateY(-50%);
  }
  .sidebar .profile-details{
    position: fixed;
    bottom: 0;
    width: 260px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #536976;
    padding: 12px 0;
    transition: all 0.5s ease;
  }
  .sidebar.close .profile-details{
    background: none;
  }
  .sidebar.close .profile-details{
    width: 78px;
  }
  .sidebar .profile-details .profile-content{
    display: flex;
    align-items: center;
  }
  
  @media (max-width: 400px) {
    .sidebar.close .nav-links li .sub-menu{
      display: none;
    }
    .sidebar{
      width: 78px;
    }
    .sidebar.close{
      width: 0;
    }
  } 
  .sidebar .nav-links li i {
    color: #fff;
  }
  
  .sidebar .nav-links li a .link_name {
    display: block;
    text-align: center; 
    color: #fff;
    font-size: 18px; 
  }
  
  .sidebar.close .nav-links li i {
    display: inline-block; 
  }
  
  .sidebar.close .nav-links li a .link_name {
    display: none; 
  }
  .link-text {
    display: block;
    text-align: center;
    margin-top: -3px;
  }
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: -webkit-linear-gradient(to top, #4c5088, #7e83a1); 
    background: linear-gradient(to top, #3c4253, #292e49); 
    color: rgb(241, 240, 240);
    padding: 10px 20px;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1;
    width: 100%;
    height: 50px;
  }

  .navbar .nav-links a {
    color: rgb(243, 240, 240);
    text-decoration: none;
    margin-left: 200px;
    font-size: 18px;
  }

  .navbar .nav-links a:hover {
    text-decoration: underline;
  }
  .navbar-brand {
    font-size: 2rem;
    font-weight: bold;
    color: #fff;
    margin-left: 59px;
    margin-top: -17px;
  }

  .navbar-logo {
    height: 40px;
    width: auto;
    margin-right: 10px;
    margin-top: -17px;
    object-fit: cover;
    border-radius: 50%;
  }

  .brand-text {
    display: inline-block;
    margin-top: -20px;
  }
  
  .bd-highlight {
    margin-top: -13px;
  }
</style> -->