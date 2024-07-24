<script>
  // @ts-nocheck

  import { onMount, onDestroy } from "svelte";
  import Map from "ol/Map";
  import "ol/ol.css";
  import View from "ol/View";
  import { Tile as TileLayer, Vector as VectorLayer } from "ol/layer";
  import { OSM,XYZ, Vector as VectorSource } from "ol/source";
  import Feature from "ol/Feature";
  import { Point, Polygon } from "ol/geom";
  import { fromLonLat, toLonLat, transform } from "ol/proj";
  import {Style, Stroke, Fill, Icon, Text} from "ol/style";
  import { Draw, Modify, Select } from "ol/interaction";
  import { basepath } from "$lib/config";
  import Overlay from "ol/Overlay";
  import { writable, get } from "svelte/store";
  import GeoJSON from "ol/format/GeoJSON";
  import { goto } from "$app/navigation";
//   import Style from "ol/style/Style";
// import Stroke from "ol/style/Stroke";
  
  // Import GeoJSON data



  export const bookmarkedTowers = writable([]);
  export const fetchedData = writable([]);

  let mapContainer;
  let map;
  let vectorLayer;
  let circleLayer; // New vector layer for circles
  let drawInteraction;
  let modifyInteraction;
  let selectInteraction;
  let coordinates = [];
  let vectorSource;
  let circleSource = new VectorSource();
  let PolygonSource = new VectorSource();
  let cdrData = null;
  let selectedCdrData = null;
  let Polygons = [];
  let isDrawing = false;
  let showlatlong;
  let numbers = '';
  let userDetails = JSON.parse(localStorage.getItem('userDetails'))
  let tell_message= ""
  let showdetails;
  let showdata = false;
  let showfilters = true;
  let strangevalue = 10;
  let endrangevalue = 10
  let towerdata = []
  let markimg;
  let bookmarkImage;
  // let personlayer
  
  onMount(() => {


  const indianStatesGeoJSONPath = "/India_states.geojson";
  vectorSource = new VectorSource({
    format: new GeoJSON(),
    url: indianStatesGeoJSONPath,
  });

  const vectorLayer = new VectorLayer({
    source: vectorSource,
    style: function (feature) {
      const color = feature.get("color") || "#5c636a"; // Default to blue if no color is specified
      return new Style({
        stroke: new Stroke({
          color: color,
          width: 2,
        }),
      });
    },
  });
  // personlayer = new VectorLayer({
  //     source: circleSource,
  //     style: new Style({
  //       stroke: new Stroke({
  //         color: "red",
  //         width: 2,
  //       }),
  //       fill: new Fill({
  //         color: "rgba(255, 0, 0, 0.1)",
  //       }),
  //     }),
  //   });
    // Create a new vector layer for circles
    circleLayer = new VectorLayer({
      source: circleSource,
      style: new Style({
        stroke: new Stroke({
          color: "red",
          width: 2,
        }),
        fill: new Fill({
          color: "rgba(255, 0, 0, 0.1)",
        }),
      }),
    });

    PolygonSource = new VectorLayer({
      source: circleSource,
      style: new Style({
        stroke: new Stroke({
          color: "green",
          width: 1,
        }),
        fill: new Fill({
          color: "rgba(255, 0, 0, 0.1)",
        }),
      }),
    });



    // map = new Map({
    //   target: mapContainer,
    //   layers: [
    //     new TileLayer({
    //       source: new OSM({
    //         attributions: [],
    //       }),
    //     }),
    //     vectorLayer,
    //     PolygonSource,
    //     circleLayer, // Add the circle layer to the map
    //   ],
    //   view: new View({
    //     center: fromLonLat([77.4533, 21.8903]),
    //     zoom: 4.8,
    //   }),
    // });
    map = new Map({
    	target: mapContainer,
    	layers: [
    		new TileLayer({
    			source: new XYZ({
    				url: 'http://10.50.50.150:8082/tile/{z}/{x}/{y}.png'
    			}),
    		}),
    		vectorLayer,
    		circleLayer,
    	],
    	view: new View({
    		center: [0, 0],
    		zoom: 2
    	})
    });
    map.on("pointermove", function (event) {
      if (event.dragging) {
        return;
      }
      const coordinate = map.getEventCoordinate(event.originalEvent);
      const lonLat = coordinate
        ? transform(coordinate, "EPSG:3857", "EPSG:4326")
        : null;
      // console.log(lonLat);
      showlatlong = lonLat;
    });

   
    
   
  });

 
  

  function insertCommas() {
      numbers = ''
      var inputNumbersElement = document.getElementById("inputNumbers");
      var inputNumbersValue = inputNumbersElement.value.trim();

      // Remove any existing commas
      inputNumbersValue = inputNumbersValue.replace(/,/g, '');

      // Add commas after every 10th number
      var resultString = '';
      for (var i = 0; i < inputNumbersValue.length; i++) {

          resultString += inputNumbersValue[i];
          if ((i + 1) % 10 === 0 && i !== inputNumbersValue.length - 1) {
              resultString += ',';
          }
      }

      // Update the textarea with the result
      inputNumbersElement.value = resultString;
      numbers = resultString
      console.log(resultString)
  }
  function addNumbers() {
      console.log(numbers)
      if (numbers === '') {
        alert("No numbers to send.");
        return;
      }
      fetch(`${basepath()}/add_numbers`, {
        method: "POST",
        body: JSON.stringify({'numbers':numbers,'user':userDetails['email']})
      }).then(res => res.json())
      .then(data => {
          console.log(data)
          if(data.status === "success")
          {
              tell_message = "added sucessfully"
          }else if (data.status === "failure")
          {
              alert(data.message)
          }
      })

      map_numbers()
  }

  function map_numbers(){
      fetch(`${basepath()}/map_data`,{
          method:'post',
          body: JSON.stringify({'user':userDetails['email']})
      })
      .then(res => res.json())
      .then(data => {
          console.log(data, "number last loc")
          towerdata = data.data_dict
          ploatmaps()
          // data.data_dict.forEach(items => {
          //     console.log(items)
          //     if(items.lat){

          //       ploatmaps(items)
          //     }
              
          // });
      })
    }
    
    map_numbers()



  

  function ploatmaps() {
    try{

      markimg.setStyle(null);
      document.getElementById("person-img").style.display = "none"
    }
    catch{
      console.log("fresh")
    }
    towerdata.forEach(towerData => {
      
      console.log(towerData, "Tower Data");
      const lonLat = [parseFloat(towerData.long), parseFloat(towerData.lat)];
      let provider = towerData.provider;
  
      if (typeof provider === "string" && provider.trim() !== "") {
        provider = provider.toUpperCase();
      } else {
        provider = "Unknown";
      }
      let Iconsrc;
      switch (provider) {
        case "AIRTEL":
          Iconsrc = "../../person.png";
          break;
        case "CELLONE":
          Iconsrc = "../person.png";
          break;
        case "JIO":
          Iconsrc = "../person.png";
          break;
        case "VODAFONE":
          Iconsrc = "../person.png";
          break;
        default:
          Iconsrc = "../person.png";
      }
    
      
       markimg = new Feature({
            geometry: new Point(
              fromLonLat([parseFloat(towerData.long), parseFloat(towerData.lat)])
            ),
            azimuth: towerData.azimuth,
            coordinates: [parseFloat(towerData.long), parseFloat(towerData.lat)],
            name: towerData.areadescription,
          });

          const iconStyle = new Style({
            image: new Icon({
              src: Iconsrc,
              scale: 0.05,
            }),
          });
    // Function to toggle the blinking class
    

          const textStyle = new Style({
            text: new Text({
              text: towerData.areadescription ,
              offsetY: -40,
              fill: new Fill({
              color: 'red',

            }),
            font: 'bold 12px Arial', // Adjust the font weight and size as needed

            }),
          });

          // Use setStyle with an array to apply both iconStyle and textStyle
          markimg.setStyle([iconStyle, textStyle]);
          // map.getViewport().addEventListener('click', function() {
          // showdata=true
          // showdetails = towerData
          //         });

           

          vectorSource.addFeature(markimg);

          const vectorLayer = new VectorLayer({
            source: new VectorSource({
              features: [new Feature(new Point(fromLonLat([77.4533, 21.8903])))],
            }),
            style: iconStyle,
          });

          const maxScale = 0.2;
          map.on('moveend', function () {
            const zoomLevel = map.getView().getZoom();
            let newScale = 0.05 * Math.pow(2, zoomLevel - initialZoomLevel);
            newScale = Math.min(newScale, maxScale);
            iconStyle.getImage().setScale(newScale);
          });
          const initialZoomLevel = map.getView().getZoom();
          map.addLayer(vectorLayer);
                            

      if(towerData.state !== towerData.pre_state && towerData.pre_state !== "" && strangevalue >= towerData.distance  ){

      
      var element = document.createElement("div");
      // element.innerHTML = `${towerData.areadescription}</br>${towerData.lat},${towerData.long}`;
  
      element.className = "highlight";
    
  
      bookmarkImage = document.createElement("img");
      bookmarkImage.src = "../blinking.gif";
      bookmarkImage.id = "person-img";
      bookmarkImage.style.width = "25px";
      bookmarkImage.style.height = "25px";
      bookmarkImage.style.borderRadius = "50%";
      bookmarkImage.textContent = "Bookmark";
      bookmarkImage.addEventListener("click", () => 
        senddatatohtm(towerData)

    
      );
      element.appendChild(bookmarkImage);
      if(towerData.sate !== towerData.pre_state){
        // console.log(alert('changed'))
        bookmarkImage.className = "highlight"

      }
      var overlay = new Overlay({
        element: element,
        positioning: "bottom-center",
        stopEvent: false,
        offset: [15, 5],
      });
  
      overlay.setPosition(fromLonLat(lonLat));
      map.addOverlay(overlay);
    }
  });

    // return markimg;
  }

  function senddatatohtm(data){
    showdata = true
    showdetails = {}
    showdetails = data
    console.log(showdetails)

  }

 

