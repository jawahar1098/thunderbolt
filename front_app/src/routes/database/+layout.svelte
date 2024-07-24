<script>
    import Sidebar from "$lib/sidebar/Sidebar.svelte";



    
</script>
<main>
    <div>
        <slot />
    </div>

    <div>
        <Sidebar />

    </div>
</main>

<style>
    .slot-wrapper {
    position: absolute;
    margin: 1em -12em;
    transform: translate3d(20em, 0, 0);
    width: calc(100% - 40em);
    transition: transform .45s cubic-bezier(0.77, 0, 0.175, 1);
    z-index: 1; /* Set a lower z-index value */

}

</style>