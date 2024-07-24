<script>
    import Sidebar from "$lib/sidebar/Sidebar.svelte";



    
</script>
<main style="position: fixed; width: 100%; height: 100vh; background:rgb(243, 247, 247)">
    <div>
        <slot />
    </div>
</main>
<div>
    <Sidebar />
</div>
