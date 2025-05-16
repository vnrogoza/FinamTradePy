import os, webbrowser, json    
htmlReport = ""

def Start():
    global htmlReport 
    htmlReport = """
<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
  </head>
  <body>
  """

def Finish():
    global htmlReport 
    htmlAdd = """
      </body>
</html>
    """
    htmlReport += htmlAdd
    #return htmlReport

def Show():
    global htmlReport 
    fileName = "report.html" 
    fileName = os.getcwd()+"\\"+fileName
    #with open("D:\\report.html", "w") as writer:
    with open(fileName, "w") as writer: 
        writer.write(htmlReport)
    webbrowser.open('file://'+fileName)
    

def AddScatter(id, data, title):    
    data = list(data)
    htmlAdd = """
    <div id="$id" style="width: 200px; height: 500px;">
		<script type="text/javascript">
	        google.charts.load('current', {'packages':['scatter']});
            google.charts.setOnLoadCallback(drawChart);

            function drawChart () {

                var data = new google.visualization.DataTable();
                data.addColumn('number', 'Часы обучения');
                data.addColumn('number', 'Финал');

                data.addRows( $addRows );
                var options = {
                width: 800,
                height: 500,
                chart: {
                    title: '$title',
                    subtitle: '$subTitle'
                },
                hAxis: {title: 'Часы'},
                vAxis: {title: 'Оценка'}
                };

                var chart = new google.charts.Scatter(document.getElementById('$id'));
                chart.draw(data, google.charts.Scatter.convertOptions(options));
            }
	    </script>
	</div>
    """
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
    htmlReport = """
<html>
 <head>  
  <title> $title </title>  
  <style>html, body, #container { width: 100%; height: 100%; margin: 0; padding: 0; }</style>
  <script src="https://cdn.anychart.com/releases/8.11.0/js/anychart-core.min.js"></script>
  <script src="https://cdn.anychart.com/releases/8.11.0/js/anychart-stock.min.js"></script>
  <script src="https://cdn.anychart.com/releases/8.11.0/js/anychart-data-adapter.min.js"></script>
  <script src="https://cdn.anychart.com/releases/8.11.0/js/anychart-exports.min.js"></script>
 </head>
 <body>
  """
    htmlReport = htmlReport.replace("$title", title)

def AnychartAddChart(**kwargs):
    global htmlReport 
    data = kwargs["data"]
    if kwargs.get("security") != None:        
      security = kwargs["security"]
    htmlAdd = """

    <div id="container"></div>
  
  <script type="text/javascript"> 
    anychart.onDocumentReady(function () {  
	  //prepare data  
      var data = $data          
              
      // create a data table with the loaded data
      var dataTable = anychart.data.table(0);
      dataTable.addData(data);

      // map the loaded data for the candlestick series
      var mapping = dataTable.mapAs({ open: 1, high: 2, low: 3, close: 4 });

      // create a stock chart
      var chart = anychart.stock();

      // create the chart plot
      var plot = chart.plot(0);
      
      // set the grid settings
      plot.yGrid(true).xGrid(true).yMinorGrid(true).xMinorGrid(true);

      // create the candlestick series
      var series = plot.candlestick(mapping);
      series.name(' $security ');
      series.legendItem().iconType('rising-falling');   	

    """
    #data_json = json.dumps(nodes)
    htmlAdd = ( htmlAdd
        .replace("$security", security)
        .replace("$data", data.__repr__())
        .replace("None", "null")
         )        
    htmlReport += htmlAdd

def AnychartAddLine(**kwargs):
    global htmlReport 
    data = kwargs["data"]
    if kwargs.get("security") != None:
      security = kwargs["security"]
    id = '2'
    if kwargs.get("id") != None:
      id = str(kwargs["id"])
    htmlAdd = """
      //add line indicator
      table$id = anychart.data.table();
      table$id.addData( $data );	          
      mapping$id = table$id.mapAs();
      mapping$id.addField('value', 1);
      var plot$id = chart.plot(0).line(mapping$id);
    """
    htmlAdd = ( htmlAdd
        .replace("$data", data.__repr__())
        .replace("None", "null")
        .replace("$id", id)        
         )        
    htmlReport += htmlAdd


def AnychartFinish(title):
    global htmlReport 
    htmlAdd = """

      // set the title of the chart
      chart.title(' $title ');

      // set the container id for the chart
      chart.container('container');      
      
      // initiate the chart drawing
      chart.draw();
    });   
  </script>
 </body>
</html>

    """    
    htmlAdd = htmlAdd.replace("$title", title)
    htmlReport += htmlAdd
    #return htmlReport