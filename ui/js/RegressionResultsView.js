export function RegressionResultsView(data){
    $("#actual-results").empty()
    var str = "";
    for(var i in data){
        var col1 = '<div><b>Title: </b>' + data[i].app_name + '</div>';
        var col2 = '<div><b>Timestamp: </b>' + data[i].timestamp + '</div>';
        var col3 = '<div><b>Title: </b>' + data[i].title + '</div>';
        var col4 = '<div><b>Description: </b>' + data[i].descr + '</div>';
        str += '<div class="row border rounded shadow m-2"><div class="col">' + col1 + col2 + col3 + col4 + '</div></div>';
    }
    $("#actual-results").html(str);
}