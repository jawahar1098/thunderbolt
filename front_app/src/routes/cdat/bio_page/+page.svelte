<script>
    // @ts-nocheck



let bottomRightHomeContentHeading = "info";
let number;
let isSubmitted = false;
let gotResult = false;

let susdb = []
let sdrdb = []
let osint = []

let numvalue = [{'name':"siva",'number':'9876543210', 'caseno':'5555555','officer':'rajkumar','address':'no.32, vivekananda strret, porur,614617','voice sample':'Available','source':'susdb'},{'name':'siva','number':'9876543210','fathername':'rajkumar','address':'no.32, vivekananda strret, porur, 614617','cdr':'Available','ipdr':'Available','tower':'Not Available','source':'sdrdb'},{'truecaller':'siva','fb':'siva_vps','twitter':'tibo','insta':'siva_vps','source':'osint'}]

let namevalue = [
    {'name':"ramesh",'number':'9876543210', 'caseno':'34123','officer':'kiran','address':'no.5,jaith street, sahara.','voice sample':'Available','source':'susdb'},{'name':"ramesh kumar",'number':'9876567854', 'caseno':'34157','officer':'subash','address':'no.6,valajabath, potheri.','voice sample':'Not Available','source':'susdb'},{'name':'ramesh','fathername':'senthil','address':'no.15, rangarajan street, colony, osur.','cdr':'Available','ipdr':'Not Available','tower':'Available','source':'sdrdb'},{'name':'ramesh kumar','fathername':'raja','address':'no.45, teenagar, tamabaram.','cdr':'Available','ipdr':'Available','tower':'Available','source':'sdrdb'},{'name':'ramesh raj','fathername':'deva raj','address':'no.3 , nehru street, kelambakam.','cdr':'Available','ipdr':'Available','tower':'Available','source':'sdrdb'},{'truecaller':'ramesh','fb':'ramesh_1978','twitter':'ramesh@123','insta':'1998_ramesh','source':'osint'},{'truecaller':'ramesh kannan','fb':'kannan','twitter':'kaali_23','insta':'kannan_@3','source':'osint'}
]
function handleSubmit() {
     if (number === "9876543210"){
        numvalue.forEach(items => {

            if(items['source'] === "susdb"){
                susdb.push(items)
                
            }
            if(items['source'] === "sdrdb"){
                sdrdb.push(items)
                
            }
            if(items['source'] === "osint"){
                osint.push(items)
                
            }
        }
        )
        gotResult = true
     }

     if (number === "ramesh"){
        namevalue.forEach(items => {

            if(items['source'] === "susdb"){
                susdb.push(items)
                
            }
            if(items['source'] === "sdrdb"){
                sdrdb.push(items)
                
            }
            if(items['source'] === "osint"){
                osint.push(items)
                
            }
        }
        )
        gotResult = true
     }
}
</script>

