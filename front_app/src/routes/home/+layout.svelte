<script>
    import Sidebar from "$lib/sidebar/Sidebar.svelte";

    let currenttab = 'home'

</script>


<main>
    <div class="slot-wrapper">
        <slot />
    </div>
   
    <div>
        <Sidebar/>
    </div>
    
</main>


<style>
.slot-wrapper {
    position: absolute;
    margin: 1em 0;
    transform: translate3d(0, 0, 0);
    width: calc(100% - 70em);
    transition: transform .45s cubic-bezier(0.77, 0, 0.175, 1);
    z-index: 1; /* Set a lower z-index value */

}

</style>