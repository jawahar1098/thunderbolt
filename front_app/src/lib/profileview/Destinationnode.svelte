<script>
    import { onMount } from 'svelte';
    import { basepath } from "$lib/config";
    import * as d3 from 'd3';
    
    export let number;
    let userData = [];
    let nodes = [];
    let links = [];
    console.log('inside dest count')
    async function sendNumberToFlask() {
        
      const mode='';
      const userNumber = number.trim();
      console.log(userNumber,"usernumber")
        try {
          const formdata = new FormData()
          formdata.append("number", number)
          formdata.append("mode",'unique_other_number')


          const response = await fetch(
            `${basepath()}/profile_num`,
            {
              method: "POST",
              body: formdata,
            }
          );
          console.log("Response:", response);
          if (!response.ok) {
            throw new Error("Network response was not ok");
          } else {
            const data = await response.json();
            console.log(data);
  
            userData = [];
            nodes = [];
            links = [];
            nodes.push({id: userNumber,type: "root"});
            console.log(userNumber)
            data.destination_numbers.forEach((cell) => {
              nodes.push({ id: cell.destination_number});
              links.push({ source: userNumber, target: cell.destination_number});
            });
            // console.log(nodes,links,"-----")
            createForceDirectedGraph();
          }
        } catch (error) {
          console.error("Error fetching user data:", error);
        }
    }
    function getRandomColor() {
    const letters = "0123456789ABCDEF";
    let color = "#";
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }
    function createForceDirectedGraph() {
    const width = 700;
    const height = 700;

    const svg = d3.select("#graph-container").append("svg")
    .attr("width", width)
    .attr("height", height);

    const simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id((d) => d.id).distance(100))
        .force("charge", d3.forceManyBody().strength(-700))
        .force("center", d3.forceCenter(width / 2, height / 2));

    const link = svg.selectAll(".link")
        .data(links)
        .enter()
        .append("line")
        .attr("class", "link")
        .style("stroke", "steelblue");

    const node = svg.selectAll(".node")
        .data(nodes)
        .enter()
        .append("g")
        .attr("class", "node")
        .call(d3.drag()
        .on("start", (event, d) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        })
        .on("drag", (event, d) => {
            d.fx = event.x;
            d.fy = event.y;
        })
        .on("end", (event, d) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        })
        );

    node.append("circle")
        .attr("r", 20)
        .style("fill", () => getRandomColor()) 
        .style("stroke", "steelblue")
        .style("stroke-width", "2px");

    node.append("text")
        .text((d) => d.id)
        .attr("text-anchor", "middle")
        .style("font-size", "12px")
        .style("fill", "black")
        .style("pointer-events", "none")
        .attr("dy", -25)
        .attr("dx", 5);

    simulation.on("tick", () => {
        link
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);

        node
        .attr("transform", (d) => `translate(${d.x},${d.y})`);
    });

    }
    onMount(() => {
        console.log("---------------------------")
        sendNumberToFlask();
        });
    
  </script>
  
  <!-- <main class="container">
    <form>
      <input type="text" bind:value={USER_NUMBER} />
      <button on:click={(event) => sendNumberToFlask(event)}>Show</button>
    </form>
  </main>
-->

<div id="graph-container" class="graph-container"></div>

   
  
  
  <style>
    .graph-container {
      flex: 1;
      margin-left: 11%;
      
    }
  
  </style> 