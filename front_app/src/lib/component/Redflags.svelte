<script>
    import { basepath } from "$lib/config";

let showpopup = false
let val = []

fetch(`${basepath()}/redflagidentifier`, {
    method: 'post',
    body : JSON.stringify({'username':"admin"})
})
.then(res => res.json())
.then(data => {
    console.log(data)
    val = data
    if(val.length > 0){

        showpopup = true
    }

})
</script>

<main>
    {#if showpopup}
    <div>
        <h1>We have a match in red flag 1</h1>
        <a href="/map" class="bg-red-600 border">View</a>
    </div>
    {/if}

    <div>
        <h2>Red flag</h2> 

    </div>
</main>