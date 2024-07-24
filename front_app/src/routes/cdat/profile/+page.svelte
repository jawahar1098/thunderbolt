<script>
  // @ts-nocheck

  import { onMount } from "svelte";
  import { page } from "$app/stores";
  import Cdrprofile from "$lib/profileview/Cdrprofile.svelte";
  import Ipdr from "$lib/profileview/Ipdr.svelte";
  import Towerprofile from "$lib/profileview/Towerprofile.svelte";
  // import { FALSE } from "ol/functions";
  // import Vigor from "$lib/vigor/Vigor.svelte";
  import { userDetailsStore } from '$lib/datastore.js';
  import { postRequest } from "$lib/req_utils";

  import { basepath } from "$lib/config";

  let reloadKey = 0;
  let number;
  let bottomRightHomeContentHeading = "profile";
  let gotResult = false;
  let propData;
  let isSubmitted = false;
  let selectedmode = "";
  let mode = "";
  let img = false;
  let img_path;
  let name = "";
  let nameinput = false;

  onMount(() => {
    const urlParams = new URLSearchParams($page.url.search);
    const urlnumber = urlParams.get("value");
    const urlmode = urlParams.get("mode");

    if (urlnumber !== null) {
      propData = {};
      console.log(urlnumber, "---number");
      number = urlnumber;
      gotResult = true;
      propData["number"] = number;
      handleSubmit();
    }
  });

  function handleSubmit() {
    propData = {};
    const ele = document.getElementById("display_div");
    isSubmitted = true;
    mode = selectedmode;
    gotResult = true;
    propData["number"] = number;
    if (ele) {
      ele.style.display = "block";
    }
    fetchImage();
  }

  function fetchImage() {
    fetch(`${basepath()}/picture`, {
      method: "post",
      body: JSON.stringify({ number: number }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data, "--------------------imgpath --------------------");
        if (data.status === "success") {
          img_path = data.img_path;
          img = true;
        } else {
          img = false;
        }
        if (data.imgstatus === "success") {
          name = data.name;
          nameinput = true;
        } else {
          nameinput = false;
          name = "not found";
        }
      });
  }
</script>

<main>
  <div class="inputs cursor-pointer d-flex">
    <!-- <div class="ml-3"></div> -->
    <label class="mx-3 font-bold" for="mobileNumber"
      >Enter Value for {bottomRightHomeContentHeading.toUpperCase()}</label
    >
    <input
      class="form-control s-hRLDX_Gekubi border-amber-700"
      id="mobileNumber"
      type="text"
      placeholder="Enter a Number"
      size="10"
      bind:value={number}
    />
    <button class="btn btn-success mx-2" on:click={handleSubmit}>Submit</button>
  </div>
</main>
<div class="container_main">
  {#if gotResult}
    <div class="row_container">
      <div class="collumn_container">
        <div class="card">
          <div class="card-body">
            <div class="image_profile">
              <div class="profile-img">
                <!-- svelte-ignore a11y-img-redundant-alt -->
                {#if img}
                  <img
                    src={`${basepath()}/attach/` + img_path}
                    alt="Profile Picture"
                    class="profile-picture margin-leftimg-fluid rounded-circle"
                  />
                {:else}
                  <img
                    src="../propic.jpeg"
                    alt="Profile Picture"
                    class="profile-picture margin-leftimg-fluid rounded-circle"
                  />
                {/if}

                <div class="detail">
                  <div class="detail_content">
                    <p id="number">Number</p>
                    <p id="blur">{number}</p>
                  </div>
                  {#if nameinput}
                    <div class="detail_content">
                      <p>Name</p>
                      <p id="blur">{name}</p>
                    </div>
                  {:else}
                    <div class="detail_content">
                      <p>Name</p>
                      <p id="blur">{name}</p>
                    </div>
                  {/if}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="collumn_container mb-2">
        <div class="card">
          <div class="card-body">
            <Cdrprofile {propData} />
          </div>
        </div>
      </div>
      <div class="collumn_container mb-2">
        <div class="card">
          <div class="card-body">
            <Ipdr {propData} />
          </div>
        </div>
      </div>
      <div class="collumn_container mb-2">
        <div class="card">
          <div class="card-body">
            <Towerprofile {propData} />
          </div>
        </div>
      </div>
      <!-- <div class="column">
        <div class="card">
          <div class="card-body">
            <Vigor {propData} />
          </div>
        </div>
      </div> -->
    </div>
  {/if}
</div>

<style>
  
  .inputs {
    margin-left: 5%;
    margin-top: 2%;
    margin-right: 5%;
  }
  button {
    height: 3rem;
    border-radius: 5px;
  }
  .container_main {
    width: 100%;
    margin-top: 1%;
    height: 91vh;
    background-color: rgba(30, 80, 134, 0.07);
    overflow: scroll;
  }
  .row_container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    width: 94.1%;
    margin-left: 5%;
    gap: 1vw;
    background-color: rgba(30, 80, 134, 0.07);
    height: 89.5vh;
  }
  .collumn_container {
    width: 23%;
    margin-top: 1%;
    border-radius: 50%;
  }
  .card {
    position: relative;
    display: flex;
    flex-direction: column;
    min-width: 0;
    word-wrap: break-word;
    background-color: #fff;
    background-clip: border-box;
    border: 1px solid rgba(0, 0, 0, 0.125);
    border-radius: 15px;
    box-shadow: 0px 0.2em 0.4em rgb(35 123 191 / 40%);
    height: 86vh;
  }
  .image_profile {
    display: flex;
    align-items: center;
    width: 100%;
  }
  .form-control {
    /* filter: blur(4px); */
  }
  .profile-picture {
    width: 71%;
    margin-top: 5vh;
    /* filter: blur(9px); */
  }
  #blur {
    /* filter: blur(4px); */
  }
  .profile-img {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    margin-bottom: 1vh;
  }
  .detail_content {
    display: flex;
    justify-content: space-between;
    gap: 16px;
    /* margin-top: 1rem; */
    font-size: 1.3em;
  }
  p {
    margin: 0;
  }
  .label_title {
    background-color: #3498db; /* Blue background color */
    color: #fff; /* White text color */
    padding: 1rem;
  }
  .next_sec {
    /* sbox-shadow: 0px 0.2em 0.4em rgb(35 123 191 / 40%); */
    padding: 1%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  img {
    margin-bottom: 2vh;
  }
  .detail {
    margin: 2vh;
  }
  .card-body {
    display: flex;
  }
  .column {
    height: 10vh;
    width: 100vw;
  }
</style>
