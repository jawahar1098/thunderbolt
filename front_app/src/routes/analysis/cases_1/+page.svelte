<script>
    // select case while analysis button will come
let activeButton = 'assigned';

function toggleActive(button) {
    activeButton = button;
}

// drop-down menu
let selectedCase = '';
let showAnalysisButton = false;
let chooseFileoption = false;

function 
handleCaseSelection(event) {
    selectedCase = event.target.value;
    showAnalysisButton = true;
}

function analyzeCase() {
    // You can write the analysis logic here
    console.log('Analyzing case:', selectedCase);
}

// choose option will visible after clicking td row
let showFileOption = false;

function toggleFileInput() {
  showFileOption = !showFileOption;
}

// Handle file selection
function handleFileChange(event) {
        const selectedFiles = event.target.files;
        // Do something with the selected files
        console.log(selectedFiles);
    }

    // second oen-case drop and choose button
 let choosefile = false;
    
    function choose(event) {
        choosefile = event.target.value !== ""; // Check if selected option is not empty
    }

</script>

<main>
    
    <div class="container">
        <button class="btn_cases {activeButton === 'assigned' ? 'active' : ''}" on:click={() => toggleActive('assigned')}> ASSIGNED CASES </button>
        <button class="btn_cases {activeButton === 'own' ? 'active' : ''}" on:click={() => toggleActive('own')}> OWN CASES </button>
        <span class="highlight"></span>
    </div>
    
    <div class="main_container" style="display: {activeButton === 'assigned' ? 'block' : 'none'};">
        <div class="container_1">
            <h2>Select any cases :</h2>

            <select class="dropdown" on:change={handleCaseSelection}>
                <option value="">Select the case</option>
                <option>797845762</option>
                <option>1234567890</option>
                <option>568741239</option>
            </select>
            {#if showAnalysisButton}
                <button class="analysis" on:click={analyzeCase}>Analysis</button>
            {/if}
        </div>

        {#if showAnalysisButton}
            <div class="requesttype">
                <h4>Requesttype :<span>  </span></h4>
               
            </div>        
        {/if}
    
        <table class="styled-table">
            <thead>
            <tr>
                <th>Phone Number</th>
                <th>From Date</th>
                <th>To Date</th>
                <th>Data Status</th>
            </tr>
            </thead>
            <tbody>
            <tr on:click={toggleFileInput}>
                <td>111111111111</td>
                <td>12/06/2024</td>
                <td>12/06/2024</td>
                <td>nodata</td>
            </tr>
            <tr on:click={toggleFileInput}>
                <td>589452</td>
                <td>14/02/2024</td>
                <td>10/01/2024</td>
                <td>datareceived</td>
            </tr>
            <tr on:click={toggleFileInput}>
                <td>5684</td>
                <td>02/01/2024</td>
                <td>08/08/2024</td>
                <td>nodata</td>
            </tr>
            </tbody>
        </table>
        
        <!-- {#if showFileOption} -->
        {#if showAnalysisButton}
        <div class="fileoption">
            <input type="file" id="fileInput" multiple on:change={handleFileChange} />
            <button class="save_files">Upload</button>
        </div>
        {/if}
    </div>

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
<!-- another button div starts from here -->
<!-- icons -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.12.1/css/all.min.css" integrity="sha256-mmgLkCYLUQbXn0B1SRqzHar6dCnv9oZFPEC1g1cwlkk=" crossorigin="anonymous" />

    {#if activeButton === 'own'}
    <div class="main_container_2">
        <!-- model to add a new case -->
        <div class="inside_part">
            <h2>Select any cases :</h2>
            <select class="dropdown" on:change={choose}>
                <option value="">Select the case</option>
                <option>797845762</option>
                <option>1234567890</option>
                <option>568741239</option>
            </select>

            {#if choosefile}
            <div class="fileoption_1">
                <input type="file" id="fileInput" multiple on:change={handleFileChange} style="margin-left: 20px;" />
                <button class="save_files" style="margin-right: 100px;">Upload</button>
            </div>
            {/if}

            <button type="button" class="btn btn-primary save_files" data-toggle="modal" data-target="#exampleModalCenter">
                +Add a New Case
            </button>
        </div>

        <div class="modal fade" id="exampleModalCenter" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLongTitle">Add New Case</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <p class="model_class">Case Name :</p>
                <input type="text" placeholder="Enter case name" style="width: 60%;">

                <p class="model_class">File Type :</p>
                <select class="dropdown" style= "width: 60%; margin-left:15px" >
                    <option value="">Select the case</option>
                    <option>Tower CDR</option>
                </select>
                
                <p class="model_class">Upload File :</p>
                <input type="file" id="fileInput" multiple on:change={handleFileChange} />
                
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary">Save </button>
            </div>
            </div>
        </div>
        </div>

       
        {#if choosefile}
        <div class="table_container">
            <table>
                <tbody>
                    <tr>
                        <th>Number of Phone Numbers</th>
                        <td>12</td>
                    </tr>
                    <tr>
                        <th>Number of IMEIS</th>
                        <td>120</td>
                    </tr>
                    <tr>
                        <th>Number of Other Numbers</th>
                        <td>48</td>
                    </tr>
                    <tr>
                        <th>Under Tower Phones</th>
                        <td>12</td>
                    </tr>
                    <tr>
                        <th>Silent Period Phone Numbers</th>
                        <td>120</td>
                    </tr>
                    <tr>
                        <th>Phone Numbers that are not having NIL Duration</th>
                        <td>48</td>
                    </tr>
                    <tr>
                        <th>Under Tower IMEIS with different Phones</th>
                        <td>12</td>
                    </tr>
                    <tr>
                        <th>Number of phones in CDAT</th>
                        <td>120</td>
                    </tr>
                    <tr>
                        <th>Number of IMEIS from CDAT</th>
                        <td>48</td>
                    </tr>
                    <tr>
                        <th>Number of New Phone Numbers from IMEIS of CDAT</th>
                        <td>12</td>
                    </tr>
                    <tr>
                        <th>Number of others in CDAT as Phone</th>
                        <td>120</td>
                    </tr>
                    <tr>
                        <th>Number of Phones as others in CDAT</th>
                        <td>48</td>
                    </tr>
                    <tr>
                        <th>Number of Phones as Phones in CDAT</th>
                        <td>48</td>
                    </tr>
                    <tr>
                        <th>LI Number Present</th>
                        <td>48</td>
                    </tr>
                </tbody>
            </table>
        </div>
        {/if}   

        <!-- <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"> -->
        <!-- <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script> -->
        <!-- <div class="progress">
            <div class="progress-bar" style="width:40%;"></div>
          </div> -->
        <div class="list_features">
            <section>
                <input type="radio" name="styles" id="default" checked>
                <label for="default">default native appearance</label>
            </section>
            <section>
                <input type="radio" name="styles" id="accent">
                <label for="accent">accent-color</label>
                <small>(widely supported >= 2021, limited possibilities)</small>
            </section>
        </div>
    </div>
    
{/if}
</main>
<style>
    small {
    font-size: 11px;
    color: #555;
    margin-left: 1rem;
}
    section {
    display: flex;
    align-items: center;
    margin-top: 1rem;
}

input,
label {
    cursor: pointer;
}

label,
small {
    margin-top: 0.1em;
}

input[type="radio"] {
    height: 1.2rem;
    width: 1.2rem;
    margin-right: 0.5rem;
}

#accent {
    accent-color: var(--checked-color);
}

.custom-radio {
    /* hiding browser el */
    appearance: none;
    /* Safari support */
    -webkit-appearance: none;
    border: 0.2rem solid #fff;
    background-color: var(--bg-color);
    border-radius: 50%;
}

/* keyboard navigation focus appearance */
.custom-radio:focus-visible {
    outline-offset: 0;
}

#box-shadow {
    box-shadow: 0 0 0 1px var(--color);
}

#box-shadow:hover {
    border-width: 0;
}

#box-shadow:checked {
    box-shadow: 0 0 0 1px var(--checked-color);
    background-color: var(--checked-color);
    border-width: 0.2rem;
}

#outline {
    outline: 1px solid var(--color);
}

#outline:hover {
    outline-color: var(--checked-color);
}

#outline:checked {
    outline-color: var(--checked-color);
    background-color: var(--checked-color);

    animation: outline-checked;
    animation-duration: 0.1s;
    animation-iteration-count: 4;
    animation-direction: alternate;
    animation-timing-function: linear;
}

