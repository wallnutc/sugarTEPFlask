
function timelineCourse(courseID, label, container){
  var url = "http://mvroso.pythonanywhere.com/timelineByCourse" + courseID.toString()
  fetch(url)
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
          text: label
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
        renderAt: container,
        width: "100%",
        height: "100%",
        dataSource: dataSource
      }).render();
    });
};

function pieCourse(courseID,label,type, container){
  var url = "http://mvroso.pythonanywhere.com//activityTypePieChartsByCourse" + courseID.toString()
  fetch(url)
      .then(res => res.json())
      .then(function(out){
      const module = out.ByModule;
      const activity = out.ByActivity;
      const grade = out.ByGrade;
      if (type == "module"){
        data = module;
        caption = "Year Breakdown by Module Hours";
        centerlabel = "$label: $value hours";
      }
      else if (type == "activity"){
        data = activity;
        caption = "Year Breakdown by Activity Type Hours";
        centerlabel = "$label: $value hours";
      }
      else if (type == "grade"){
        data = grade;
        caption = "Year Breakdown by Avergae Activity Type Grade";
        centerlabel = "$label: $value%"
      }
      const datasource = {
        chart: {
          caption: caption,
          bgColor: "#ffffff",
          startingAngle: "310",
          legendNumColumns: "1",
          plotHighlightEffect: "fadeout",
          legendPosition: "right",
          legendAllowDrag: "0",
          legendScrollBgColor: "#ffffff",
          showLegend: "1",
          defaultCenterLabel: label,
          centerlabel: centerlabel,
          centerLabelBold: "1",
          doughnutradius: "100",
          showTooltip: "0",
          showLabels: "0",
          decimals: "1",
          theme: "fusion"
        },
        data: data
      }
      
      new FusionCharts({
        type: 'doughnut2d',
        renderAt: container,
        width: '100%',
        height: '100%',
        dataFormat: 'json',
        dataSource: datasource
      }).render();
    });      
};

function pieModule(moduleID,label,type,container){
  var url = "http://mvroso.pythonanywhere.com/activityTypePieChartsByModule" + moduleID.toString()
  fetch(url)
      .then(res => res.json())
      .then(function(out){
      const hours = out.ByHours;
      const grade = out.ByGrade;

      if (type == "hours"){
        data = hours;
        caption = "Year Breakdown by Activity Type Hours"
      }
      else if (type == "grade"){
        data = grade;
        caption = "Year Breakdown by Activity Type Grade"
      }
      const datasource = {
        chart: {
          caption: caption,
          plotHighlightEffect: "fadeout",
          subcaption:label,
          legendNumColumns: "1",
          legendPosition: "right",
          legendAllowDrag: "0",
          numberPrefix: "$",
          bgColor: "#ffffff",
          startingAngle: "310",
          showLegend: "1",
          showTooltip: "0",
          decimals: "1",
          theme: "fusion"
        },
        data: data
      }
      new FusionCharts({
        type: 'pie2d',
        renderAt: container,
        width: '100%',
        height: '100%',
        dataFormat: 'json',
        dataSource: datasource
      }).render();
    });      
};

function nestedPieCourse(courseID,label,container){
  var url = "http://mvroso.pythonanywhere.com/nestedPieByCourse" + courseID.toString()
  fetch(url)
      .then(res => res.json())
      .then(function(out){
      const data = out;
      const dataSource = {
        chart: {
          caption: "Total Year Breakdown By Hours",
          subcaption: label,
          showplotborder: "1",
          legendNumColumns: "1",
          plotHighlightEffect: "fadeout",
          legendPosition: "right",
          legendAllowDrag: "0",
          plotfillalpha: "60",
          hoverfillcolor: "#CCCCCC",
          numberprefix: "$",
          theme: "fusion",
          plottooltext:"<b>$label</b> contributed <b>$value hours</b>, which was <b>$percentValue</b> of <b>$category.label</b>",
          showLegend: "1",
          showLabels: "0",
          highlightParentPieSlices: "0",
          highlightChildPieSlices: "1"
        },
        category: data
      }

      new FusionCharts({
      type: "multilevelpie",
      renderAt: container,
      width: "100%",
      height: "100%",
      dataFormat: "json",
      dataSource
      }).render();
      })
};

function feedbackChartsByQuestion(moduleID, questionName,type, bardial,container){
  var url = "/feedbackBarChartsByModule" + moduleID.toString()
  fetch(url)
      .then(res => res.json())
      .then(function(out){
      data = out;
      if(type == "activity"){
        dataType = data.byActivity;
      }
      if(type == "class"){
        dataType = data.byClass;
      }
      if(type == "module"){
        dataType = data.byModule;
      }

      for (i=0; i< dataType.length; i++){
        if(dataType[i].question == questionName){
          q = dataType[i];
        }
      }
      if (bardial == "bar"){
        const bardataSource = {
          chart: {
            caption: "Distribution of responses for " + q.question + " by " + type,
            labelDisplay: "Auto",
            xaxisname: "Score",
            yaxisname: "# of Entries",
            theme: "fusion"
          },
          data: q.bardata,
          yAxis: [{
            format: {
                round: "0"
            }
          }]
        }
        new FusionCharts({
          type: "column2d",
          renderAt: container,
          width: "100%",
          height: "100%",
          dataFormat: "json",
          dataSource: bardataSource
          }).render(); 
      }
      else {
        const dialdataSource = {
          chart: {
            caption: "Average score for " + questionName + " by " + type,
            lowerlimit: "0",
            upperlimit: "10",
            showvalue: "1",
            theme: "fusion",
            showtooltip: "0"
          },
          colorrange: {
            color: [{minvalue: "0",maxvalue: "3.33",code: "#F2726F"},{minvalue: "3.33",maxvalue: "6.66",code: "#FFC533"},{minvalue: "6.66",maxvalue: "10",code: "#62B58F"}]
          },
          dials: {
            dial: [{value: q.dialvalue.toString()}]}
        };
    
        new FusionCharts({
            type: "angulargauge",
            renderAt: container,
            width: "100%",
            height: "100%",
            dataFormat: "json",
            dataSource: dialdataSource
          }).render();
      }
    })
}