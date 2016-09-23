google.charts.load('visualization', {'packages':['treemap',"corechart"]});
google.charts.setOnLoadCallback(drawChart);
 
//getting the csv color map with PAPA parse
//This data was created separately. It is used to assign a color to each contributor in the list and on the bottom right plot
var mapPath = 'http://localhost:8000/dataFiles/authColorMapGrafted.csv';
var colorMap = {};
Papa.parse(mapPath, {
    download: true,
    complete: function(results) {
        for (i=0;i<results.data.length;i++){
            colorMap[results.data[i][0]] = results.data[i][1]
        }
    }
});


function drawChart() {
    //this is the main data file. It was created using the db2csv.py script and Daniel German's database
    var path = 'http://localhost:8000/dataFiles/graftedData.csv';
    var query = new google.visualization.Query( path,
	   { csvColumns: ['string', 'string','number', 'number', 'string', 'string', 'string', 'string', 'string', 'string', 'string', 'string', 'string', 'string', 'string', 'string', 'string', 'string', 'string', 'string', 'string', 'string', 'string', 'string', 'number','number','number', 'number', 'number','number', 'number', 'number', 'number', 'number', 'number', 'number', 'number', 'number', 'number', 'number', 'number', 'number', 'number', 'number','string','number','number','string'], 
	   csvHasHeader: true });
    query.send(handleQueryResponse);

    function handleQueryResponse(response) {
        if (response.isError()) {
        	alert('Error in query: ' + response.getMessage() + ' ' +
        	response.getDetailedMessage());
        	return;
        }

        var data = response.getDataTable();
        var tree = new google.visualization.TreeMap(document.getElementById('chart_div'));
        var options = {
                highlightOnMouseOver: true,
                maxDepth: 1,
                maxPostDepth: 2,
                minHighlightColor: '#8c6bb1',
                midHighlightColor: '#9ebcda',
                maxHighlightColor: '#edf8fb',
                minColor: '#009688',
                midColor: '#f7f7f7',
                maxColor: '#ee8100',
                generateTooltip: showFullTooltip,
                noColor: "#ecf0f1",
                textStyle: {bold:true},
                headerHeight: 35,
           };
        tree.draw(data, options);

        function showFullTooltip(row, size, value) {
            if ( data.getValue(row,5) == ""){
              var output = '<div style="background:#fd9; padding:10px; border-style:solid">' +
                     '<span style="font-family:Courier"><b>' + data.getValue(row, 0) +
                    '</span><br>' +
                     ' Number of LoC in this folder or file: ' + size + '<br>' +
                 'Author 1 : ' + data.getValue(row, 4) + "  " + data.getValue(row, 24)+' LOC'+ "  " + (100*(data.getValue(row, 24)/data.getValue(row, 2))).toFixed(2) + '%<br>' + 
                 '<a href=' + data.getValue(row, 44) + '> Github Blame </a>' +
                 ' </div>';
            }
            else if ( data.getValue(row,6) == ""){
              var output = '<div style="background:#fd9; padding:10px; border-style:solid">' +
                     '<span style="font-family:Courier"><b>' + data.getValue(row, 0) +
                    '</span><br>' +
                     ' Number of LoC in this folder or file: ' + size + '<br>' +    
                 'Author 1 : ' + data.getValue(row, 4) + "  " + data.getValue(row, 24)+' LOC'+ "  " +(100*(data.getValue(row, 24)/data.getValue(row, 2))).toFixed(2) + '%<br>' + 
                'Author 2 : ' + data.getValue(row, 5) + "  " + data.getValue(row, 25)+' LOC'+"  " + (100*(data.getValue(row, 25)/data.getValue(row, 2))).toFixed(2) +'%<br>' + 
                 '<a href=' + data.getValue(row, 44) + '> Github Blame </a>' +
                 ' </div>';
            }
            else {
              var output = '<div style="background:#fd9; padding:10px; border-style:solid">' +
                     '<span style="font-family:Courier"><b>' + data.getValue(row, 0) +
                    '</span><br>' +
                     ' Number of LoC in this folder or file: ' + size + '<br>' +
                 'Author 1 : ' + data.getValue(row, 4) + "  " + data.getValue(row, 24)+' LOC'+ "  " + (100*(data.getValue(row, 24)/data.getValue(row, 2))).toFixed(2) +'%<br>' + 
                 'Author 2 : ' + data.getValue(row, 5) + "  " + data.getValue(row, 25)+' LOC'+ "  " + (100*(data.getValue(row, 25)/data.getValue(row, 2))).toFixed(2) +'%<br>' + 
                 'Author 3 : ' + data.getValue(row, 6) + "  " + data.getValue(row, 26)+' LOC'+ "  " + (100*(data.getValue(row, 26)/data.getValue(row, 2))).toFixed(2) +'%<br>' + 
                 '<a href=' + data.getValue(row, 44) + '> Github Blame </a>' +
                 ' </div>';
            }
            return output
          }

        google.visualization.events.addListener(tree, 'select', myOnClickFunction);

        var listElement = document.getElementById('list');
        var listDescription = document.getElementById('listDescription');
        var itemData = document.getElementById('itemData');
        var barplot = document.getElementById('barplot');

        function myOnClickFunction(){
           
            //The following code will put together the list and send it to the html document.
            listDescription.innerHTML = "Top Contributors in : <font size='5'><b>" + data.getValue(tree.getSelection()[0]["row"],0) + "</b></font>";

            var firstCommitDate = new Date( data.getValue(tree.getSelection()[0]["row"],45) *1000);
            var secondCommitDate = new Date( data.getValue(tree.getSelection()[0]["row"],46) *1000);
            
            itemData.innerHTML = "<p> First commit: " + firstCommitDate.toLocaleString() + "</p>" +
                                 "<p> Last commit: " + secondCommitDate.toLocaleString() + "</p>" +
                                 "<p> Size (LoC): " + data.getValue(tree.getSelection()[0]["row"],2) + "</p>";                              
                                    
            

            var list = "";
            list += "<tr>   <th>#</th>  <th>Name</th>   <th>LOC</th> <th>Percentage</th>    </tr>";
            var count = 1;
            for (i=4; i < 24; i++){
                if (data.getValue(tree.getSelection()[0]["row"],i) != "") {
                    // list += '<li class="list-group-item"> <a href="#">  ' + count + '. ' + data.getValue(tree.getSelection()[0]["row"],i).toLocaleString() + ' </a> <span class="badge">' + data.getValue(tree.getSelection()[0]["row"],i+20) + '</span> </li>';
                    list += '<tr><td>' + count + '</td><td style="color:' + colorMap[data.getValue(tree.getSelection()[0]["row"],i)]+'">'+ data.getValue(tree.getSelection()[0]["row"],i) 
                     +'</td><td>'+ data.getValue(tree.getSelection()[0]["row"],i+20) +'</td> <td>'+ (100*(data.getValue(tree.getSelection()[0]["row"],i+20)/data.getValue(tree.getSelection()[0]["row"],2))).toFixed(2)+'%</td></tr>'
                    count ++
                }
            }
            listElement.innerHTML = list;

            //the following code will draw the bar plot

            var author1 = [data.getValue(tree.getSelection()[0]["row"],4),data.getValue(tree.getSelection()[0]["row"],24),data.getValue(tree.getSelection()[0]["row"],47)];
            var author2 = [data.getValue(tree.getSelection()[0]["row"],5),data.getValue(tree.getSelection()[0]["row"],25),data.getValue(tree.getSelection()[0]["row"],47)];
            var author3 = [data.getValue(tree.getSelection()[0]["row"],6),data.getValue(tree.getSelection()[0]["row"],26),data.getValue(tree.getSelection()[0]["row"],47)];
            var rest = ["Rest", (data.getValue(tree.getSelection()[0]["row"],2) - (data.getValue(tree.getSelection()[0]["row"],24)+data.getValue(tree.getSelection()[0]["row"],25)+data.getValue(tree.getSelection()[0]["row"],26)))];
            var barChartData = {
                labels: [author1[0], author2[0], author3[0], rest[0]],
                datasets: [
                            {
                                label: "Lines of Code in " + data.getValue(tree.getSelection()[0]["row"],0),
                                backgroundColor: [
                                    colorMap[author1[0]], //author 1
                                    colorMap[author2[0]], //author 2
                                    colorMap[author3[0]], //author 3
                                    'rgba(75, 192, 192, 0.2)',
                                ],
                                borderColor: [
                                ],
                                borderWidth: 1,
                                data: [author1[1], author2[1], author3[1], rest[1]],
                            }
                        ]
            };
            Chart.defaults.global.events = [];
            var barChart = new Chart(barplot, {
                type: 'bar',
                data: barChartData,
                options: options
            });
        }
    }
}

