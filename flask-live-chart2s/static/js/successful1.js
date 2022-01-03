var chart;

/**
 * Request data from the server, add it to the graph and set a timeout
 * to request again
 */
function requestData() {
    $.ajax({
        url: '/live-data1',
        success: function(point) {
            var series = chart.series[0];
                shift = series.data.length > 20; // shift if the series is
                                                 // longer than 20

            // add the point
            chart.series[0].addPoint(point, true, shift);

            // call it again after one second
            //setTimeout(requestData, 1000);
        }
        //cache: false
    });

    $.ajax({
        url: '/live-data2',
        success: function(point) {
            var series2 = chart.series[1];
                shift2 = series2.data.length > 20; // shift if the series is
                                                 // longer than 20

            // add the point
            chart.series[1].addPoint(point, true, shift2);

            // call it again after one second
            //setTimeout(requestData, 1000);
        },
        //cache: false
    });

    $.ajax({
        url: '/live-data3',
        success: function(point) {
            var series3 = chart.series[2];
                shift3 = series3.data.length > 20; // shift if the series is
                                                 // longer than 20

            // add the point
            chart.series[2].addPoint(point, true, shift3);

            // call it again after one second
            //setTimeout(requestData, 1000);
        },
        //cache: false
    });

    $.ajax({
        url: '/live-data4',
        success: function(point) {
            var series4 = chart.series[3];
                shift4 = series4.data.length > 20; // shift if the series is
                                                 // longer than 20

            // add the point
            chart.series[3].addPoint(point, true, shift4);

            // call it again after one second
            //setTimeout(requestData, 1000);
        },
        //cache: false
    });

    $.ajax({
        url: '/live-data5',
        success: function(point) {
            var series5 = chart.series[4];
                shift5 = series5.data.length > 20; // shift if the series is
                                                 // longer than 20

            // add the point
            chart.series[4].addPoint(point, true, shift5);

            // call it again after one second
            setTimeout(requestData, 1000);
        },
        cache: false
    });
}

$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container',
            defaultSeriesType: 'spline',
            events: {
                load: requestData
            }
        },
        title: {
            text: 'Live random data'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150,
            maxZoom: 20 * 1000
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'Value',
                margin: 80
            }
        },
        series: [{
            name: 'Random data1',
            data: []
        }, {
            name: 'Random data2',
            data: []
        }, {
            name: 'Random data3',
            data: []
        }, {
            name: 'Random data4',
            data: []
        }, {
            name: 'Random data5',
            data: []
        }]
    });
    
});