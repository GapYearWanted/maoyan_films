var dom = document.getElementById("box3_left");
var myChart = echarts.init(dom);
var app = {};
option = null;
app.title = '极坐标系下的堆叠柱状图';

option = {
	textStyle:{//图例文字的样式
                color:'#dbdbdb',
                fontSize:10
           },
    angleAxis: {
    },
    radiusAxis: {
        type: 'category',
        data: ['中国大陆', '中国香港', '中国台湾'],
        z: 10
    },
    polar: {
    },
    series: [{
        type: 'bar',
        data: [11528],
        coordinateSystem: 'polar',
        name: 'A',
        stack: 'a'
    }, {
        type: 'bar',
        data: [2041],
        coordinateSystem: 'polar',
        name: 'B',
        stack: 'a'
    }, {
        type: 'bar',
        data: [2223],
        coordinateSystem: 'polar',
        name: 'C',
        stack: 'a'
    }],
    legend: {
        show: true,
        textStyle:{//图例文字的样式
                color:'#dbdbdb',
                fontSize:10
           },
        data: ['中国大陆', '中国香港', '中国台湾']
    }
};
;
if (option && typeof option === "object") {
    myChart.setOption(option, true);
}