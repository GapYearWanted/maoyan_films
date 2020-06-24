var dom = document.getElementById("box2");
var myChart = echarts.init(dom);
var app = {};
option = null;
option = {
    title: {
        text: '漏斗图',
    },
    toolbox: {
        feature: {
            dataView: {readOnly: false},
            restore: {},
            saveAsImage: {}
        }
    },
    series: [
        {
            type: 'funnel',
            left: '10%',
            width: '80%',
            label: {
                formatter: '{b}'
            },
            labelLine: {
                show: false
            },
            itemStyle: {
                opacity: 0.7
            },
            data: [
                {value:3156,name:'0~19'},
                {value:2174,name:'20~39'},
                {value:920,name:'40~59'},
                {value:1910,name:'60~79'},
                {value:5189,name:'80~99'},
                {value:1453,name:'100~119'},
                {value:400,name:'120~139'},
                {value:228,name:'>=140'},
            ]
        }]
};
;
if (option && typeof option === "object") {
    myChart.setOption(option, true);
}