import {ToggleSpinner} from './ToggleSpinner.js'

export function Comparator(file_data, file_name){

//    differ.js has to be linked before main.js !!!

    function draw_compare_table(a, b, filename=""){

        var dmp = new diff_match_patch();
        var diff = dmp.diff_main(JSON.stringify(JSON.parse(a.body), null, " "), JSON.stringify(JSON.parse(b.body), null, " "));

        var th = document.createElement('th');
            th.className = 'bg-light border';
            th.innerHTML = "<div class='container'>"
            + "<div class='row'>"
                + "<div class='col-9'>"
                    + b.timestamp
                + "</div>"
                + "<div class='col-3 d-flex justify-content-end'>"
                    + "<a class='btn btn-light' download='" + filename + "' href='data:text/plane;base64," + window.btoa(unescape(encodeURIComponent("//" + b.timestamp + "\n" + JSON.stringify(JSON.parse(b.body), null, "\t")))) + "'>"
                        + "<img src='/ui/img/download_icon.png' width='20'>"
                    + "</a>"
                + "</div>"
             + "</div>";

        var td = document.createElement('td');
            td.className = 'bg-light border valign-top';
            td.innerHTML = "<pre>" + dmp.diff_prettyHtml(diff) + "</pre>";

        $("#line-head").append(th);
        $("#line").append(td);
    }

    var logArr = file_data.match(/^{.+}$/gm);
    var iterator = 0;
    var list = [];

    logArr.forEach( (el, index) => {

        el = JSON.parse(el);

        var item = {
            "id" : iterator,
            "timestamp" : el["@timestamp"],
            "headers" : el["transaction"]["headers"],
            "source" : el["transaction"]["source"],
            "body" : el["transaction"]["data"]
        }

        list.push(item);
        iterator++;

    });

    list.sort( function(a, b) {
        if (new Date(a.timestamp) < new Date(b.timestamp)) { return -1; }
        else if (new Date(a.timestamp) > new Date(b.timestamp)) { return 1; }
        else { return 0; }
    });

    var noAnyDifference = true;
    $("#line").empty();
    $("#line-head").empty();
    for (var i = 1; i < list.length; i++) {
        if(list[i].body != list[i-1].body){
            noAnyDifference = false;
            draw_compare_table(list[i-1], list[i], file_name);
        }
    }
    if(noAnyDifference){
        $("#line-head").append(
            "<th class='bg-light border'>"
            + "<div class='container'>"
                + "<div class='row'>"
                    + "<div class='col-9'>"
                        + list[0].timestamp
                    + "</div>"
                    + "<div class='col-3 d-flex justify-content-end'>"
                        + "<a class='btn btn-light' download='" + file_name + "' href='data:text/plane;base64," + window.btoa(unescape(encodeURIComponent("//" + list[0].timestamp + "\n" +  JSON.stringify(JSON.parse(list[0].body), null, "\t")))) + "'>"
                            + "<img src='/ui/img/download_icon.png' width='20'>"
                        + "</a>"
                    + "</div>"
                + "</div>"
            + "</th>");
        $("#line").append("<td class='bg-light border'><pre class='text-muted'>" + JSON.stringify(JSON.parse(list[0].body), null, " ") + "</pre></td>")
        $("#line").append("<p>No any difference to show</p>")
    }

    ToggleSpinner();

    $('html, body').animate({scrollTop: $('#line-head').offset().top}, 1000);

}