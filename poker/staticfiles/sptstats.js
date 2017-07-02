$(document).ready(function() {
 $.getJSON('/get_placementwins', { }, function (callback) {
    console.log(callback);
    var firstplaceData = [];
    var secondplaceData = [];
    var thirdplaceData = [];
    var forthplaceData = [];
    
    var yourLabels = [];
    
    for (var i = 0, len = callback.length; i < len; ++i) 
    {
    	var firstp = [
				callback[i]['firstplaces']
		];
    	var secondp = [
    			callback[i]['secondplaces']
		];
       	var thirdp = [
				callback[i]['thirdplaces']
		];
       	var forthp = [
				callback[i]['forthplaces']
		];

    	var Labels = [
    			callback[i]['firstname']
    	];

    	firstplaceData.push(firstp);
    	secondplaceData.push(secondp);
    	thirdplaceData.push(thirdp);
    	forthplaceData.push(forthp);
    	
    	yourLabels.push(Labels);
    }
   $(function () {
	   $(document).ready(function () {
        $('#plot1').highcharts({
        	 chart: {
                 type: 'column'
             },
             credits: {
                 enabled: false
             },
            legend: {enabled: false},
            title: {text: 'Placement Wins'},
            xAxis: {    
            	type: 'category',
                labels: {
                    rotation: -45,
                    style: {
                        fontSize: '13px',
                        fontFamily: 'Verdana, sans-serif'
                    },
                    formatter: function() {
                        return yourLabels[this.value];
                    }
                }
            },
            yAxis: {
         	   labels: {
         	       enabled: false
         	   },
         	   title: {
                    text: 'Placement'
                }
            },
            stackLabels: {
                enabled: true,
                style: {
                    fontWeight: 'bold',
                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                }
            },
            legend: {
                reversed: true
            },
            tooltip: {
                formatter: function () {
                    return '<b>' + this.x + '</b><br/>' +
                        this.series.name + ': ' + this.y + '<br/>' +
                        'Total: ' + this.point.stackTotal;
                }
            },
            plotOptions: {
                series: {
                    stacking: 'normal',
                    dataLabels: {
                        enabled: true,
                        color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white',
                        style: {
                            textShadow: '0 0 3px black'
                        }
                    }

                }
            },
            series: [{
                name: '4th',
                data: forthplaceData
            }, {
                name: '3rd',
                data: thirdplaceData
            }, {
                name: '2nd',
                data: secondplaceData
            }, {
                name: '1st',
                data: firstplaceData
            }]
        });
   });
   });   
 });
}) 

$(document).ready(function() {
 $.getJSON('/get_profit', { }, function (callback) {
    console.log(callback);
       
    var chartSeriesData = [];
    for (var i = 0, len = callback.length; i < len; ++i) 
    {
    	var series = [
				callback[i]['firstname'],
				callback[i]['profit']
		];
    	
    	chartSeriesData.push(series);
    }
    
   //start
   $(function () {
     $('#plot2').highcharts({
    	 chart: {
             type: 'column',
         },
         credits: {
             enabled: false
         },
         title: {text: 'Cumalative Profit'},
         xAxis: {
             type: 'category',
             labels: {
                 rotation: -45,
                 style: {
                     fontSize: '13px',
                     fontFamily: 'Verdana, sans-serif'
                 }
             }
         },
         yAxis: {
             title: {
                 text: 'profit'
             }
         },
         legend: {
             enabled: false
         },        
         series: [{
             name: 'Profit',
             data: chartSeriesData,
             dataLabels: {
                 enabled: true,
                 rotation: -90,
                 color: '#FFFFFF',
                 align: 'right',
                 y: -50, 
                 style: {
                     fontSize: '13px',
                     fontFamily: 'Verdana, sans-serif'
                 }
             }
         }]
     });
   });
 });
})
function generateData(cats, names, points) {
	var ret = {},
    ps = [],
    series = [],
    len = cats.length;

	//concat to get points
	for (var i = 0; i < len; i++) {
    	ps[i] = {
        	x: cats[i],
        	y: points[i],
        	n: names[i]
    	};
	}
	names = [];
	//generate series and split points
	for (i = 0; i < len; i++) {
    	var p = ps[i],
        	sIndex = $.inArray(p.n, names);

    	if (sIndex < 0) {
        	sIndex = names.push(p.n) - 1;
        	series.push({
            	name: p.n,
            	data: []
        	});
    	}
    	series[sIndex].data.push(p);
	}
	return series;
}

