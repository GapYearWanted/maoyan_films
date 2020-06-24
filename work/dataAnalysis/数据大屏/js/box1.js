var dom = document.getElementById("box1");
var myChart = echarts.init(dom);
var app = {};
option = null;
var labelRight = {
    normal: {
        position: 'right'
    }
};


var data = [
    [
    ["喜剧",5.91],
    ["爱情",6.79],
    ["剧情",6.51],
    ["音乐",5.92],
    ["奇幻",5.54],
    ["运动",6.9],
    ["动作",5.72],
    ["历史",5.28],
    ["传记",6.57],
    ["古装",7.0],
    ["武侠",7.0],
    ["动画",6.16],
    ["悬疑",4.95],
    ["家庭",6.55],
    ["惊悚",5.6],
    ["犯罪",6.34],
    ["纪录片",7.76],
    ["歌舞",6.55]
    ],
];

option = {
    backgroundColor: new echarts.graphic.RadialGradient(0.3, 0.3, 0.8, [{
        offset: 0,
        color: '#f7f8fa'
    }, {
        offset: 1,
        color: '#cdd0d5'
    }]),
    title: {
        text: '各类型电影评分---散点图'
    },
    xAxis: {
        type:'category',
        splitLine: {
            lineStyle: {
                type: 'dashed'
            }
        }
    },
    yAxis: {
        splitLine: {
            lineStyle: {
                type: 'dashed'
            }
        },
        scale: true
    },
    series: [{
        name: '1990',
        data: data[0],
        type: 'scatter',
        symbolSize: function (data) {
            return data[1]*3
        },
        emphasis: {
            label: {
                show: true,
                formatter: function (param) {
                    return param.data[3];
                },
                position: 'top'
            }
        },
        itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(120, 36, 50, 0.5)',
            shadowOffsetY: 5,
            color: new echarts.graphic.RadialGradient(0.4, 0.3, 1, [{
                offset: 0,
                color: 'rgb(251, 118, 123)'
            }, {
                offset: 1,
                color: 'rgb(204, 46, 72)'
            }])
        }
    }]
};
;
if (option && typeof option === "object") {
    myChart.setOption(option, true);
}