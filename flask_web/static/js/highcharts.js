var chart;

function requestData() {

    // 각각의 센서 데이터를 실시간으로 그래프에 할당
    $.ajax({
        url: '/live-data1',
        success: function(point) {
            var series = chart.series[0];
                shift = series.data.length > 20; // 그래프의 길이가 20보다 길어질 경우 그래프 이동

            //그래프의 점에 센서 데이터 할당
            chart.series[0].addPoint(point, true, shift);

        }

    });

    $.ajax({
        url: '/live-data2',
        success: function(point) {
            var series2 = chart.series[1];
                shift2 = series2.data.length > 20;

                chart.series[1].addPoint(point, true, shift2);

        },

    });

    $.ajax({
        url: '/live-data3',
        success: function(point) {
            var series3 = chart.series[2];
                shift3 = series3.data.length > 20;

                chart.series[2].addPoint(point, true, shift3);

        },

    });

    $.ajax({
        url: '/live-data4',
        success: function(point) {
            var series4 = chart.series[3];
                shift4 = series4.data.length > 20;

                chart.series[3].addPoint(point, true, shift4);

        },

    });

    $.ajax({
        url: '/live-data5',
        success: function(point) {
            var series5 = chart.series[4];
                shift5 = series5.data.length > 20;

                chart.series[4].addPoint(point, true, shift5);
        },
    });

    $.ajax({
        url: '/live-data6',
        success: function(point) {
            var series6 = chart.series[5];
                shift6 = series6.data.length > 20;

            chart.series[5].addPoint(point, true, shift6);

            // 1초 뒤 재호출
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
            text: '실시간 센서 측정값'
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
            name: 'DS18B20_온도',
            data: []
        }, {
            name: 'DHT22_온도',
            data: []
        }, {
            name: 'DHT22_습도',
            data: []
        }, {
            name: 'MH-Z19B_이산화탄소',
            data: []
        }, {
            name: 'MQ2_가스',
            data: []
        }, {
            name: 'GY-712_전류(가변저항을 이용한 변화)',
            data: []
        }]
    });
    
});