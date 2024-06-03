function _1(md){return(
md`# Untitled`
)}

function _force(FileAttachment){return(
FileAttachment("force.json").json()
)}

function _3(force,d3)
{
  // Estrai i nodi e i collegamenti dal JSON
  const nodes = force.nodes.map(node => ({ ...node }));
  const links = force.links.map(link => ({ ...link }));
  
  const width = 800;
  const height = 800;
  const margin = { top: 20, bottom: 20, left: 50, right: 50 };

  const svg = d3
    .create("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .style("border", "1px dotted red");
  
  // Crea la simulazione della forza di D3 per il layout del grafo
  // Crea la simulazione della forza di D3 per il layout del grafo
  const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id).distance(50))
    .force("charge", d3.forceManyBody().strength(-400))
    .force("center", d3.forceCenter(width / 2, height / 2));
  // Aggiungi i collegamenti al grafico
  const link = svg.append("g")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
    .selectAll("line")
    .data(links)
    .join("line")
      .attr("stroke-width", d => Math.sqrt(d.value));
  
  // Aggiungi i nodi al grafico
  const node = svg.append("g")
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5)
    .selectAll("circle")
    .data(nodes)
    .join("circle")
      .attr("r", 25)
      .attr("fill", "blue")
      .call(drag(simulation));
  
  // Aggiungi etichette ai nodi
  const label = svg.append("g")
    .selectAll("text")
    .data(nodes)
    .join("text")
      .attr("x", 8)
      .attr("y", "0.31em")
      .text(d => d.id);
  
  // Aggiorna la posizione dei nodi e dei collegamenti durante la simulazione
  simulation.on("tick", () => {
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);
  
    node
      .attr("cx", d => d.x)
      .attr("cy", d => d.y);
  
    label
      .attr("x", d => d.x)
      .attr("y", d => d.y);
  });
  
  // Funzione per gestire il trascinamento dei nodi
  function drag(simulation) {
    function dragstarted(event) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }
    
    function dragged(event) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    }
    
    function dragended(event) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }
    
    return d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended);
  }
  
  // Aggiungi il grafico SVG al documento
  return svg.node();


}


function _limits_it_regions(FileAttachment){return(
FileAttachment("limits_IT_regions.geojson").json()
)}

function _5(d3,limits_it_regions)
{
  const width = 1000;
  const height = 1000;
  const projection = d3.geoMercator().fitSize([width, height], limits_it_regions);
  const path = d3.geoPath().projection(projection);
  const features = limits_it_regions.features
  
  // Crea il layout del grafo
  const svg = d3.create("svg")
  .attr("viewBox", [0, 0, width, height])
  .style("font", "12px sans-serif");
  
  // Gruppo per la mappa dell'Italia
  const mapLayer = svg.append("g");
  
 const sva = mapLayer.selectAll("path")
    .data(features)
    .join("path")
    .attr("d", path)
    .attr("fill", "#e0e0e0") // Colore di riempimento
    .attr("stroke", "#000")   // Colore del contorno
    .attr("stroke-width", 0.5); // Spessore del contorno

  return svg.node()
}


export default function define(runtime, observer) {
  const main = runtime.module();
  function toString() { return this.url; }
  const fileAttachments = new Map([
    ["force.json", {url: new URL("./files/6733c264a935db1f356ae0aecc2fa7e6c0bc10e0ed040e956ccf2a364c702174df1ca16b6da0fc1ce9a625a0bebb9294c0f567b54907eafef810a3b61b139647.json", import.meta.url), mimeType: "application/json", toString}],
    ["limits_IT_regions.geojson", {url: new URL("./files/78f7cdeb59e25802165a63de761bfbe3157cc696d7dab18242c130759ca1dd646a9998142d9075386fca3498fbcaea557e5fffe9c14b1ada7aa2f84968353e1b.geojson", import.meta.url), mimeType: "application/geo+json", toString}]
  ]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["md"], _1);
  main.variable(observer("force")).define("force", ["FileAttachment"], _force);
  main.variable(observer()).define(["force","d3"], _3);
  main.variable(observer("limits_it_regions")).define("limits_it_regions", ["FileAttachment"], _limits_it_regions);
  main.variable(observer()).define(["d3","limits_it_regions"], _5);
  return main;
}
