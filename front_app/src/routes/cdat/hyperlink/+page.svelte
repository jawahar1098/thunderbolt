
<script>
    // @ts-nocheck

    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import Summarybetweendates from "$lib/Summary/Summarybetweendates.svelte";
    import Totalcalls from "$lib/hyperlink/totalcalls.svelte";
    import Callout from "$lib/hyperlink/callout.svelte";
    import Callin from "$lib/hyperlink/callin.svelte";
    import Cdrprofile from "$lib/profileview/Cdrprofile.svelte";
    import Commoncalls from "$lib/hyperlink/commoncalls.svelte";
    import PhoneusedinImei from "$lib/imeisearch/PhoneusedinImei.svelte";
    import Cellidsearch from "$lib/search/Cellidsearch.svelte";
    import TowerTotalcalls from "$lib/hyperlink/tower_totalcalls.svelte";
    import OverallTowersummary from "$lib/towercdr/overalltowersummary.svelte";
    let number;
    let mode;
    let dest_number;
    let towerid;
    let fromdate;
    let todate;
    let state;
    let propData;
    console.log(fromdate,todate)
    onMount(() => {
        propData = {}
    const urlParams = new URLSearchParams($page.url.search);
        number = urlParams.get('number');
        mode = urlParams.get('mode');
        state = urlParams.get('state');
        dest_number = urlParams.get('dest_number');
        towerid = urlParams.get('towerid');
        fromdate = urlParams.get('fromdate');
        todate = urlParams.get('todate');
        propData['number'] = urlParams.get('number');
    }
    ) 

       

</script>

<div>
    {#if mode === 'summary'}
        <Summarybetweendates {propData}  />
    {/if}
    {#if mode === 'overallsummary'}
        <OverallTowersummary {number}  />
    {/if}
    {#if mode === 'total_calls'} 
        <Totalcalls {number} {dest_number} {fromdate} {todate} {state} />
    {/if}
    {#if mode === 'call_out'}
        <Callout {number} {dest_number} {fromdate} {todate} {state} />
    {/if}
    {#if mode === 'call_in'}
        <Callin {number} {dest_number} {fromdate} {todate} {state} />
    {/if}
    {#if mode === 'dest_num'}
        <Cdrprofile {number} />
    {/if}
    {#if mode === 'hyper_contact'}
        <Commoncalls {dest_number} {number} />
    {/if}
    {#if mode === 'imei'}
        <PhoneusedinImei {propData} />
    {/if}
    {#if mode === 'cellid'}
        <Cellidsearch {number} />
    {/if}
    {#if mode === 'tower_total_calls'}
        <TowerTotalcalls {number} {towerid} {mode}/>
    {/if}
    {#if mode === 'tower_day_calls'}
        <TowerTotalcalls {number} {towerid} {mode}/>
    {/if}
    {#if mode === 'tower_night_calls'}
        <TowerTotalcalls {number} {towerid} {mode}/>
    {/if}
    



</div>