

console.log({hello:"kevin"})




d3.json("/data.json", function(data) {
    console.log(data);
})






d3.select("pricing_table_wdg")
  .selectAll("tr")
  .data(austinWeather)
  .enter()
  .append("tr")
  .html(function(d) {
    return `<td>${d.date}</td><td>${d.low}</td><td>${d.high}</td>`;
  });



