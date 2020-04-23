
fetch("http://127.0.0.1:5000/timelineModuleGraphs")
    .then(res => res.json())
    .then(function(out){
    const data = out[0];
    const schema = out[1];
    
    console.log(schema)
    console.log(data)
    const dataStore = new FusionCharts.DataStore();
    const dataSource = {
      chart: {},
      caption: {
        text: "Total Hours Over Year"
      },
      subcaption: {
        text: "From September 2018 - May 2019"
      },
      series: "Module",
      yaxis: [
        {
          plot: [
            {
              value: "Hours",
              type: "column"
            }
          ],
          title: "Hours Count",
          format: {
            suffix: " Hours"
          }
        }
      ]
    };
    dataSource.data = dataStore.createDataTable(data, schema);
  
    new FusionCharts({
      type: "timeseries",
      renderAt: "chart-container",
      width: "100%",
      height: "500",
      dataSource: dataSource
    }).render();
  });
  