@keyframes outline-checked {
    0% {
        outline-offset: 0;
    }

    100% {
        outline-offset: -0.2rem;
    }
}


    /* .progress {
        display: flex;
        height:10px;
        width:100px;
        margin-left: 90%;
        margin-top: -10%;
    } */
    .list_features {
        display: absolute;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        margin-top: -32%;
        margin-left: 50%;

    }


    .table_container {
        display: flex;
        /* margin-left: -50px; */
    }
    .table_container {
        margin-top: 20px;
        display: flex;
        /* justify-content: center; */
    }

    table {
        width: 40%;
        border-collapse: collapse;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }

    th, td {
        padding: 8px 15px;
        border-bottom: 1px solid #dddddd;
        text-align: center;
    }

    th {
        background-color: #585c5b;
        color: #ffffff;
        font-weight: bold;
    }

    tr:nth-child(even) td {
        background-color: #e0e2e2;
    }
    tr:nth-child(odd) td {
        background-color: #eceeee;
    }


    
    .fileoption {
    position: fixed;
    top: 110px; /* Adjust the top position as needed */
    left: 67%; /* Center horizontally */
    transform: translateX(-50%); /* Center horizontally */
    height: 40px;
    cursor: pointer;
    width: 25%;
}
    .save_files{
        border: none;
        border-radius: 4px;
        background-color: #525252; 
        color: #fff;
        font-size: 16px;
        cursor: pointer;
        padding: 0 10px; 
        height: 40px;
    }

    .save_files:hover {
    background-color: #808181; 
}
       
    /* Container Styles */
    .container_1 {
        margin-left: 100px;
        margin-top: 30px;
        width: 85%;
        display: flex;
    }
    .container {
        margin-left: 250px;
        margin-top: 30px;
        width: 85%;
        display: flex;
    }
    .requesttype {
        /* box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); */
        /* background-color: #007a6c; */
        position: fixed;
        margin-left: 38%;
        margin-top: -40px;
        color: #5c70be;
        display: flex;
    }

    /* Button Styles */
    .btn_cases {
        height: 40px;
        width: 40%;
        transform: skew(-30deg);
        font-weight: bold;
        margin-right: 10px;
        border: none;
        /* background-color: rgb(200, 125, 213); */
        background-color: #555;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
    }

    .btn_cases.active {
        background: linear-gradient(to right, rgb(65, 105, 225), rgb(224, 159, 135));
    }

    .btn_cases:hover {
        background: linear-gradient(to right, rgb(193, 194, 197), rgb(45, 44, 43));
    }

    /* .btn_cases:active {
        background: linear-gradient(to right, rgb(155, 233, 155), rgb(129, 61, 141));
    } */



    /* H2 Styles */
    h2 {
        margin-right: 10px;
        margin-top: 5px;
        color: rgb(89, 123, 174); /* Teal color for the header */
    }
    /* Table Styles */
    .styled-table {
        width: 90%;
        margin-left: 100px;
        border-collapse: collapse;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        background-color: #f3f3f3;
    }

    .styled-table th, .styled-table td {
        padding: 10px;
        text-align: left;
        text-align: center;
        width: 10px;
    }
    .styled-table td {
        cursor: pointer;
    }
   
    .styled-table thead {
        background-color: #009879;
        color: white;
    }

    .styled-table tbody tr:nth-of-type(odd) {
        background-color: #ffffff;
    }

    .styled-table tbody tr:nth-of-type(even) {
        background-color: #f9f9f9;
    }
    .styled-table tbody tr:hover {
    background-color: rgb(189, 202, 213);
  }
  

    /* Dropdown Styles */
