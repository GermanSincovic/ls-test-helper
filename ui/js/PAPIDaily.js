import {ToggleSpinner} from './ToggleSpinner.js'

export function PAPIDaily(data){

    this.LSDateGetYear = function(ls_date){
        return ls_date.toString().substr(0,4);
    }

    this.LSDateGetMonth = function(ls_date){
        return ls_date.toString().substr(4,2)
    }

    this.LSDateGetDay = function(ls_date){
        return ls_date.toString().substr(6,2)
    }

    this.LSDateGetHours = function(ls_date){
        return ls_date.toString().substr(8,2)
    }

    this.LSDateGetMinutes = function(ls_date){
        return ls_date.toString().substr(10,2)
    }

    this.LSDateGetSeconds = function(ls_date){
        return ls_date.toString().substr(12,2)
    }

    this.getEventStartDateCol = function(esd){
        return "<td style='vertical-align: middle;'>" + this.LSDateGetHours(esd) + ":" + this.LSDateGetMinutes(esd) + "</td>";
    }

    this.getEventStatusText = function(eps){
        return "<td style='vertical-align: middle;'>" + eps + "</td>"
    }

    this.getEventParticipant = function(t, side){
        var align = "";
        var data = "";
        if(side == "left"){ align = "right"; }
        if(side == "right"){ align = "left"; }
        for (var i = 0; i < t.length; i++){
            var badge_link = (t[i].Img) ? static_url + t[i].Img : "/ui/img/no_badge.png";
            if(side == "left"){
                data += "<div>" + t[i].Nm + " <small class='text-muted'>(" + t[i].ID + ")<img width='30' height='30' src='" + badge_link + "'></small></div>";
            }
            if(side == "right"){
                data += "<div><img width='30' height='30' src='" + badge_link + "'><small class='text-muted'>(" + t[i].ID +")</small> " + t[i].Nm + "</div>"
            }
        }
        return "<td align='" + align + "' style='vertical-align: middle;'>" + data + "</td>";
    }

    this.getEventProviderIDs = function(pids){
        var data = '<td>';
        for(var k in pids) {
           data += "<div><small>" + k + "-" + pids[k] + "</small></div>";
        }
        data += '</td>';
        return data;
    }

    this.getEventScore = function(e){
        return "<td align='center' style='vertical-align: middle;'>" + (e.Tr1OR || "?") + " - " + (e.Tr2OR || "?") + "</td>";
    }

    data = data.Stages;
    var table = $("#event-list-table");
    var cur_table_body = $("#event-list-table")[0].firstElementChild;
    var new_table_body = document.createElement("tbody");

    var static_url = window.api_config["static-data-base-url"] + "/low/";

    data.forEach(stage => {
        var stage_live_count = 0;
        var fp_tmp = [];
        stage.Events.forEach(event => {
            if(event.Epr == "1" || event.Epr == 1){
                stage_live_count++;
            }
        });
        for(var k in api_data.Stages[0]._FP) {
           fp_tmp.push(k + " : " + api_data.Stages[0]._FP[k]);
        }
        var fp = fp_tmp.join("</br>");
        new_table_body.innerHTML +=
            "<tr data-type='stage' data-live-count='" + stage_live_count + "'>" +
                "<td colspan='6'>" +
                    "<div class='d-flex justify-content-between'>" +
                        "<div>" +
                            "<b>" + stage.Cnm + "</b> " +
                            "<small class='text-muted'>(" + stage.Cid + ")</small> " +
                            "<b>/ " + stage.Snm + "</b> " +
                            "<small class='text-muted'>(" + stage.Sid + ")</small> " +
                        "</div>" +
                        "<div>" +
                            "<button type='button' class='btn btn-secondary' data-toggle='tooltip' data-placement='left' data-html='true' title='" + fp + "'>FP</button>" +
                        "</div>" +
                    "</div>" +
                "</td>" +
            "</tr>";
        stage.Events.forEach(event => {
            new_table_body.innerHTML +=
                "<tr data-type='event' data-epr='" + event.Epr + "'>"
                    + this.getEventStartDateCol(event.Esd)
                    + this.getEventStatusText(event.Eps)
                    + this.getEventProviderIDs(event.Pids)
                    + this.getEventParticipant(event.T1, "left")
                    + this.getEventScore(event)
                    + this.getEventParticipant(event.T2, "right")
                + "</tr>";
        })
    })
    cur_table_body.remove();
    table.append(new_table_body);
    if($("#live-only button")[0].attributes['aria-pressed'].value == "true"){
        toggleLiveEvents();
    }

}