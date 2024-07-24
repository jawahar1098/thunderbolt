<script>
    export let selectedState;
    export let label;
    const indianStates = [
      { name: "Andhra Pradesh" },
      { name: "Arunachal Pradesh" },
      { name: "Assam" },
      { name: " Bihar"},
      { name: "Chhattisgarh"},
      { name: "Goa"},
      { name: "Gujarat"},
      { name: "Haryana"},
      { name: "Himachal Pradesh"},
      { name: "Jammu and Kashmir"},
      { name: "Jharkhand"},
      { name: "Karnataka"},
      { name: " Kerala"},
      { name: "Madhya Pradesh"},
      { name: "Maharashtra"},
      { name: "Manipur"},
      { name: "Meghalaya"},
      { name: "Mizoram"},
      { name: "Nagaland"},
      { name: "Odisha"},
      { name: "Punjab"},
      { name: "Rajasthan"},
      { name: "Sikkim"},
      { name: "Tamil Nadu"},
      { name: "Telangana"},
      { name: "Tripura"},
      { name: "Uttar Pradesh"},
      { name: "West Bengal"}
    ];
  </script>
  <div class="row mb-3">
   <!-- svelte-ignore a11y-label-has-associated-control -->
   <label class="col-sm-3 col-form-label">
    {label} </label>
  
  <select  class="col-sm-5" bind:value={selectedState}>
    <option value="">-- Select a state --</option>
    {#each indianStates as state}
      <option value={state}>{state.name}</option>
    {/each}
  </select>
</div>
  