$(document).ready(function() {
 $.getJSON('/get_profitbyseason', { }, function (callback) {
    console.log(callback);
    
    var seasonstmp;
    var datatmp;
    var namestmp;

    var seasons = [];
    var data = [];
    var names = [];

    for (var i = 0, len = callback.length; i < len; ++i) 
    {
    	seasonstmp = callback[i]['seasonnumber'];
    
        datatmp = callback[i]['profit'];
        
        namestmp = callback[i]['firstname'];
    
        seasons.push(seasonstmp);
      	data.push(datatmp);
      	names.push(namestmp);
    }
       
    var series = [];

	series = generateData(seasons, names, data);

    
   $(function () {
	   $(document).ready(function () {
        $('#plot3').highcharts({
            title: {
                text: 'Profit by Season',
                x: -20 //center
            },
            credits: {
                enabled: false
            },
            xAxis: {
            	allowDecimals: false,
            	tickInterval:1		 	
           },
            yAxis: {
            	title: {
                    text: 'Seasons'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                valuePrefix: '$'
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            series: series
        });
   });
   });   
 });
})

$(document).ready(function() {
 $.getJSON('/get_plfinaltablewins', { }, function (callback) {
    console.log(callback);
    
    var yourLabels = [];
    var ftData = [];
    var plData = [];
    
    for (var i = 0, len = callback.length; i < len; ++i) 
    {
    	var ft = [
				callback[i]['finaltablewins']
		];

    	var pl = [
    			callback[i]['plleader']
    	];
    	    	
    	var Labels = [
    			callback[i]['firstname']
    	];
    	
    	if (callback[i]['finaltablewins'] > 0 || callback[i]['plleader'] > 0) {  
    		ftData.push(ft);
    		plData.push(pl);
    		yourLabels.push(Labels);
    	}
    }
    
   $(function () {
	   $(document).ready(function () {
        $('#plot4').highcharts({
        	   chart: {
                   type: 'column',
               },
               credits: {
            	      enabled: false
               },
               legend: {enabled: false},
               title: {text: 'Season Champs & Season Point Leaders'},
               xAxis: {    
               	type: 'category',
                   labels: {
                       rotation: -45,
                       style: {
                           fontSize: '13px',
                           fontFamily: 'Verdana, sans-serif'
                       },
                       formatter: function() {
                           return yourLabels[this.value];
                       }
                   }
               },
               yAxis: {
            	   labels: {
            	       enabled: false
            	   },
            	   title: {
                       text: 'Season Champs & Season Point Leaders'
                   }
               },
               stackLabels: {
                   enabled: true,
                   style: {
                       fontWeight: 'bold',
                       color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                   }
               },
               legend: {
                   reversed: true
               },
               tooltip: {
                   formatter: function () {
                       return '<b>' + this.x + '</b><br/>' +
                           this.series.name + ': ' + this.y + '<br/>' +
                           'Total: ' + this.point.stackTotal;
                   }
               },
               plotOptions: {
                   series: {
                       stacking: 'normal',
                       dataLabels: {
                           enabled: true,
                           color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white',
                           style: {
                               textShadow: '0 0 3px black'
                           },
                           formatter:function() {
                        	    if(this.y != 0) {
                        	      return this.y;
                        	    }
                           }
                       }

                   }
               },
               //series: [{}],
               series: [{
                   name: 'Season Point Leader',
                   data: plData
               }, {
            	   name: 'Season Champion',
                   data: ftData
               }]
        });
   });
   });   
 });
}) 

$(document).ready(function() {
 $.getJSON('/get_placement', { }, function (callback) {
    console.log(callback);
    
    var chartSeriesData = [];
    var yourLabels = [];
    
 
    
    for (var i = 0, len = callback.length; i < len; ++i) 
    {
    	var series = [
				callback[i]['percent']
		];
    	
    	var Labels = [
    			callback[i]['firstname']
    	];
    	chartSeriesData.push(series);
    	yourLabels.push(Labels);
    }
 	
   $(function () {   
	   $(document).ready(function () {
        $('#plot5').highcharts({
            chart: {
                type: 'column',
               
            },
            credits: {
                enabled: false
            },
            legend: {enabled: false},
            title: {text: 'Top 4 Placement %'},
            xAxis: {    
            	type: 'category',
                labels: {
                    rotation: -45,
                    style: {
                        fontSize: '13px',
                        fontFamily: 'Verdana, sans-serif'
                    },
                    formatter: function() {
                        return yourLabels[this.value];
                    }
                }
            },
            yAxis: {
         	   labels: {
         	       enabled: false
         	   },
         	   title: {
                    text: 'Placement'
                }
            },
            stackLabels: {
                enabled: true,
                style: {
                    fontWeight: 'bold',
                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                }
            },
            legend: {
                reversed: true
            },
            tooltip: {
                formatter: function () {
                    return '<b>' + this.x + '</b><br/>' +
                        this.series.name + ': ' + this.y + '<br/>' +
                        'Total: ' + this.point.stackTotal;
                }
            },
            plotOptions: {
                series: {
                    stacking: 'normal',
                    dataLabels: {
                        enabled: true,
                        color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white',
                        style: {
                            textShadow: '0 0 3px black'
                        }
                    }

                }
            },
            //series: [{}],
            series: [{
                name: 'Top 4 placement %',
                data: chartSeriesData,
                dataLabels: {
                    enabled: true,
                    rotation: -90,
                    color: '#FFFFFF',
                    align: 'right',
                    format: '{point.y:.2f}', // two decimal
                    y: -50, 
                    style: {
                        fontSize: '13px',
                        fontFamily: 'Verdana, sans-serif'
                    }
                }
            }]
        });
   });
   });   
 });
}) 

