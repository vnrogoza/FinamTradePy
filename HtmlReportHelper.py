htmlReport = "AAA"

def Start():
    htmlReport = """
<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
  </head>
  <body>
  """
    
def AddScatter(id, data, title):
    import json    
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

def Finish():
    htmlAdd = """
      </body>
</html>
    """
    return htmlReport

def Show():
    import webbrowser
    with open("D:\\report.html", "w") as writer:
        writer.write(htmlReport)
    webbrowser.open('file://d:\\report.html')