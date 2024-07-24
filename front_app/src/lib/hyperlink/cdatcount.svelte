<script>
    // @ts-nocheck

    let number;
    let showProgress = false;
    let gotResult = false;
    let datafound = "no data yet";
    let data = {};
    
    
    // const url = `${basepath()}/hyperlink`
    // postRequest(fetch,url,call_in)
    
    async function cdat_contacts(number,mode) {
        gotResult = false
        const cdat_contacts = new FormData();
        cdat_contacts.append("number", number);
        cdat_contacts.append("mode", mode);
        showProgress = true
        
        // try {
        //   const response = await fetch(
        //     `http://${window.location.hostname}:5005/profile_num`,
        //     {
        //       method: "POST",
        //       body: cdat_contacts,
        //     }
        //   );
        
        const url = `${basepath()}/profile_num`
        postRequest(fetch,url,cdat_contacts)
        
        .then(data => {


            if (data.data_dict === 'Not data Matched'){
              showProgress = false
              datafound = "No Data Matched In Database"
            }else{
              otherStates = data.data_dict[0]['other_states']
              gotResult=true
            }
        } )
    }
    
    
    
    
    </script>
    
    <div class="input-container shadow p-2 mt-4 border-top">
        <form>
            <label  class=" mx-5 font-bold" for="mobileNumber">Enter Number</label>
            <input class="input input-bordered w-50 md:w-auto s-hRLDX_Gekubi border-amber-700" id="mobileNumber"  type="text" placeholder=" Enter a value" size="10" bind:value={number}/>
            <button class="btn btn-success" type="submit" on:click={cdat_contacts}>Submit</button>
        </form>
    </div>
    <div class="relatieve h-[100vh] w-[100vw]">
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
                            <th scope="col"  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[200px]">CAT
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
                            <th scope="col"  class="border-r border-b px-4 py-2 text-base-100 dark:border-neutral-500 w-[200px]">IO NAME
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {#each data.data_dict as item}
                        <tr class="border-b hover:bg-gray-100 dark:border-neutral-500">
                            <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['source_number']}</td>
                            <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['destination_number']}</td>
                            <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['nickname']}</td>
                            <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['cat']}</td>
                            <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['call_in']}</td>
                            <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['call_out']}</td>
                            <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['duration']}</td>
                            <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['first_call_timestamp']}</td>
                            <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['last_call_timestamp']}</td>
                            <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['address']}</td>
                            <td class="border-r px-4 py-2  font-medium text-ellipsis dark:border-neutral-500">{tblD['io_name']}</td>
                        </tr>
                        {/each}
                    </tbody>
                </table>
            </div>
        </div>
        {:else if showProgress}
        <div class="w-25 flex justify-center mt-20">
          
          <div class="absolute top-[50%] left-[50%] p-10">
            <span class="loading loading-spinner loading-lg"></span>
          </div>
        </div>
        {:else}
        <div class="w-25 flex justify-center mt-20">
          <span>{datafound}</span>
        </div>
      {/if}
    </div>  