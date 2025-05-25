import os, webbrowser, json    
htmlReport = ''
htmlMarkers = ''

def Start():
    global htmlReport 
    htmlReport = '''
<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
  </head>
  <body>
  '''

def Finish():
    global htmlReport 
    htmlAdd = '''
      </body>
</html>
    '''
    htmlReport += htmlAdd
    #return htmlReport

def Show():
    global htmlReport 
    fileName = 'report.html'
    fileName = os.getcwd()+'\\'+fileName
    #with open("D:\\report.html", "w") as writer:
    with open(fileName, 'w') as writer: 
        writer.write(htmlReport)
    webbrowser.open('file://'+fileName)
    

def AddScatter(id, data, title):    
    data = list(data)
    htmlAdd = '''
    <div id="$id" style="width: 200px; height: 500px;">
		<script type="text/javascript">
	        google.charts.load("current", {"packages":["scatter"]});
            google.charts.setOnLoadCallback(drawChart);

            function drawChart () {

                var data = new google.visualization.DataTable();
                data.addColumn("number', "Часы обучения");
                data.addColumn("number', "Финал");

                data.addRows( $addRows );
                var options = {
                width: 800,
                height: 500,
                chart: {
                    title: "$title",
                    subtitle: "$subTitle"
                },
                hAxis: {title: "Часы"},
                vAxis: {title: "Оценка"}
                };

                var chart = new google.charts.Scatter(document.getElementById("$id"));
                chart.draw(data, google.charts.Scatter.convertOptions(options));
            }
	    </script>
	</div>
    '''
    #data_json = json.dumps(nodes)
    htmlAdd = (htmlAdd
        .replace("$id", id)
        .replace("$addRows", data.__repr__())
        .replace("$title", title)
        .replace("$subTtitle", ''))
    htmlReport += htmlAdd

def AddChart(id, data, title):
    global htmlReport 
    data = list(data)
    htmlAdd = """
    <div id="$id" style="width: 1900px; height: 1000px;">
	<script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawVisualization);

      function drawVisualization() {
        // Some raw data (not necessarily accurate)
        var data = google.visualization.arrayToDataTable( $data );
        var options = {
          title : '$title',
          vAxis: {title: 'Price'},
          //hAxis: {title: 'Day', showTextEvery:5},
          hAxis: {title: 'Day'},
          seriesType: 'candlesticks'          
          };
        var chart = new google.visualization.ComboChart(document.getElementById('$id'));
        chart.draw(data, options);
      }  
    </script>
	</div>
    """
    #data_json = json.dumps(nodes)
    htmlAdd = (htmlAdd
        .replace("$id", id)
        .replace("$data", data.__repr__())
        .replace("$title", title)
        .replace("$subTtitle", ''))
    htmlReport += htmlAdd


def AnychartStart(title):
    global htmlReport 
    htmlReport = '''<html>
 <head>  
  <title> $title </title>  
  <style>html, body, #container { width: 100%; height: 100%; margin: 0; padding: 0; }</style>
  <script src="https://cdn.anychart.com/releases/8.13.0/js/anychart-core.min.js"></script>
  <script src="https://cdn.anychart.com/releases/8.13.0/js/anychart-stock.min.js"></script>
  <script src="https://cdn.anychart.com/releases/8.13.0/js/anychart-annotations.min.js"></script>
  <script src="https://cdn.anychart.com/releases/8.13.0/js/anychart-exports.min.js"></script>
  <script src="https://cdn.anychart.com/releases/8.13.0/js/anychart-ui.min.js"></script>
 </head>
 <body>'''
    htmlReport = htmlReport.replace('$title', title)