<main>
    <div class="inputs cursor-pointer d-flex">
        <div class="ml-3"></div>
        <label class="mx-3 font-bold" for="mobileNumber">Enter Value for {bottomRightHomeContentHeading.toUpperCase()}</label>
        <input
          class="form-control s-hRLDX_Gekubi border-amber-700"
          id="mobileNumber"
          type="text"
          placeholder="Enter a number or name"
          size="10"
          bind:value={number}
        />
        <button class="btn btn-success mx-2" on:click={handleSubmit}>Submit</button>
    </div>
    {#if gotResult}
    <div class="container_main">
            <div class="card">
                <h2 style="text-align: center;">Suspect DB</h2>
                <div class="suscard ">
                    {#each susdb as _sus}
                        <div class="sub-suscard ">
                            <div class="col-7">
                                <p>Name : {_sus.name}</p>
                                <p>Number : {_sus.number}</p>
                                <p>Case No: {_sus.caseno} </p>
                                <p>Officer: {_sus.officer}</p>
                                <p>Address: {_sus.address}</p>
                                <p>Voice Note: {_sus.voice}</p>
                            </div>
                            <div class="col-5">
                                <img class="profile-picture" src="/propic.jpeg" alt="">
                            </div>
                        </div>
                    {/each}
                </div>
            </div>
            
            <!-- SDR -->
            <div class="sdrcard">
                <div class="row card_2 align-items-start">
                    <h2 style="text-align: center;">SDR DB</h2>
                    {#each sdrdb as sdr}
                    <div class="col">
                        <div class="row">

                            <div class="col-7">
                                <p>Name : {sdr.name} </p>
                                <p>Father Name : {sdr.fathername}</p>
                                <p>Address: {sdr.address} </p>
                                <p>CDR: {sdr.cdr}</p>
                                <p>IPDR: {sdr.ipdr}</p>
                                <p>Tower: {sdr.tower}</p>
                            </div>
                            <div class="col-4">
                                <img class="profile-picture" src="/4.jpeg" alt="">
                            </div>
                        </div>

                    </div>
                    {/each}
                   
                  </div>
                
            </div>

            <!-- OSINT CARD -->
            <div class="sdrcard">
                <div class="row card_2 align-items-start">
                    <h2 style="text-align: center;">OSINT REC</h2>
                    {#each osint as _o}
                    <div class="col">
                        <div class="row">

                            <div class="col-7">
                                <p>Truecaller : {_o.truecaller}</p>
                                <p>FB : {_o.fb}</p>
                                <p>Twitter: {_o.twitter}</p>
                                <p>Insta: {_o.insta}</p>
                            </div>
                            <div class="col-4">
                                <img class="profile-picture" src="/propic.jpeg" alt="">
                            </div>
                        </div>

                    </div>
                    {/each}
                </div>
                
            </div>
            <div class="darkweb">
                <div class="row card_2 align-items-start">
                    <h2 style="text-align: center;">Dark Web</h2>
                    <div class="col">
                        <div class="row">
                            
                            <div class="col-7">
                                <p>No Data Available</p>
                            </div>
                            
                        </div>

                    </div>
                </div>
            </div>
        
        
    </div>
    {:else}
    <p style="text-align: center; margin-top:30px;">No Data</p>
    {/if}

</main>

<style>
  .inputs {
    margin-left: 5%;
    margin-top:4%;
    margin-right: 5%;
  }
  button {
    height: 3rem;
    border-radius: 5px;
  }

  main {
        font-family: Arial, sans-serif;
        margin-left: 7%;
        padding: 0;
        /* width: 90%; */
    }
.container_main{
    margin-top: 1%;
    overflow-y: scroll;
    height: 80vh;
}    

.profile-picture{
    width: 71%;
    margin-top: 3vh;
    /* filter: blur(9px); */
  }

    
.card {
    width: 97%; 
    background-color: #f0f0f0;
    border: 1px solid #ddd;
    border-radius: 8px;
    margin-bottom: 5px;
    /* padding-left: 10px; */
    box-sizing: border-box;
    padding: 5px;
}

.sdrcard {
    width: 97%; 
    background-color: #f0f0f0;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-sizing: border-box;
    padding: 5px;

}
.darkweb{
    width: 97%; 
    background-color: #f0f0f0;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-sizing: border-box;
    padding: 5px;
}
.card_2 {
    background-color: #ffffff;
    /* border: 1px solid #ddd; */
    border-radius: 8px;
    box-sizing: border-box;
    overflow-x: scroll;
    margin: 0.5em;
}
.suscard{
    background-color: rgb(255, 255, 255);
    /* width: 50%; */
    display:flex;
    border-radius: 8px;
    margin:0.5em;
}
.sub-suscard{
    display:flex;
    width:50%;
    margin: 0.5em;
}
/* .col-2
{
  flex: 0 0 auto;
  width: 20%;

} */
@media only screen and (max-width: 768px) {
    .card {
        width: calc(100% - 20px); /* 100% width on smaller screens */
    }
}
</style>