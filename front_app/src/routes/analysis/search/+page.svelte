<script context="module">
    import Automation from "$lib/database/Automation.svelte";
    import Directfiles from "$lib/database/Directfiles.svelte";
    import Towerdata from "$lib/towercdr/Towerdata.svelte";
  
    export const navOptions = [
      { page: "Search", component: Towerdata },
      { page: "Map", component: Automation },
      { page: "Tower Analysis", component: Directfiles },
    ];
  </script>
  
  <script>
    let selected = navOptions[0];
    let intSelected = 0;
  
    function changeComponent(event) {
      selected = navOptions[event.srcElement.id];
      intSelected = event.srcElement.id;
    }
  </script>
  
  <main>
    <div class="container-fluid">
      <ul class="nav nav-tabs">
        {#each navOptions as option, i}
          <li class="nav-item">
            <button
              class={intSelected == i
                ? "nav-link active p-2 ml-1"
                : "p-2 ml-1 nav-link"}
              on:click={changeComponent}
              id={i}
              role="tab">{option.page}</button
            >
          </li>
        {/each}
      </ul>
      <div class="row">
        <div class="col-sm-12">
          <div class="p-2">
            <svelte:component this={selected.component} />
          </div>
        </div>
      </div>
    </div>
  </main>
  
  <style>
    main {
      margin-left: 5%;
      margin-top: 65px;
    }
    .nav-link.active {
      color: #167ee6 !important;
      border: none !important;
      border-bottom: 2px solid #1266f1 !important;
    }
    .nav-item:focus-visible {
      outline: none !important;
    }
    button {
      width: 30vw;
    }
    .col-sm-12 {
      padding: 1rem !important;
    }
  </style>
  