def AnychartAddChart(**kwargs):
    global htmlReport 
    data = kwargs['data']
    if kwargs.get('security') != None:        
      security = kwargs['security']
    htmlAdd = '''\n  <div id="container"></div>  
  <script type="text/javascript"> 
    anychart.onDocumentReady(function () { 

	  //CHART Candlestick
      var data = $data                    
      var dataTable = anychart.data.table(0);
      dataTable.addData(data);      
      var mapping = dataTable.mapAs({ open: 1, high: 2, low: 3, close: 4 });  // map the loaded data for the candlestick series       
      var chart = anychart.stock();       
      var plot = chart.plot(0);  // create the chart plot      
      plot.yGrid(true).xGrid(true).yMinorGrid(true).xMinorGrid(true);      
      var series = plot.candlestick(mapping);  // create the candlestick series
      series.name(" $security ");
      series.legendItem().iconType("rising-falling");
      series.risingStroke("#000000");
  	  series.risingFill("#ffffff");
      series.fallingStroke("#000000");
      series.fallingFill("#000000"); '''
    #data_json = json.dumps(nodes)
    htmlAdd = ( htmlAdd
        .replace('$security', security)
        .replace('$data', data.__repr__())
        .replace('None', 'null')
         )        
    htmlReport += htmlAdd

def AnychartAddLine(**kwargs):
    global htmlReport 
    data = kwargs['data']
    if kwargs.get('security') != None:
      security = kwargs['security']
    id = '2'
    if kwargs.get('id') != None:
      id = str(kwargs['id'])
    htmlAdd = '''\n\n      //LINE Indicator
      table$id = anychart.data.table();
      table$id.addData( $data );	          
      mapping$id = table$id.mapAs();
      mapping$id.addField("value", 1);
      var plot$id = chart.plot(0).line(mapping$id);
      plot$id.stroke("$color")'''
    htmlAdd = ( htmlAdd
        .replace('$data', data.__repr__())
        .replace('None', 'null')
        .replace('$id', id)        
         )        
    if kwargs.get('color') != None:
      htmlAdd = htmlAdd.replace('$color', str(kwargs['color']))
    else:
      htmlAdd = htmlAdd.replace('$color', '#0066ff')
    htmlReport += htmlAdd


def AnychartAddOrder(**kwargs):
    global htmlReport, htmlMarkers    
    #if kwargs.get("id") != None:
    #  id = str(kwargs["id"])
    id = kwargs['id']
    time = kwargs['time']
    price = kwargs['price']
    type = kwargs['type']
    size = 10
    offset = 10
    if type == 'Buy':
      color = '#00ff00 0.5'
      border = '#00ff00'
      markerType = 'arrowUp'
    if type == 'Sell':
      color = '#ff0000 0.5'
      border = '#ff0000'
      markerType = 'arrowDown'
      offset = -10
    if htmlMarkers=='':
      htmlMarkers = '\n\n      //MARKERS \n      var controller = plot.annotations();  '
      htmlReport += htmlMarkers
    htmlAdd = '\n      marker$id = controller.marker({ xAnchor: "$time", valueAnchor: $price, size: $size, offsetY: $offset, normal:{fill:"$color", stroke:"$border"}, markerType:"$markertype" });	'
    htmlAdd = ( htmlAdd
        .replace('$id', str(id)) 
        .replace('$time', str(time))
        .replace('$price', str(price))
        .replace('$size', str(size)) 
        .replace('$offset', str(offset)) 
        .replace('$color', str(color))
        .replace('$border', str(border)) 
        .replace('$markertype', str(markerType)) 
        ) 
    htmlReport += htmlAdd

def AnychartAddTrades(**kwargs):
    global htmlReport    
    id = kwargs['id']
    data = kwargs['data']
    htmlAdd = '''\n\n      //COLUMN CHART (Trades)
	  table$id = anychart.data.table('x');
	  table$id.addData( $data );
	  mapping$id_pos = table$id.mapAs({x:'x', value:'value'});
	  var series$id_pos = chart.plot($id).column(mapping$id_pos);
	  series$id.name("PL");
	  mapping$id_neg = table$id.mapAs({x:'x', value:'value2'});
	  var series$id_neg = chart.plot($id).column(mapping$id_neg);
	  series$id_neg.fill("#ff0000")
	  chart.plot($id).height(100)
    '''
    htmlAdd = ( htmlAdd
        .replace('$id', str(id)) 
        .replace('$time', str(data))
    )
    htmlReport += htmlAdd
    

def AnychartFinish(title):
    global htmlReport 
    htmlAdd = '''\n      
      chart.title(" $title ");
      chart.container("container");
      chart.draw();
    });   
  </script>
 </body>
</html>

    '''
    htmlAdd = htmlAdd.replace("$title", title)
    htmlReport += htmlAdd
    #return htmlReport