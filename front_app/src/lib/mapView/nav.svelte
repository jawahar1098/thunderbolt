<script>
    import Cell from "./cell.svelte";
    import Main from "./main.svelte";
    import Common from "./common_link.svelte";

    export let menu = 1;
</script>
<main class="nav">
    <a  on:click|preventDefault={() => (menu = 1)}>Tower</a>
    <a on:click|preventDefault={() => (menu = 2)}>Time Track</a>
    <a  on:click|preventDefault={() => (menu = 3)}>Common Link</a>
    
</main>
{#if menu === 1}
<Main />
{:else if menu === 2}
<Cell />
{:else if menu === 3}
<Common />
{:else}
<h1>Page Not Found</h1>
{/if}

<style>
    .nav{
        /* background-color: rgb(207, 199, 146); */
        background: rgb(2,0,36);
        background: linear-gradient(90deg, rgba(2,0,36,1) 0%, rgba(9,104,121,1) 78%, rgba(0,212,255,1) 100%);  
        color: white;
        padding: 10px;
        display: flex;
        gap: 10px;
    }
    a{
        color: white;
    }
</style>