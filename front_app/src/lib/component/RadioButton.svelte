<!-- <script>
    export let options =  ['A', 'B', 'C','D', 'UNKNOWN'];
    export let selectedOption = '';
    export let label = '';
  
    function handleOptionChange(event) {
      selectedOption = event.target.value;
    }
  </script>
  
 
  <label class="col-sm-3 col-form-label">
    {label} 
</label>
{#each options as option}
 
      <input  type="radio" name="radio-group" on:change={handleOptionChange} />
      {option}
  
  {/each} -->

  <script>
    // based on suggestions from:
    // Sami Keijonen https://webdesign.tutsplus.com/tutorials/how-to-make-custom-accessible-checkboxes-and-radio-buttons--cms-32074
    // and Inclusive Components by Heydon Pickering https://inclusive-components.design/toggle-button/
  
    export let required_options;
    export let userSelected = options[0].value;
    export let fontSize = 16;
    export let flexDirection = 'row'
    export let label;
    
    const uniqueID = Math.floor(Math.random() * 100)
  
    const slugify = (str = "") =>
      str.toLowerCase().replace(/ /g, "-").replace(/\./g, "");
  </script>
<div class="row mb-3">
  <label class="col-sm-3 col-form-label">
    {label} 
  
  </label>
  <div role="radiogroup" 
           class="group-container col-sm-3"
           aria-labelledby={`label-${uniqueID}`}
           style="font-size:{fontSize}px; flex-direction:{flexDirection}" 
           id={`group-${uniqueID}`}>
          <div class="legend" 
               id={`label-${uniqueID}`}>
          </div>
    {#each required_options as { value, label }}
      <input
        class="sr-only pl-5"
        type="radio"
        id={slugify(label)}
        bind:group={userSelected}
        value={value} />
      <label for={slugify(label)}> {label} </label>
    {/each}
  </div>
</div>
  
  <style>
        :root {
      --accent-color: CornflowerBlue;
      --gray: #ccc;
    }
    
     .group-container {
        border-radius: 2px;
        display: flex;
        flex-direction: row;
      }
  
    .legend {
      font-weight: bold;
    }
    label {
      user-select: none;
      line-height: 1.2em;
    }
  
    .sr-only {
      position: absolute;
      clip: rect(1px, 1px, 1px, 1px);
      padding: 0;
      border: 0;
      height: 1px;
      width: 1px;
      overflow: hidden;
    }
  
    input[type="radio"] {
      position: absolute;
    }
  
    input[type="radio"] + label {
      display: block;
      position: relative;
      text-align: left;
    }
  
    input[type="radio"] + label::before {
        content: "";
        position: relative;
        display: inline-block;
        margin-left: 0.5em;
        width: 1em;
        height: 1em;
        background: white;
        border: 1px solid var(--gray, #ccc);
        border-radius: 50%;
        top: 0.2em;
    }
  
    input[type="radio"]:checked + label::before {
      border: 1px solid var(--gray, #ccc);
      border-radius: 50%;
    }
  
    input[type="radio"] + label::after {
      content: "";
      position: absolute;
      display: inline-block;
      width: 0.5em;
      height: 0.5em;
      top: 0.45em;
      left: 0.8em;
      background: var(--accent-color, #282828);
      border: 1px solid var(--accent-color, #282828);
      border-radius: 50%;
      transform: scale(0);
    }
  
    input[type="radio"]:checked + label::after {
      opacity: 1;
      transform: scale(1);
    }
  
    input[type="radio"]:focus + label::before {
      box-shadow: 0 0 0 1px var(--accent-color, #282828);
      border-radius: 50%;
    }  
    
    input[type="radio"]:disabled + label {
      color: darken(var(--gray, #ccc), 10);
    }
  
    input[type="radio"]:disabled + label::before {
      background: var(--gray, #ccc);
    } 
    /* gravy */
  
  
    input[type="radio"] + label::before {
        transition: background 0.3s ease-out;
    }
  
    input[type="radio"]:checked + label::before {
      transition: background 0.3s ease-in;
    }
  
    input[type="radio"] + label::after {
      transition: transform 0.2s ease-out;
    }
  
    input[type="radio"]:checked + label::after {
      transition: transform 0.2s ease-in;
    }
  
    input[type="radio"]:focus + label::before {
      box-shadow: 0 0px 8px var(--accent-color, #282828);
      border-radius: 50%;
    }
  
  </style>
  