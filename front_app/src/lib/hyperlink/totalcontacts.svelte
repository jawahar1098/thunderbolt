<script>
  // @ts-nocheck

    import { onMount } from "svelte";
    import { basepath } from "$lib/config";
   let data = {};
   let showProgress = false;
   let gotResult = false;
   let parammode;
   let showTablePage = false;
   let dest_num;
   let bottomRightHomeContentHeading = false;
   let datafound = "no data yet";
   let urlParamValue;
   let state;
   let dest_count;
   let imei_num;
   


    onMount(() => {
    const params = new URLSearchParams(window.location.search);
    urlParamValue = params.get('value') || '';
    parammode = params.get('mode') || 'undefined';
    dest_num = params.get('dest_number' || '')
    urlParamValue = urlParamValue
    state = params.get('states' || '')
    dest_count = params.get('dest_count' || '')
    imei_num = params.get('imei_num') || '';
    console.log(urlParamValue,parammode)
    hyperlink_route(urlParamValue,dest_num,parammode,imei_num)
    });
    async function hyperlink_route(number,dest_num,mode,imei_num) {
    const profile_num = new FormData();
    profile_num.append("number", number);
    profile_num.append("mode", mode);
    profile_num.append('dest_num',dest_num)
    profile_num.append('imei_num',imei_num)
    profile_num.append('state',state)
    profile_num.append('dest_count',dest_count)
    if (number){
      showProgress = true

    }

    try {
      const response = await fetch(
        `http://${window.location.hostname}:5005/hyperlink`,
        {
          method: "POST",
          body: profile_num,
        }
      );

      if (response.ok) {
        data = await response.json();
        console.log(data)
        if (data.data_dict === 'Not data Matched'){
          showProgress = false
          datafound = "No Data Matched In Database"
        }
        else{

          bottomRightHomeContentHeading = ""
          gotResult=true
        }
      } else {
        console.error("Failed to submit form",response);
      }
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  }

  async function total_contacts(){
    gotResult = false
    const  total_contacts= new FormData();
    total_contacts.append("number", number);
    total_contacts.append("mode", "total_contacts");
    showProgress = true
    try {
            const response = await fetch(
            `http://${window.location.hostname}:5005/total_contacts`,
            {
            method: "POST",
            body: total_contacts,
            }
        );
        

        if (response.ok) {
            data = await response.json();
            console.log(data)
            if (data.data_dict === 'Not data Matched'){
            showProgress = false
            datafound = "No Data Matched In Database"
            }else{
            otherStates = data.data_dict[0]['other_states']
            gotResult=true
            }
        } else {
            console.error("Failed to submit form",response);
          }
        } catch (error) {
          console.error("Error submitting form:", error);
        }
  }
</script>

{#if gotResult}
<div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between w-full px-5">
    <div class="flex flex-col p-2 h-[80vh] overflow-hidden">
      <table class="table-fixed border text-center text-sm font-light dark:border-neutral-500">
        <thead class="font-medium bg-base-content dark:border-neutral-500">
          <tr>
            <th scope="col"  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[200px]">SOURCE NUMBER
            </th>
            <th scope="col"  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[200px]">DESTINATION NUMBER
            </th>
            <th scope="col"  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[200px]">NICKNAME
            </th>
            <th scope="col"  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[200px]">CALL IN
            </th>
            <th scope="col"  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[200px]">CALL OUT
            </th>
            <th scope="col"  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[200px]">TOTAL CALLS
            </th>
            <th scope="col"  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[200px]">DURATION
            </th>
            <th scope="col"  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[200px]">FIRST CALL
            </th>
            <th scope="col"  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[200px]">LAST CALL
            </th>
            <th scope="col"  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[200px]">ADDRESS
            </th>
          </tr>
        </thead>
        <tbody>
         {#each data.data_dict as item}
         <tr class="border-b hover:bg-gray-100 dark:border-neutral-500">
            {#each data.headers as header}
            {#if parammode === "total_contacts" || parammode === "dest_num" ||parammode === "dest_count" || parammode === "cellidsearch"  || bottomRightHomeContentHeading === "cellIdSearch" || bottomRightHomeContentHeading ==='cdatContacts' || bottomRightHomeContentHeading === 'profile'|| parammode === "other_states" ||  bottomRightHomeContentHeading ==='imeiSearch' || bottomRightHomeContentHeading === 'summary_new' }
            {#if header === "call_count"}
            <td class="border-r px-6 py-4 font-medium text-ellipsis dark:border-neutral-500 capitalize text-rose-600"><a href="/home?value={number}&mode=total_calls" target="_blank">{item[header]}</a></td>
            {:else if header === "call_in" || header === "call_out" || header === "total_calls"}
          
            <td class="border-r px-6 py-4 font-medium text-ellipsis dark:border-neutral-500 text-rose-600"><a href="/home?value={number}&mode={header}&dest_number={item["destination_number"]}" target="_blank">{item[header]}</a></td>
            {:else if header === "destination_number"}
            <td class="border-r px-6 py-4 font-medium text-ellipsis dark:border-neutral-500 text-rose-600"><a href="/home?value={item[header]}&mode=dest_num" target="_blank">{item[header]}</a></td>
            {:else if header === "cellid"}
            <td class="border-r px-6 py-4 font-medium text-ellipsis dark:border-neutral-500 text-rose-600"><a href="/home?value={item[header]}&mode=cellidsearch" target="_blank">{item[header]}</a></td>
            {:else if header === "imei"}
            <td class="border-r px-6 py-4 font-medium text-ellipsis dark:border-neutral-500 text-rose-600"><a href="/home?value={number}&mode=imei&imei_num={item[header]}" target="_blank">{item[header].length}</a></td>
            {:else if header === "total_contacts"}
            <td class="border-r px-6 py-4 font-medium text-ellipsis dark:border-neutral-500 text-rose-600"><a href="/home?value={number}&mode=total_contacts&dest_number={item[header]}" target="_blank">{item[header].length}</a></td>
            {:else if header === "cdat_count"}
            <td class="border-r px-6 py-4 font-medium text-ellipsis dark:border-neutral-500 text-rose-600"><a href="/home?value={number}&mode=cdat_count" target="_blank">{item[header].length}</a></td>
            {:else if header === "other_states"}
            <td class="border-r px-6 py-4 font-medium text-ellipsis dark:border-neutral-500 text-rose-600"><a href="/home?value={number}&mode=other_states&states={item[header]}" target="_blank">{item[header].length}</a></td>
            {:else if header === "dest_count"}
            <td class="border-r px-6 py-4 font-medium text-ellipsis dark:border-neutral-500 text-rose-600"><a href="/home?value={number}&mode=dest_count&dest_count={item[header]}" target="_blank">{item[header].length}</a></td>
                  
            <!-- {/if} -->
        
            {:else}
            <td class="border-r px-6 py-4 font-medium text-ellipsis dark:border-neutral-500">{item[header]}</td>
            {/if}
            
            {:else if parammode === "imei" || parammode === 'call_out' || parammode === 'cdat_count' || parammode === 'call_in' || parammode === 'total_calls'}
              {#if header === null}
              <td class="border-r px-6 py-4 font-medium text-ellipsis dark:border-neutral-500 text-rose-600"></td>
              {:else if header === "cdat_count" || header === "call_in" || header === "call_out" || header === "total_calls"}
              <td class="border-r px-6 py-4 font-medium text-ellipsis dark:border-neutral-500 text-rose-600"><a href="/home?value={item['source_number']}&mode={header}&dest_number={item["destination_number"]}&imei_num={item['imei']}" target="_blank">{item[header]}</a></td>
              {:else if header === "imei"  }
              <td class="border-r px-6 py-4 font-medium text-ellipsis dark:border-neutral-500 text-rose-600">
                <a href="/home?value={number}&mode=imei&imei_num={item[header]}" target="_blank">{item[header]}</a></td>
                {:else if header === "destination_number" }
              <td class="border-r px-6 py-4 font-medium text-ellipsis dark:border-neutral-500 text-rose-600">
                <a href="/home?value={item[header]}&mode=dest_num" target="_blank">{item[header]}</a></td>
            {:else}
            <td class="border-r px-6 py-4 font-medium text-ellipsis dark:border-neutral-500">{item[header]}</td>
            {/if}
                {/if}
             {/each}
             <!-- <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['source_number']}</td>
             <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['destination_number']}</td>
             <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['nickname']}</td>
             <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['call_in']}</td>
             <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['call_out']}</td>
             <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['total_calls']}</td>
             <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['duration']}</td>
             <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['first_call']}</td>
             <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['last_call']}</td>
             <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['address']}</td> -->
            </tr>
            {/each}
        </tbody>
      </table>
      <div class="w-25 flex justify-center mt-20">
        <span>{datafound}</span>
      </div>
    </div>
  </div>
  {/if}
