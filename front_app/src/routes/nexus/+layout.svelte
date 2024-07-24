<script>
    import Sidebar from "$lib/sidebar/Sidebar.svelte";

    
</script>

<div>
    <Sidebar  />

</div>
<div class="allinONE">
    <slot />

</div>

<style>
.allinONE{
margin-left: 3.2%;
margin-top: 2.8%;
/* border: 4px solid #000000;  */
  /* box-sizing: border-box; */
  height: 100%;
}
</style>