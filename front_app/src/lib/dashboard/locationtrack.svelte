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
    // let personlayer
    
    onMount(() => {
    

    const indianStatesGeoJSONPath = "/indian_states.geojson";
    vectorSource = new VectorSource({
      format: new GeoJSON(),
      url: indianStatesGeoJSONPath,
    });

    const vectorLayer = new VectorLayer({
      source: vectorSource,
      style: function (feature) {
        const color = feature.get("color") || "#0000ff"; // Default to blue if no color is specified
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
  


      map = new Map({
        target: mapContainer,
        layers: [
          new TileLayer({
            source: new OSM({
              attributions: [],
            }),
          }),
          vectorLayer,
          PolygonSource,
          circleLayer, // Add the circle layer to the map
        ],
        view: new View({
          center: fromLonLat([77.4533, 21.8903]),
          zoom: 5,
        }),
      });
      // map = new Map({
      // 	target: mapContainer,
      // 	layers: [
      // 		new TileLayer({
      // 			source: new XYZ({
      // 				url: 'http://0.0.0.0:8082/tile/{z}/{x}/{y}.png'
      // 			}),
      // 		}),
      // 		vectorLayer,
      // 		circleLayer,
      // 	],
      // 	view: new View({
      // 		center: [0, 0],
      // 		zoom: 2
      // 	})
      // });
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
  
        
    }

    function map_numbers(){
        fetch(`${basepath()}/map_data`,{
            method:'post',
            body: JSON.stringify({'user':userDetails['email']})
        })
        .then(res => res.json())
        .then(data => {
            console.log(data, "number last loc")
            data.data_dict.forEach(items => {
                console.log(items)
                if(items.pre_location.lat){

                  ploatmaps(items.pre_location)
                }
                
            });
        })

    }
  
   map_numbers()
  
  
    
  
    function ploatmaps(towerData) {
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
     
      
      const markimg = new Feature({
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
              scale: 0.13,
            }),
          });
    // Function to toggle the blinking class
     

          const textStyle = new Style({
            text: new Text({
              text: towerData.areadescription,
              offsetY: -40,
              fill: new Fill({
              color: 'red',

            }),
            font: 'bold 12px Arial', // Adjust the font weight and size as needed

            }),
          });

          // Use setStyle with an array to apply both iconStyle and textStyle
          markimg.setStyle([iconStyle, textStyle]);
          markimg.on('click', function() {
            alert()
            // Toggle the visibility of the infoDiv
          });


          vectorSource.addFeature(markimg);

          

      if(towerData.state !== towerData.pre_state && towerData.pre_state !== ""){

      
      var element = document.createElement("div");
      // element.innerHTML = `${towerData.areadescription}</br>${towerData.lat},${towerData.long}`;
  
      element.className = "highlight";
     
  
      const bookmarkImage = document.createElement("img");
      bookmarkImage.src = "../blinking.gif";
      bookmarkImage.className = "person-img";
      bookmarkImage.style.width = "20px";
      bookmarkImage.style.height = "20px";
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

  <div class="map-container text-end" bind:this={mapContainer} >
    <div class="showlatlong text-end ">
            {showlatlong}
          </div>
          
        </div>    
        <div class="container-fuid info">
          <div class="accordion" id="accordionExample">
            
            <div class="accordion-item">
              <h2 class="accordion-header" id="headingTwo">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                  Add Intrested Numbers
                </button>
              </h2>
              <div id="collapseTwo" class="accordion-collapse collapse" aria-labelledby="headingTwo" data-bs-parent="#accordionExample">
                <div class="accordion-body text-end">
                  <textarea id="inputNumbers" rows="5" cols="40" placeholder="Enter a sequence of numbers" on:input={insertCommas}></textarea>
                    <p class="text-danger">{tell_message}</p>  <button on:click={addNumbers}>Add</button>
                 </div>
                </div>
                <div class="container mt-4">
                  {#if showdata}
                    <div class="card">
                      <div class="card-body">
                        <h5 class="card-title">Source Number: {showdetails.number}</h5>
                        <p class="card-text">Last Location: <span style="color: green;">{showdetails.pre_state}</span></p>
                        <p class="card-text">Last Areadescription: <span style="color: green;">{showdetails.pre_areadescription}</span></p>
                        <p class="card-text">Last State: <span style="color: green;">{showdetails.pre_state}</span></p>
                        <hr>
                        <p class="card-text">Current Location: <span style="color: red;">{showdetails.state}</span></p>
                        <p class="card-text">Current Areadescription: <span style="color: red;">{showdetails.areadescription}</span></p>
                        <p class="card-text">Current State: <span style="color: red;">{showdetails.state}</span></p>
                      </div>
                    </div>
                  {/if}
                </div>
                

        </div>

        
    </div>

  </main>
    
    
    <style>
      .main {
      display: flex;
      align-items: flex-start;
      margin-left: 5%;
      width: 91vw;
      margin-top: 30px;
    }
   
    .info {
        margin-top: 1.5%;
        width: 30vw;
        height: 93vh;
        margin-left: 1%;
        background-color: rgb(245, 248, 248);
    }
  
    .map-container {
      height: 90vh;
      width:90%;
      cursor: pointer;
    }
   
    .showlatlong {
      margin-top: 3%;
      /* animation: colorChange 1s infinite; Adjust the duration as needed */
      /* background-color: red; */
      /* height: 10px; */
    }

  .blink {
    animation: blinkAnimation 1s infinite;
  }

  @keyframes blinkAnimation {
    0%, 100% {
      fill: red;
    }
    50% {
      fill: transparent;
    }
  }
  .person-img{
    border-radius: 50%;
  }

  </style>
  