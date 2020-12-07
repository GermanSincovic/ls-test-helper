import {RequestManager} from './RequestManager.js'
import {Repeater} from './Repeater.js'

var urlPathParameters = location.pathname.split("/");
var urlGetParameters = new URLSearchParams(window.location.search);

var publicAPIRequestParams = {
    "environment": urlPathParameters[3],
    "feed": urlPathParameters[4],
    "sport": urlGetParameters.get("sport"),
    "ls_date": urlGetParameters.get("date"),
    "id": urlGetParameters.get("id"),
    "pid": urlGetParameters.get("pid")
}

window.location.sport = publicAPIRequestParams.sport;
window.location.environment = publicAPIRequestParams.environment;
if (publicAPIRequestParams.ls_date){
    window.location.ls_date = publicAPIRequestParams.ls_date;
    window.location.date = [publicAPIRequestParams.ls_date.substr(0,4), publicAPIRequestParams.ls_date.substr(4,2), publicAPIRequestParams.ls_date.substr(6,2)].join('-');
}
if (publicAPIRequestParams.id){
    window.location.id = publicAPIRequestParams.id;
}
if (publicAPIRequestParams.pid){
    window.location.pid = publicAPIRequestParams.pid;
}


var data_link = location.origin + "/ui/public-api";
    data_link += "/" + publicAPIRequestParams.environment;
    data_link += "/" + publicAPIRequestParams.feed;
    data_link += "?sport=" + publicAPIRequestParams.sport;
    if(publicAPIRequestParams.feed == "event-list"){
        data_link += "&date=" + publicAPIRequestParams.ls_date;
    } else if(publicAPIRequestParams.feed == "event") {
        data_link += "&pid=" + publicAPIRequestParams.pid;
        data_link += "&id=" + publicAPIRequestParams.id;
    }

var data_update_link = data_link + "&update=true";

var live_count_link = "/public-api/" + window.location.environment + "/live/count";

$.ajax({
    url: "/urlconfig",
    success: function(res){
        window.api_config = res.message[publicAPIRequestParams.environment];
    }
});

const RM = new RequestManager();
    if(publicAPIRequestParams.feed == "event-list"){
        RM.getPublicAPIDaily(data_update_link);
        RM.getPublicAPILiveCount(live_count_link);
        $("#" + location.sport).prop('checked', true);
        $("#calendar-picker").val(location.date);
        new Repeater( () => {
            RM.getPublicAPIDaily(data_update_link);
            RM.getPublicAPILiveCount(live_count_link);
        }, 5000 );
    } else if(publicAPIRequestParams.feed == "event"){
        RM.getPublicAPIEvent(data_update_link)
        new Repeater( () => {RM.getPublicAPIEvent(data_update_link)}, 5000 );
    }

new Repeater( () => {$('[data-toggle="tooltip"]').tooltip();}, 2000 );