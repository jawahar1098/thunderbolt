<script>
    import { basepath } from '$lib/config';
    
    let totalmails = 0;
    let catteam = [];
    let isotteam = [];
    let apteam = []
    let cdrupdates;
    let ipdrupdates
    let table = [];
    let showtable = false
	
	

    function get_data(){
        fetch(`${basepath()}/mail_stat`,{
            method: 'post',
            
        })
        .then(res => res.json())
        .then(data => {
            console.log(data)
            if (data.status === "success"){
                const resp = data.data
                resp.forEach(item => {
                    if(item['team'] === 'cat' && item['count'] !== 0){
                        catteam.push(item)
                        totalmails += item['count']
                    }
                    if(item['team'] === 'isot' && item['count'] !== 0){
                        isotteam.push(item)
                        totalmails += item['count']
                    }
                    if(item['team'] === 'ap' && item['count'] !== 0){
                        apteam.push(item)
                        totalmails += item['count']
                    }
                })

            }
            
            console.log(totalmails,catteam,isotteam)
            // rendertable('cat')
        })
    }
    get_data()

    function rendertable(team){
        console.log(team)
        table= []
        if(team === 'cat'){
            console.log("=====================")

            table = catteam
            showtable = true
        }
        if (team === 'ap'){
            showtable = true
            table= apteam
        }
        if (team === 'isot'){
            showtable=true
            table = isotteam
        }
        console.log(table)
    }
   
</script>
<main>

   

    <div class="showdata row">
        <div class="col-5 parentbox">
            <b>Total Mails Sent</b>: {totalmails} <br>
            <b>Cdr last updated</b>: {cdrupdates} <br>
            <b>Ipdr last updated</b>: {ipdrupdates} <br>
          </div>
        <div class="col-7">
            <div>
                <div class="teamselection text-end">
                        <button class="btn " on:click={() => {rendertable('cat')}}>cat</button>
                        <button class="btn" on:click={() => {rendertable('isot')}}>isot</button>
                        <button class="btn" on:click={() => {rendertable('ap')}}>ap</button>
                </div>
                {#if showtable}
                    {#if table.length > 0}
                        <table class="table table-custom table-striped table-bordered">
                            <thead class="thead-custom">
                            
                            <tr>
                                <th>Request Type</th>
                                <th>Provider</th>
                                <th>Counts</th>
                            </tr>
                            </thead>
                            <tbody>
                            {#each table as row}
                                <tr>
                                <td>{row['req_type']}</td>
                                <td>{row['provider']}</td>
                                <td>{row['count']}</td>
                                </tr>
                            {/each}
                            </tbody>
                        </table>
                    {:else}
                    <div class="text-center">
                        <p>no data</p>

                    </div>
                    {/if}
                {/if}
                
            </div>
        </div>

    </div>
    
    
</main>
<style>
    main{
        margin-left: 5%;
        margin-top: 65px;
        
    }
    button{
        width: 44vw;
    }

    .table-custom {
    background-color: #f5f5f5;
    /* width: 50%; */
  }

  .thead-custom {
    background-color: #4285f4;
    color: #fff;
  }

  .table-custom tbody tr:hover {
    background-color: #e0e0e0;
  }
    .teamselection button{
        width: 100px;
    }
    .showdata{
        width: 98%;
    }

    .parentbox {
        /* Add any additional styles for the parent box */
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 8px;
        margin-bottom: 10px;
    }

  /* Add a margin-bottom to the <b> element for some spacing */
  .parentbox{
    margin-bottom: 5px;
    padding: 50px;
    /* display: block; Display each <b> element as a block to force a new line */
  }

</style>