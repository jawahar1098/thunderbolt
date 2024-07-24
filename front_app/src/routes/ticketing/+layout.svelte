<script>
// @ts-nocheck

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
margin-left: 3.5%;
/* border: 4px solid #000000;  */
  /* box-sizing: border-box; */
  height: 100%;
  background-color: aliceblue;
}
</style>