
<script>
    import { onMount } from 'svelte';
    import * as XLSX from "xlsx";
    import { basepath } from "$lib/config";
  
  // export let key_location;
  // export let sitename;
  // export let startDate;
  // export let endDate ;
  export let selectedValues;
  let data = [];
  let final_result = [];
  let mode ;
  let gotResult = false;
  let response = ['common_towers', 'common_numbers'];
  
  
  function handleSubmit() {
    gotResult = false;
    console.log(selectedValues)
    const same_tower = new FormData();
    
    // Determine which input to use based on user's choice
      same_tower.append("value", selectedValues);
      // same_tower.append("sitename", sitename);
      // same_tower.append("fromdate", startDate);
      // same_tower.append("todate", endDate);
      same_tower.append("mode", "overview");
      console.log(same_tower)
  
    fetch(`${basepath()}/tower_analysis_2`, {
      method: "POST",
      body: JSON.stringify({'value':selectedValues,'mode':'overview'}),
    })
    .then((res) =>  res.json())
    .then(data => {
      final_result = data
      console.log(final_result);
      gotResult = true;
    })
    .catch((err) => {
      console.error("Fetch error:", err);
    });
  }
  
  function downloadData(data) {
    const wb = XLSX.utils.book_new();
    const dataArray = data.map(item => {
      return {
        "COMMON TOWERS": item._id.join(', '),
        "COMMON NUMBERS": item.common_numbers.join(', ')
      };
    });
    const ws = XLSX.utils.json_to_sheet(dataArray);
    XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
    const excelData = XLSX.write(wb, { bookType: "xlsx", type: "binary" });
    const blob = new Blob([s2ab(excelData)], { type: "application/octet-stream" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "data.xlsx";
    a.click();
  }
  function s2ab(s) {
    const buf = new ArrayBuffer(s.length);
    const view = new Uint8Array(buf);
    for (let i = 0; i < s.length; i++) {
      view[i] = s.charCodeAt(i) & 0xff;
    }
    return buf;
  }
  
  onMount(() =>{
     handleSubmit()
    
  })
  
  
  </script>
  
  
  
  <div class="table-container">
    {#if gotResult}
    <div class="custom-border">
      <table>
        <thead>
          <tr>
            {#each response as tblH}
              <th>
                {tblH.toUpperCase().replace(/_/g, " ")}
              </th>
            {/each}
          </tr>
        </thead>
  
  
        <tbody>
          {#each final_result as tblD}
          <tr>
            {#each Object.values(tblD) as column}
            <td class="border-r border-b px-6 py-4">
              {#if typeof column === 'object'} 
                {#each Object.values(column) as subColumn} 
                  {subColumn} ,
                {/each}
              {:else}
                {column}
              {/if}
            </td>
          {/each}
          </tr>
          {/each}
  
        </tbody>
        
      </table>
    </div>
  
    {/if}
  
  </div>
  
  
  <style>
  .input-container {
    display: flex;
    align-items: center;
    gap: 2px;
  }
  label {
    font-weight: bold; 
  }
  button {
    border: 2px solid;
  }
  .table-container {
    margin-top: 2%;
    margin-bottom: 2%;
    margin-left: 2%;
    margin-right: 2%;
    overflow-x: auto; 
    max-height: 700px;
    position: relative;
  }
  
  table {
    width: 100%;
    table-layout: fixed;
    border-color: black;
    text-align: center;
  }
  
  th, td {
    border: 1px solid black;
    padding: 8px;
    text-align: left;
    text-wrap: wrap;
    word-wrap: break-word;
    overflow-wrap:break-word;
    text-overflow: ellipsis;
    padding-top: 10px;
    padding-bottom: 20px;
    padding-left: 30px;
    padding-right: 40px;
  }
  
  th {
    background-color: #dddddd;
    text-align: center;
    position: sticky;
    top: 0;
    z-index: 1;
  }
  table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
  }
  
  </style>
  