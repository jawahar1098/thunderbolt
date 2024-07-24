<script>
    // @ts-nocheck
  
    import './global.css';
    import {onMount , onDestroy} from 'svelte';
    import {goto} from '$app/navigation';
    import {basepath} from "$lib/config"
    import { userDetailsStore } from '$lib/datastore.js';
    import flatpickr from 'flatpickr';
    import 'flatpickr/dist/flatpickr.css';

    let userDetails;
    userDetailsStore.subscribe(value => {
    userDetails = value;
    });
    onMount(() => {
    // beware of truthy and falsy values
    if (localStorage.getItem("userAuth")==="true"){
    userDetailsStore.set(JSON.parse(localStorage.getItem("userDetails")))
    ticket_dash();
    }
    else{
    goto('/');
    }
    });

let result = [];
  async function ticket_dash() {
    const response = await fetch(basepath()+"/ticket_dash", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email:userDetails.email,
        team:userDetails.team,
        modules:userDetails.modules,
        designation:userDetails.designation,
        role:userDetails.role,


    }),
    });
    if (response.ok){
      result = await response.json();
      console.log(result)
    }
  }

</script>
<style>
    
 h1 {
    margin-left: 470px;
    margin-top: 14px;
    font-family: Georgia, "Times New Roman", Times, serif;
    font-size: 4rem;
    font-weight: bold;
    color: transparent;
    background: linear-gradient(to right, #000000, #000000, #000000); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
    background-clip: text;
    font-style: italic;

    }
h3{
    font-family: Georgia, "Times New Roman", Times, serif;
    font-size: 2rem;
    font-weight: bold;
    text-align: center;
    font-style: italic;
}
.card{
    background: linear-gradient(to right, #ffffff, #ffffff); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
    border-radius: 7px !important;
    box-shadow: 0 .5rem 4rem rgb(0, 0, 0)!important;    
    font-family: Georgia, "Times New Roman", Times, serif;
    font-size: 2rem;
    text-align: center;
    font-style: italic;
}
button{
    font-style: italic;
}
.right-side-container {
    position: fixed;
    top: 0;
    right: 0;
    width: 29%;
    height: 100%; /* Adjust as needed */
    color: white;
    background-color: #343a40 !important; /* Optionally set background color */
}
.userdata{
    margin-left: 25px;
    font-size: 1.4rem;
    text-align: center;
    margin-top: 40px;
}
.data{
    margin-left: 10px;
}
.user-data{
    margin-left: 70px;
}

</style>
<div class="right-side-container">
        <h3 style="font-family: Georgia, Times New Roman, Times, serif;font-size: 4rem;margin-right: 270px;margin-top: 7px;">User Info</h3>
        <div class="d-flex justify-content-right align-items-center" style="margin-left: 155px; margin-top: 94px">
            <img src="../../src/public/Images/logo.png" alt="Generic placeholder image" class="img-fluid" style="width: 250px; border-radius: 100px;">
        </div>
        <div class="row userdata">
            <h3 style="margin-bottom: 50px;margin-left:-60px">{userDetails.officername}</h3>
            <div class="user-data">
                {#if userDetails.designation !== 'Administrator'}
                <div class="d-flex justify-content-left">
                    <p><b>Superior</b></p><p style="margin-left: 109px;">:</p>
                    <p class="data">{userDetails.superior}</p>
                </div>
                <div class="d-flex justify-content-left">
                    <p><b>Designation</b></p><p style="margin-left: 74px;">:</p>
                    <p class="data">{userDetails.designation}</p>
                </div>
                <div class="d-flex justify-content-left">
                    <p><b>Team</b></p><p style="margin-left: 145px;">:</p>
                    <p class="data">{userDetails.team}</p>
                </div>
                <div class="d-flex justify-content-left">
                    <p><b>Modules</b></p><p style="margin-left: 111px;">:</p>
                    <p class="data">{userDetails.modules}</p>
                </div>
                <div class="d-flex justify-content-left">
                    <p><b>Email</b></p><p style="margin-left: 140px;">:</p>
                    <p class="data">{userDetails.email}</p>
                </div>
                <div class="d-flex justify-content-left">
                    <p><b>Role</b></p><p style="margin-left: 150px;">:</p>
                    <p class="data">{userDetails.role}</p>
                </div>
            {:else}
            <div class="d-flex justify-content-left">
                <p><b>Designation</b></p><p style="margin-left: 74px;">:</p>
                <p class="data">{userDetails.designation}</p>
            </div>
            <div class="d-flex justify-content-left">
                <p><b>Email</b></p><p style="margin-left: 140px;">:</p>
                <p class="data">{userDetails.email}</p>
            </div>
            {/if}
            </div>
        </div>
    </div>
<main>
    <div class="main_card" style="background-color: aliceblue;">
        <div class="d-flex justify-content-right align-items-center">
            <h1 style="font-weight: bold;font-family:'Times New Roman', Times, serif; color: #333;">Tickets Summary</h1>
        </div>
        {#if userDetails.designation !== 'Administrator'}
            <div class="d-flex justify-content-right align-items-center" style="height: 200px;">
                <div class="data_tickets" style="width: 650px;margin-top:260px;margin-left:20px">       
                    <div class="card rounded-3 shadow" style="height: 360px; background-color: #fff;">
                        <h3 class="card-header bg-primary text-white">Data Tickets</h3>
                        <div class="card-body">
                        <h3 class="card-title">Total My Data Tickets</h3>
                        <p class="card-text">{result.mydata}</p>
                        {#if userDetails.role === 'Analyst'}
                        <button on:click={()=> goto("/ticketing/Datareq/")} class="btn btn-primary mt-3" style="margin-top: 122px;">Go To Data Tickets</button>
                        {:else}
                        <h3 class="card-title">Total Others Data Tickets</h3>
                        <p class="card-text">{result.otherdata}</p>
                        <button on:click={()=> goto("/ticketing/Datareq/")} class="btn btn-primary mt-3">Go To Data Tickets</button>
                        {/if}
                        </div>
                    </div>
                </div>
                <div class="data_tickets" style="width: 650px;margin-top:260px;margin-left:20px; ">
                    <div class="card rounded-3 shadow" style="height: 360px; background-color: #fff;">
                        <h3 class="card-header bg-success text-white">Analysis Tickets</h3>
                        <div class="card-body">
                        <h3 class="card-title">Total My Analysis Tickets</h3>
                        <p class="card-text">{result.myanalysis}</p>
                        {#if userDetails.role === "Mailer"}
                        <button on:click={()=> goto("/ticketing/Analysisreq/")} class="btn btn-dark" style="margin-top: 122px;">Go To Analysis Tickets</button>
                        {:else}
                        <h3 class="card-title">Total Others Analysis Tickets</h3>
                        <p class="card-text">{result.otheranalysis}</p>
                        <button on:click={()=> goto("/ticketing/Analysisreq/")} class="btn btn-success mt-3">Go To Analysis Tickets</button>
                        {/if}
                        </div>
                    </div>
                </div>
                </div>
                <div class="d-flex justify-content-right align-items-center" style="height: 550px;">
                <div class="data_tickets" style="width: 650px;margin-top:260px;margin-left:20px">
                    <div class="card rounded-3 shadow" style="background-color: #fff;">
                        <h3 class="card-header bg-info text-white">Report</h3>
                        <div class="card-body">
                        <h3 class="card-title">Total Data Tickets</h3>
                        <p class="card-text">{result.report_data}</p>
                        <h3 class="card-title">Total Analysis Tickets</h3>
                        <p class="card-text">{result.report_analysis}</p>
                        <button on:click={()=> goto("/ticketing/Dashboard/")} class="btn btn-info mt-3">Go To Report</button>
                        </div>
                    </div>
                </div>
                <div class="data_tickets" style="width: 650px;margin-top:260px;margin-left:20px">
                    <div class="card text-center rounded-3 shadow" style="height: 360px; background-color: #fff;">
                        <h3 class="card-header bg-warning text-white">Nickname Database</h3>
                        <div class="card-body">
                        <h3 class="card-title">Total Nickname Created</h3>
                        <p  class="card-text" style="font-size: xx-large;">{result.nickname}</p>
                        <button on:click={()=> goto("/ticketing/Nickname/")} class="btn btn-warning mt-3" style="margin-top: 122px;">Go To NickName Database</button>
                        </div>
                    </div>
                </div>
            </div>
        {:else}
            <div class="d-flex justify-content-right align-items-center" style="height: 200px;">
                <div class="data_tickets" style="width: 650px;margin-top:260px;margin-left:20px">
                    <div class="card text-center rounded-3 shadow" style="height: 360px; background-color: #fff;">
                        <h3 class="card-header bg-danger text-white">User Registration</h3>
                        <div class="card-body">
                        <h3 class="card-title">Total User Created</h3>
                        <p class="card-text" style="font-size: xx-large;">{result.totalusers}</p>
                        <button on:click={()=> goto("/ticketing/superadmin/")} class="btn btn-danger mt-3" style="margin-top: 50px;">Go To Registration</button>
                        </div>
                    </div>
                </div>
                <div class="data_tickets" style="width: 650px;margin-top:260px;margin-left:20px">
                    <div class="card text-center rounded-3 shadow" style="height: 360px; background-color: #fff;">
                        <h3 class="card-header bg-warning text-white">Nickname Database</h3>
                        <div class="card-body">
                        <h3 class="card-title">Total Nickname Created</h3>
                        <p  class="card-text" style="font-size: xx-large;">{result.nickname}</p>
                        <button on:click={()=> goto("/ticketing/Nickname/")} class="btn btn-warning mt-3" style="margin-top: 50px;">Go To NickName Database</button>
                        </div>
                    </div>
                </div>
            </div>
        {/if}
    </div>
</main>