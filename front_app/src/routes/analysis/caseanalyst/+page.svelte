<script>
  // @ts-nocheck

  import { base } from "$app/paths";
  import { basepath } from "$lib/config";
  import Bpartysummary from "$lib/towercdr/Bpartysummary.svelte";
  import Detailview from "$lib/towercdr/Detailview.svelte";
  import Formulaone from "$lib/towercdr/Formulaone.svelte";
  import Imeisummary from "$lib/towercdr/Imeisummary.svelte";

  import { json } from "@sveltejs/kit";
  import { onMount } from "svelte";


// exportdata() in Formulaone   , sendCoordinatesToFlask(/tower)[map]
//     import Towerdata from "$lib/towercdr/Towerdata.svelte";  -NF
// func - sendNumberToFlask [commonmap] [towermap]

//  backend -- formulaOneexport




  let casename = "";
  let casetype = "";
  let result = false;
  let gotResult = false;
  let formulaone = [];
  let ind_num_val;
  let induval = false;
  let processdata;
  let filetype = "";
  let filestat = false;
  let fileup = "";
  let current_num;
  let filtervalue = "detailsview";
  let userDetails;
  let user;

  // location.reload()
  onMount(() => {
    // location.reload()
    // const params = new URLSearchParams(window.location.search);
    casename = localStorage.getItem("casename"); //params.get('casename') || '';
    casetype = localStorage.getItem("casetype"); //params.get('type') || '';
    userDetails = JSON.parse(localStorage.getItem("userDetails"));
    user = userDetails.email;
    console.log(casename, casetype);
    if (casename !== "") {
      gotResult = true;
    }
  });

  function getvalue(num) {
    current_num = num;
    induval = false;
    fetch(`${basepath()}/getvalue`, {
      method: "post",
      body: JSON.stringify({ number: num }),
    })
      .then((res) => res.json())
      .then((val) => {
        console.log(val);
        induval = true;
        ind_num_val = val;
        document.getElementById("my_modal_4").setAttribute("open", true);
      });
  }
  function getjson() {
    filestat = true;
    processdata = "Processing";
    const fileInput = document.querySelector("#fileupload");

    if (fileInput && fileInput.files.length > 0) {
      let formData = new FormData();
      console.log(fileInput.files);
      for (let i = 0; i < fileInput.files.length; i++) {
        formData.append("files", fileInput.files[i]);
        formData.append("casename", casename);
        formData.append("filetype", filetype);
      }

      console.log("Sending fetch request...");

      console.log(formData);
      fetch(`${basepath()}/getjson`, {
        method: "post",

        body: formData,
      })
        .then((res) => res.json())
        .then((response) => {
          filestat = response;
          filestat = false;
          fileup = "Upload Sucess";
          console.log(filestat);
        })
        .catch((err) => {
          console.log(err);
        });
    }
  }
</script>

<main>
  <div class="text">Case Name: {casename}</div>
  <div class="inline-block relative mr-2">
    <select
      bind:value={filtervalue}
      style="margin:0rem 0rem 0.5rem 0rem;border:none; height:2em ; border-radius:5px;background:#d4ebf7"
    >
      <option value="detailsview">Details View</option>
      <option value="casesummary">Case Summary</option>
      <option value="imeisummary">Imei Summary</option>
      <option value="bpartysummary">B party Summary</option>
    </select>
  </div>
  {#if gotResult}
    {#if filtervalue === "casesummary"}
      <Formulaone {casename} {casetype} {user} />
    {:else if filtervalue === "imeisummary"}
      <Imeisummary {casename} {casetype} {user} />
    {:else if filtervalue === "bpartysummary"}
      <!-- <div> -->
      <Bpartysummary {casename} {casetype} {user} />
      <!-- </div> -->
    {:else if filtervalue === "detailsview"}
      <Detailview {casename} {casetype} {user} />
    {/if}
  {:else}
    <div class="position-absolute top-50 start-50 translate-middle p-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  {/if}
</main>

<style>
  main {
    width: 80vw;
    margin-left: 5%;
  }
  .text {
    text-align: center;
    font-family: "Raleway";
    font-size: 1.5rem;
    font-weight: 800;
  }
</style>
