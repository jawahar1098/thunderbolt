<script>
    export let rows = 3;
    export let label = '';
    export let value;
    export let placeholder;
    

    const handleInput = (event) => {
    value = event.target.value;
  };
  
  </script>
  <div class="row mb-3">

  
    <!-- svelte-ignore a11y-label-has-associated-control -->
    <label class="col-sm-3 col-form-label">
      {label} 
    </label>
  <textarea class="col-sm-4"  rows={rows} value={value} placeholder={placeholder} on:input={handleInput}></textarea>
  
</div>

<style>
    textarea {
        border: none;
        border-radius: 4px;
    }
</style>