.dropdown:focus {
    outline: none;
    border-color: #343535;
}

.dropdown {
    height: 40px;
    width: 200px; 
    margin-right: 10px; 
    border: 1px solid #4b4c4c; 
    border-radius: 4px;
    background-color: #fff; 
    font-size: 16px;
    padding: 5px;
    color: #555; 
}

.analysis {
    height: 40px;
    padding: 0 20px; 
    border: none;
    border-radius: 4px;
    background-color: #525252; 
    color: #fff; 
    font-size: 16px;
    cursor: pointer;
    margin-left: 56%;
}

.analysis:hover {
    background-color: #808181; 
}


/* new container for the button */

.main_container_2 {
        /* display: flex; */
        margin-top: 30px;
        margin-left: 12%;
        align-items: center;
        /* box-shadow: 0 0 20px rgba(0, 0, 0, 0.15); */

    }

    .main_container_2 p {
        margin-right: 10px; 
        color: #2b4943; 
        font-weight: bold;
    }  

    .main_container_2 input[type="text"] {
        padding: 8px;
        border-radius: 5px;
        /* border: 1px solid #009879;  */
        outline: none; 
        transition: border-color 0.3s ease;
    }

    .main_container_2 input[type="text"]:focus {
        border-color: #009879; 
    }

    .main_container_2 button {
        padding: 8px 15px;
        border: none;
        /* background-color: #009879;  */
        color: white;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease; 
    }
    .button:hover {
        background-color: #007a6c; 
    }
   
    .model_class {
        display: inline-block;
    }
  
    .modal-content {
        border-radius: 10px;
    }

    .modal-header {
        background-color: #4f9fe0;
        color: white;
        border-bottom: none;
        border-radius: 10px 10px 0 0;
    }

    .modal-title {
        font-weight: bold;
    }

    .modal-body {
        padding: 20px;
    }

    .modal-footer {
        border-top: none;
        padding: 20px;
        justify-content: center;
    }

    .btn-primary:hover {
        background-color: #007a6c;
    }
    .inside_part {
        display: flex;
        /* box-shadow: 0 0 20px rgba(0, 0, 0, 0.15); */

    }
    
</style>


  