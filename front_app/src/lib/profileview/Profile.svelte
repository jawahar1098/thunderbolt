<script>
        import Previewmodal from '$lib/modal/Previewmodal.svelte';
    import Numbersummary from '$lib/towercdr/Numbersummary.svelte';


    export let data;
    export let number;
    console.log(data,"---------")

    let summary_of_app = data.data_dict[0].ipdr_profile.summary_app;
    let summary_of_vpn = data.data_dict[0].ipdr_profile.summary_vpn;
    let summary_of_iptype = data.data_dict[0].ipdr_profile.summary_iptype;
    let summary_of_country = data.data_dict[0].ipdr_profile.summary_country;

    let mode;
    let show_modal = false;

    function renderdata(val){
        console.log(number,mode,"in profile")
        show_modal = true
        mode = val
    }

 
    

</script>
  


<style>

.tooltip {
  @apply invisible absolute;
}

.has-tooltip:hover .tooltip {
  @apply visible z-50;
}

</style>