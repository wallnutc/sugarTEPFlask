fetch("http://127.0.0.1:5000/timelineByCourse1")
    .then(res => res.json())
    .then(function(out){
    const data = out[1];
    const schema = out[2];
    const binning = out[3]
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
              type: "column",
              aggregation: "sum"
            }
          ],
          title: "Hours Count",
          format: {
            suffix: " Hours"
          }
        }
      ],
      xAxis: {
        binning: binning
      }
    };
    dataSource.data = dataStore.createDataTable(data, schema);
  
    new FusionCharts({
      type: "timeseries",
      renderAt: "chart-container",
      width: "100%",
      height: "100%",
      dataSource: dataSource
    }).render();
  });


  