</script>

<main class="main">

<div class="row">
<div class="col-9">
    <div class="map-container" bind:this={mapContainer} >
      
    </div>
    <div class="showlatlong text-end ">
      {showlatlong}
    </div>
</div>
<div class="col-3 rightbox">
  <button class="btn btn-primary mb-3" on:click={() => showfilters = !showfilters}>
      {#if showfilters}
          Hide Filters
      {:else}
          Show Filters
      {/if}
  </button>

  {#if showfilters}
      <div class="pb-3 border-bottom">
          <h6>Interested Numbers</h6>
          <div class="form-check">
              <input type="checkbox" class="form-check-input" id="interestedCheckbox" checked>
              <label class="form-check-label" for="interestedCheckbox">Interested Numbers</label>
              <button type="button" class="btn btn-secondary ms-3" data-bs-toggle="modal" data-bs-target="#addNumbersModal">+</button>
          </div>
      </div>

      <div class="pb-3 border-bottom">
          <h6>Source</h6>
          <div class="form-check">
              <input type="checkbox" class="form-check-input" id="airtelCheckbox"> 
              <label class="form-check-label" for="airtelCheckbox">CDAT</label>
          </div>
          <!-- Repeat similar structure for other checkboxes -->
      </div>

      <div class="pb-3 border-bottom">
          <h6>Distance in Kilometers</h6>
          <input type="range" class="form-range" min="0" max="1000" bind:value={strangevalue} on:change={ploatmaps}>
          <span>{strangevalue}</span>
      </div>

      <div class="pb-3 border-bottom">
        <h6>Provider</h6>
        <div class="">
            <input type="checkbox" class="form-check-input" id="airtelCheckbox">
            <label class="form-check-label" for="airtelCheckbox">Airtel</label>
            <input type="checkbox" class="form-check-input" id="airtelCheckbox">
            <label class="form-check-label" for="airtelCheckbox">Cellone</label>
            <input type="checkbox" class="form-check-input" id="airtelCheckbox">
            <label class="form-check-label" for="airtelCheckbox">Jio</label>
            <input type="checkbox" class="form-check-input" id="airtelCheckbox">
            <label class="form-check-label" for="airtelCheckbox">Vi</label>
        </div>
    
    </div>
    
  {/if}

  <div class="container mt-5">
      {#if showdata}
          <h5 class="card-title">
              Source Number:
              <a href="/cdat/profile?value={showdetails.source_number}" target="_blank">
                  {showdetails.source_number}
              </a>
          </h5>
          <div class="card">
              <div class="card-body">
                  <!-- <p class="card-text">Last Location: <span class="text-success">{showdetails.pre_state}</span></p> -->
                  <!-- <p class="card-text">Last Date: <span class="text-success">{showdetails.pre_date}</span></p> -->
                  <hr>
                  <p class="card-text">Current Location: <span class="text-danger">{showdetails.state}</span></p>
                  <!-- <p class="card-text">Current Areadescription: <span class="text-danger">{showdetails.}</span></p> -->
                  <p class="card-text">Current Date: <span class="text-danger">{showdetails.date}</span></p>
                  <!-- <p class="card-text">Distance: <span class="text-success">{showdetails.distance} km</span></p> -->
                  <p class="card-text">Source: <span class="text-success">{showdetails.from}</span></p>
              </div>
          </div>
      {/if}
  </div>
</div>

</div>



          
<div class="modal fade" id="addNumbersModal" tabindex="-1" aria-labelledby="addNumbersModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="addNumbersModalLabel">Add Interested Numbers</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <textarea id="inputNumbers" rows="5" cols="48" placeholder="Enter a sequence of numbers" on:input={insertCommas}></textarea>
        <p class="text-danger">{tell_message}</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button on:click={addNumbers} class="btn btn-primary">Add</button>
      </div>
    </div>
  </div>
</div>


        
     

        </main>
  
<style>
  .main {
    margin-left:5%;
    width: 94vw;
    margin-top: 10px;
  }
 
  .info {
    width: 99%;
    height: 15vh;
    background-color: rgb(245, 248, 248);
  }

  .map-container {
    height:92vh;
    /* width:77vw; */
    cursor: pointer;
  }
 
  .showlatlong {
    /* margin-right: ; */
    /* animation: colorChange 1s infinite; Adjust the duration as needed */
    /* background-color: red; */
    /* height: 10px; */
  }
  /* #addNumbersModal {
    margin-top:25%;
    margin-left: -20%;
  } */
  .card {
    widows: 40vw;
  }
  .filterbox button{
    background-color: rgb(222, 236, 16);
    width: 2vw;
    height: 3vh;
  }
  .rightbox{
    margin-top: 3%;
  }
</style>

   
          