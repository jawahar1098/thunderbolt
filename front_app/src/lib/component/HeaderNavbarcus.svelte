<script>
	// import SidebarCus from "./SidebarCus.svelte";
	
	import {goto} from '$app/navigation'

	
    
   
</script>


<div>
	<button on:click={() => goto("/cdat/summary")}>Summary</button>
	<button on:click={() => goto("/cdat/callDetails")}>Calldetails</button>

</div>
