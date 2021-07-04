function lineChart(price_data) {
    console.log("FUNCTION RUNNONG");
    console.log(price_data);
    console.log(typeof price_data);
    if ( price_data.length <= 0) {
        return;
    }
    var years = [];
    var min_prices = [];
    var max_prices = [];
    var modal_prices = [];

    price_data.forEach(element => {
        years.push(element[0]);
        min_prices.push(element[1]);
        max_prices.push(element[2]);
        modal_prices.push(element[3]);
    });

    console.log(years);
    console.log(min_prices);
    console.log(max_prices);
    console.log(modal_prices);
    var chart_canvas = document.getElementById("lineChart").getContext("2d");
    Chart.defaults.global.responsive = false;
    var chart_def = new Chart(chart_canvas,{
        type: 'line',
        data : {
            labels : years,
            datasets : [{
                data : min_prices,
                label : 'Max Prices',
                borderColor: "#8e5ea2",
                fill : true
            }, {
                data : max_prices,
                label : 'Min Prices',
                borderColor: "#36a2eb",
                fill : true
            }, {
                data : modal_prices,
                label : 'Average Modal Prices',
                borderColor: "#ff6384",
                fill : true
            }
            ]
        },
        options : {
            title : {
                display : true,
                text : 'Variation of prices acorss years'
            }
        }
    });
}

// function lineChart2(price_data) {
//     console.log("FUNCTION RUNNONG");
//     console.log(price_data);
//     console.log(typeof price_data);
//     if ( price_data.length <= 0) {
//         return;
//     }
//     var years = [];
//     var min_prices = [];
//     var max_prices = [];
//     var modal_prices = [];

//     price_data.forEach(element => {
//         years.push(element[2]);
//         max_prices.push(element[3]);
//         modal_prices.push(element[5]);
//         min_prices.push(element[4]);
//     });

//     console.log(years);
//     console.log(min_prices);
//     console.log(max_prices);
//     console.log(modal_prices);
//     var chart_canvas = document.getElementById("lineChart").getContext("2d");
//     Chart.defaults.global.responsive = false;
//     var chart_def = new Chart(chart_canvas,{
//         type: 'line',
//         data : {
//             labels : years,
//             datasets : [{
//                 data : min_prices,
//                 label : 'Min Prices',
//                 borderColor: "#8e5ea2",
//                 fill : false
//             }, {
//                 data : max_prices,
//                 label : 'Max Prices',
//                 borderColor: "#36a2eb",
//                 fill : false
//             }, {
//                 data : modal_prices,
//                 label : 'Average Modal Prices',
//                 borderColor: "#ff6384",
//                 fill : false
//             }
//             ]
//         },
//         options : {
//             title : {
//                 display : true,
//                 text : 'Variation of prices acorss years'
//             }
//         }
//     });
// }