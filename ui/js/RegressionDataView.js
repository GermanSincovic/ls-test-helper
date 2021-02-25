export function RegressionDataView(data){
    $("#test-data").empty();
    var str = "";
    for(var i in data){
        var col1 = '<div class="col-6"><b>Action: </b>' + data[i].action + '</div>';
        var col2 = '<div class="col-6"><b>Extra data: </b>' + JSON.stringify(data[i].extra_data) + '</div>';
        var col3 = (data[i].timestamp) ? '<div class="col-12"><b>Timestamp: </b>' + data[i].timestamp + '</div>' : "";
        var col4 = '<div class="col-12"><b>Title: </b>' + data[i].expected_result.title + '</div>';
        var col5 = '<div class="col-12"><b>Description: </b>' + data[i].expected_result.message + '</div>';
       str += '<div class="row border rounded shadow m-2">' + col1 + col2 + col3 + col4 + col5 + '</div>';
    }
    $("#test-data").html(str);
}