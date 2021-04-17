var data = [{

  "Dates": "2021-04-18",
  "Cloudcover": "62",
  "Humidity": "72",
  "Pressure": "1014",
  "FeelsLike": "44",
  "HeatIndex": "46",
  "MaxTemp": "54",
  "MinTemp": "38",
  "SunHours":"9.1",
  "UVIndex":"5",
  "TempDelta":"16",
  "BarChange":"0.003",
  "HeatChange":"0.022",
  "HumChange":"-0.014"
}, {

  "Dates": "2021-04-18",
  "Cloudcover": "62",
  "Humidity": "72",
  "Pressure": "1014",
  "FeelsLike": "44",
  "HeatIndex": "46",
  "MaxTemp": "54",
  "MinTemp": "38",
  "SunHours":"9.1",
  "UVIndex":"5",
  "TempDelta":"16",
  "BarChange":"0.003",
  "HeatChange":"0.022",
  "HumChange":"-0.014"
}, {

  "Dates": "2021-04-18",
  "Cloudcover": "62",
  "Humidity": "72",
  "Pressure": "1014",
  "FeelsLike": "44",
  "HeatIndex": "46",
  "MaxTemp": "54",
  "MinTemp": "38",
  "SunHours":"9.1",
  "UVIndex":"5",
  "TempDelta":"16",
  "BarChange":"0.003",
  "HeatChange":"0.022",
  "HumChange":"-0.014"
}, {

  "Dates": "2021-04-18",
  "Cloudcover": "62",
  "Humidity": "72",
  "Pressure": "1014",
  "FeelsLike": "44",
  "HeatIndex": "46",
  "MaxTemp": "54",
  "MinTemp": "38",
  "SunHours":"9.1",
  "UVIndex":"5",
  "TempDelta":"16",
  "BarChange":"0.003",
  "HeatChange":"0.022",
  "HumChange":"-0.014"
}, {

  "Dates": "2021-04-18",
  "Cloudcover": "62",
  "Humidity": "72",
  "Pressure": "1014",
  "FeelsLike": "44",
  "HeatIndex": "46",
  "MaxTemp": "54",
  "MinTemp": "38",
  "SunHours":"9.1",
  "UVIndex":"5",
  "TempDelta":"16",
  "BarChange":"0.003",
  "HeatChange":"0.022",
  "HumChange":"-0.014"
}, {

  "Dates": "2021-04-18",
  "Cloudcover": "62",
  "Humidity": "72",
  "Pressure": "1014",
  "FeelsLike": "44",
  "HeatIndex": "46",
  "MaxTemp": "54",
  "MinTemp": "38",
  "SunHours":"9.1",
  "UVIndex":"5",
  "TempDelta":"16",
  "BarChange":"0.003",
  "HeatChange":"0.022",
  "HumChange":"-0.014"
}, {

  "Dates": "2021-04-18",
  "Cloudcover": "62",
  "Humidity": "72",
  "Pressure": "1014",
  "FeelsLike": "44",
  "HeatIndex": "46",
  "MaxTemp": "54",
  "MinTemp": "38",
  "SunHours":"9.1",
  "UVIndex":"5",
  "TempDelta":"16",
  "BarChange":"0.003",
  "HeatChange":"0.022",
  "HumChange":"-0.014"
}]

d3.select("pricing_table_wdg")
  .selectAll("ul")
  .data("data")
  .enter()
  .append("ul")
  .append("li")
  .html(function(d) {
    return `<li>${d.Dates}</li>
            <li>${d.Clpudcover}</li>
            <li>${d.Humidity}</li><li>${d.Pressure}</li>
            <li>${d.FeelsLike}</li><li>${d.HeatIndex}</li>
            <li>${d.MaxTemp}</li>
            <li>${d.MinTemp}</li>
            <li>${d.SunHours}</li>
            <li>${d.UVIndex}</li>
            <li>${d.TempDelta}</li>
            <li>${d.BarChange}</li>
            <li>${d.HeatChange}</li>
            <li>${d.HumChange}</li>`;
  });

  console.log(data)