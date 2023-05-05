// Set the dataset
const medians_dataset = medians.map(d => ({ year: d[0], value: d[1] }));
const dataset = vintageData.map(d => ({ year: d[0], value: d[1] }));

// Set the margin
const margin = { top: 20, right: 20, bottom: 30, left: 50 },
    width = 380 - margin.left - margin.right,
    height = 300 - margin.top - margin.bottom;

// Set the x-axis scale and domain
const xScale = d3.scaleBand().range([0, width]).padding(0.1);
xScale.domain(medians_dataset.map(d => d.year));

// Set the y-axis scale and domain
const yScale = d3.scaleLinear().range([height, 0]);
yScale.domain([minMax[0], minMax[1]]);

// Create the svg element
const svg = d3.select("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Add the x-axis
svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(xScale));

// Add the y-axis
svg.append("g")
    .call(d3.axisLeft(yScale).tickFormat(d => d + "€"));

// Add data points
const circles = svg.selectAll("circle")
    .data(dataset)
    .enter()
    .append("g")
    .attr("transform", d => "translate(" + (xScale(d.year) + xScale.bandwidth() / 2) + "," + yScale(d.value) + ")");

circles.append("circle")
    .attr("r", 4)
    .attr("fill", "steelblue");

circles.append("text")
  .text(d => d.value)
  .attr("x", 5)
  .attr("y", -5)
  .attr("font-size", "10px");

svg.selectAll(".median_circle")
    .data(medians_dataset)
    .enter().append("circle")
    .attr("class", "median_circle")
    .attr("cx", d => xScale(d.year) + xScale.bandwidth() / 2)
    .attr("cy", d => yScale(d.value))
    .attr("r", 0)
    .style("fill", "red");

// Adding line connecting the datapoints
svg.append("path")
    .datum(dataset)
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 1.5)
    .attr("d", d3.line()
      .x(d => xScale(d.year) + xScale.bandwidth() / 2)
      .y(d => yScale(d.value))
    );

// Adding line connecting the datapoints
svg.append("path")
    .datum(medians_dataset)
    .attr("fill", "none")
    .attr("stroke", "red")
    .attr("stroke-width", 1.5)
    .attr("d", d3.line()
      .x(d => xScale(d.year) + xScale.bandwidth() / 2)
      .y(d => yScale(d.value))
    );
    

// Add legend
const legend = svg.append("g")
  .attr("transform", "translate(" + (width - width + 20) + "," + (height - height + 40) + ")");
  
legend.append("line")
  .attr("x1", 0)
  .attr("y1", 5)
  .attr("x2", 10)
  .attr("y2", 5)
  .style("stroke", "red")
  .style("stroke-width", 2);

legend.append("text")
    .attr("x", 10)
    .attr("y", 5)
    .attr("dy", "0.32em")
    .attr("dx", "5")
    .style("font-size", "10px")
    .text("Appellation Median Price");

legend.append("circle")
    .attr("cx", 5)
    .attr("cy", 20)
    .attr("r", 4)
    .style("fill", "steelblue");

legend.append("text")
    .attr("x", 10)
    .attr("y", 20)
    .attr("dy", "0.32em")
    .attr("dx", "5")
    .style("font-size", "10px")
    .text(" " + wineData[0]);