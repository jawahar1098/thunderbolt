<script>
    import { goto } from "$app/navigation";
    import { basepath } from "$lib/config";
    import { getRequest,postRequest } from "$lib/req_utils";

    getRequest(fetch,`${basepath()}/user`)
    .then(data => {console.log(data)
        if (data['authorized'] !== true){
            goto('/')
        }
    })

</script>

<main>
    <slot/>
</main>