function makeStackedChart(response, ctx, typeChart, title, xlabel) {

    var mydatasets = [];
    var colorslist = ['rgba(199, 0, 57, 0.8)','rgba(255, 87, 51, 0.6)','rgba(255, 141, 26, 0.6)','rgba(237, 221, 83, 0.6)','rgba(87, 199, 133, 0.6)','rgba(0, 186, 173, 0.6)','rgba(42, 123, 155, 0.6)','rgba(61, 61, 107, 0.6)','rgba(81, 24, 73, 0.6)','rgba(144, 12, 63, 0.8)','rgba(63, 56, 68, 0.6)',];
    var borderlist = ['rgba(199, 0, 57, 1)','rgba(255, 87, 51, 1)','rgba(255, 141, 26, 1)','rgba(237, 221, 83, 1)','rgba(173, 212, 92, 1)','rgba(87, 199, 133, 1)','rgba(0, 186, 173)','rgba(42, 123, 155, 1)','rgba(61, 61, 107, 1)','rgba(81, 24, 73, 1)','rgba(144, 12, 63, 1)','rgba(63, 56, 68, 1)',];
    for(var j = 0; j < response.datasets.length; j++) {
        mydatasets.push({label: response.datasets[j].label, backgroundColor: colorslist[j], boderColor: borderlist[j], data: response.datasets[j].data.split(','), spanGraphs: true});
    }
    var subjectsData = {
        labels: response.labels.split(','),
        datasets: mydatasets
    }

    var options = {
        title: {
            display: true,
            text: title,
            position: 'top'
        },
        scales: {
            xAxes: [{
                stacked: true,
                ticks: {
                    min: response.startAxis,
                    max: response.endAxis
                },
                scaleLabel: {
                    display: true,
                    labelString: xlabel,
                    fontSize: 14
                }
            }],
            yAxes: [{
                stacked: true,
                ticks: {
                        suggestedMin: 0.1
                    },
                scaleLabel: {
                        display: true,
                        labelString: 'Hours',
                        fontSize: 14
                    }
            }]
        }
    };
    var myChart = new Chart(ctx,
    {
        type: typeChart,
        data: subjectsData ,
        options: options
    });
    return myChart;
}

function makePieChart(response, ctx, typeChart, title) {
    var mydatasets = [];
    var colorslist = ['rgba(199, 0, 57, 0.8)','rgba(255, 87, 51, 0.6)','rgba(255, 141, 26, 0.6)','rgba(237, 221, 83, 0.6)','rgba(87, 199, 133, 0.6)','rgba(0, 186, 173, 0.6)','rgba(42, 123, 155, 0.6)','rgba(61, 61, 107, 0.6)','rgba(81, 24, 73, 0.6)','rgba(144, 12, 63, 0.8)','rgba(63, 56, 68, 0.6)',];
    var borderlist = ['rgba(199, 0, 57, 1)','rgba(255, 87, 51, 1)','rgba(255, 141, 26, 1)','rgba(237, 221, 83, 1)','rgba(173, 212, 92, 1)','rgba(87, 199, 133, 1)','rgba(0, 186, 173)','rgba(42, 123, 155, 1)','rgba(61, 61, 107, 1)','rgba(81, 24, 73, 1)','rgba(144, 12, 63, 1)','rgba(63, 56, 68, 1)',];
    
    for(var j = 0; j < response.datasets.length; j++) {
            mydatasets.push({backgroundColor: colorslist, boderColor: borderlist, data: response.datasets[j].data.split(','), spanGraphs: true});
    }
    subjectsData = {
        labels: response.labels.split(','),
        datasets: mydatasets
    }
    
    var barOptions = {
        title: {
            display: true,
            text: title,
            position: 'top',
            fontSize: 20,
            fontFamily: 'Roboto',
        },
        scales: {
            yAxes: [{
                ticks: {
                        beginAtZero: true
                    },
                scaleLabel: {
                        display: true,
                        labelString: 'Hours',
                        fontSize: 14
                    }
            }]
        }
    };

    var pieOptions = {
        legend: {
            display: true
        },
        title: {
                  display: true,
                  text: title,
                  position: 'top',
                  fontSize: 20,
                  fontFamily: 'Roboto',
              },
        rotation: -0.7 * Math.PI,
    };
    var myChart;
    if(typeChart == 'bar'){
        myChart = new Chart(ctx,
            {
                type: typeChart,
                data: subjectsData,
                options: barOptions
            });
    }
    else myChart = new Chart(ctx,
        {
            type: typeChart,
            data: subjectsData,
            options: pieOptions
        });
    myChart.generateLegend()
    return myChart;
}