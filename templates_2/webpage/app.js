var clickHandler = d3.select("#filter-btn");
                                           
//event
clickHandler.on("click", function() {

//delete
d3.select("tbody").html("");

//stop page from refreshing
d3.event.preventDefault();

var dates  = d3.select("#form-control date").property("value");
console.log(date);
