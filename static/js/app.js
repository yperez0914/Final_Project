d3.select('#form').on('submit', userData);

function userData() {
    d3.event.preventDefault();
    var zipcode  = d3.select('#zip').node().value;
    var dates = d3.select('#date').node().value;
    console.log(dates)
    console.log(zipcode)
    var URL = `/userdata/${dates}/${zipcode}`
    window.open(URL, "_self")
}