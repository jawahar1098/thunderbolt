<!-- InputField.svelte -->
<script>
  export let label = '';
  export let type = 'text';
  export let placeholder;
  export let value;

  const handleInput = (event) => {
    value = event.target.value;
  };

  
</script>

<div class="row mb-3">
  <!-- svelte-ignore a11y-label-has-associated-control -->
  <label class="col-sm-3 col-form-label">{label}</label>
  <input class="col-sm-4" type={type} placeholder={placeholder} value={value} on:input={handleInput}/>
</div>
<style>
    input {
        border: none;
        border-radius: 5px;
    }
</style>

