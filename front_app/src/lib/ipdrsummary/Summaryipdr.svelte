<script>
// @ts-nocheck

 
 export let summary_of_app;
 export let summary_of_country;
 export let summary_of_iptype;
 export let summary_of_vpn;
//  console.log(summary_of_app,summary_country,summary_of_vpn,summary_of_iptype)

</script>

<div class="container">

    <h3 class="heading"><b>VPN Summary</b></h3>
    {#if summary_of_vpn && summary_of_vpn.total_unique_vpn_count}

    <p>Summary for this Number: <b>{summary_of_vpn.data}</b>. The Highest Count VPN, <b>{summary_of_vpn.highest_count_vpn.VPN}</b>, has a total destination IP count of <b>{summary_of_vpn.highest_count_vpn.total_destination_ips_count_of_vpn}</b>, and its destination IP is <b>{summary_of_vpn.highest_count_vpn_ip}</b>. The lowest count vpn, <b>{summary_of_vpn.lowest_count_vpn.VPN}</b>, has a total destination IP count of <b>{summary_of_vpn.lowest_count_vpn.total_destination_ips_count_of_vpn}</b> and it's destination IP is <b>{summary_of_vpn.lowest_count_vpn_ip}</b>. The total unique vpn count is <b>{summary_of_vpn.total_unique_vpn_count}</b>.</p><br>
    {:else}
    <p class="container">VPN Summary is not available.</p>
    {/if}


    <h3 class="heading"><b>App Summary</b></h3>
    {#if summary_of_app && summary_of_app.total_unique_app_count}

    <p>Summary for this Number: <b>{summary_of_app.data}</b>. The Highest Count App, <b>{summary_of_app.highest_count_app.APP}</b>, has a total destination IP count of <b>{summary_of_app.highest_count_app.total_destination_ips_count_of_app}</b>, and its destination IP is <b>{summary_of_app.highest_count_app_ip}</b>. The lowest count app, <b>{summary_of_app.lowest_count_app.APP}</b>, has a total destination IP count of <b>{summary_of_app.lowest_count_app.total_destination_ips_count_of_app}</b> and it's destination IP is <b>{summary_of_app.lowest_count_app_ip}</b>. The total unique app count is <b>{summary_of_app.total_unique_app_count}</b>.</p><br>
    {:else}
    <p class="container">App Summary is not available.</p>
    {/if}



    <h3 class="heading"><b>Country Summary</b></h3>
    {#if summary_of_country && summary_of_country.total_unique_country_count}

    <p>Summary for this Number: <b>{summary_of_country.data}</b>. The Highest Count Country, <b>{summary_of_country.highest_count_country.COUNTRY}</b>, has a total destination IP count of <b>{summary_of_country.highest_count_country.total_destination_ips_count_of_country}</b>, and its destination IP is <b>{summary_of_country.highest_count_country_ip}</b>. The lowest count country, <b>{summary_of_country.lowest_count_country.COUNTRY}</b>, has a total destination IP count of <b>{summary_of_country.lowest_count_country.total_destination_ips_count_of_country}</b> and it's destination IP is <b>{summary_of_country.lowest_count_country_ip}</b>. The total unique country count is <b>{summary_of_country.total_unique_country_count}</b>.</p><br>
    {:else}
    <p class="container">Country Summary is not available.</p>
    {/if}


    <h3 class="heading"><b>IP Type Summary</b></h3>
    {#if summary_of_iptype && summary_of_iptype.total_unique_iptype_count}
    <p>Summary for this Number: <b>{summary_of_iptype.data}</b>. The Highest Count IPType, <b>{summary_of_iptype.highest_count_iptype.IPTYPE}</b>, has a total destination IP count of <b>{summary_of_iptype.highest_count_iptype.total_destination_ips_count_of_iptype}</b>, and its destination IP is <b>{summary_of_iptype.highest_count_iptype_ip}</b>. The lowest count iptype, <b>{summary_of_iptype.lowest_count_iptype.IPTYPE}</b>, has a total destination IP count of <b>{summary_of_iptype.lowest_count_iptype.total_destination_ips_count_of_iptype}</b> and it's destination IP is <b>{summary_of_iptype.lowest_count_iptype_ip}</b>. The total unique iptype count is <b>{summary_of_iptype.total_unique_iptype_count}</b>.</p>
    {:else}
    <p class="container">IP Type Summary is not available.</p>
    {/if}


</div>

<style>
    .container {
        margin-top: 60px;
        margin-left: 50px;
    }
    .heading{
        color: #296b97;

    }
</style>