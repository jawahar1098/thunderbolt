<script>
    import { goto } from "$app/navigation";
    import Sidebar from "$lib/sidebar/Sidebar.svelte";
    import { onMount } from "svelte";


    let casename = 'No case';
    
    onMount(()=>{
       casename =  localStorage.getItem('casename')
    });
  
</script>

<div>
    <div class="slot-wrapper">
        <slot />
    </div>
    <div>
        <Sidebar  />

    </div>
    <!-- <div class='sidebaarcdat text-red-600 h-[100vh]' >
        <h1 class="text-2xl font-bold text-red-600  text-center mt-2 ml-2 mr-2">Analysis</h1>
            <p class="text-right mr-3">- {casename}</p>
        <div class="mt-10 mx-3">
            <ul class="text-white">
                <li class="mb-2 p-2 hover:bg-gray-800 cursor-pointer transition duration-300">
                    <button  class="w-[100%] text-left" on:click={() => goto("/analysis/map")}> Map  </button>
                </li>
                <li class="mb-2 p-2 hover:bg-gray-800 cursor-pointer transition duration-300" >
                    <button class="w-[100%] text-left"  on:click={() => goto("/analyst/requests")}> Requests  </button>
                </li>
                <li class="mb-2 p-2 hover:bg-gray-800 cursor-pointer transition duration-300">
                    <button class="w-[100%] text-left"  on:click={() => goto("/analysis/cases")}> Cases  </button>

                </li>
                <li class="mb-2 p-2 hover:bg-gray-800 cursor-pointer transition duration-300">
                    <button class="w-[100%] text-left"  on:click={() => goto("/analyst/redflags")}> Redflags  </button>
                </li>
            </ul>
        </div>

    </div> -->
</div>

<style>
.slot-wrapper {
    position: absolute;
    margin: 1em 2em;
    /* transform: translate3d(20em, 0, 0); */
    width: calc(100% - 7em);
    /* transition: transform .45s cubic-bezier(0.77, 0, 0.175, 1); */
    z-index: 1;

}

</style>