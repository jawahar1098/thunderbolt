<!-- <script>
    export let options;
    export let selectedOption = '';
    export let label;
    
    function handleOptionChange(event) {
      selectedOption = event.target.value;
    }
  </script>
  <div class="row mb-3">

  
  <label class="col-sm-3 col-form-label">
    {label} </label>
    <select class="col-sm-2" bind:value={selectedOption} on:change={handleOptionChange}>
      {#each options as option}
        <option value={option}>{option}</option>
      {/each}
    </select>
</div>

<style>
    select {
        border: none;
        border-radius: 4px;
        padding: 2px;
        

    }
</style>
 
   -->

   <script>
    export let options = [];
    export let display_func = a => a;
    export let index = 0;
    export let value;
    export let label;
    export let placeholder;

  
    $: {
      value = options[index];
      console.log(value);
    }
  </script>
  <div class="row mb-3">
    <!-- svelte-ignore a11y-label-has-associated-control -->
    <label class="col-sm-3 col-form-label">
      {label} 
    
    </label>

 
  
  
  <select class="col-sm-4" bind:value={index}>
    {#each options as option, i}
      <option value={i} placeholder={placeholder}>{display_func(option)}</option>
    {/each}
  </select>
</div>


  <style>
    select {
        border: none;
        border-radius: 8px !important;
        background-color: rgba(238, 238, 238, 0.486);
        border-bottom:2px solid black !important;
        box-shadow: 0 .5rem 1rem rgb(0, 0, 0)!important;    


    }
</style>