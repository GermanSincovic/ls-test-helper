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
        return this.LSDateGetHours(esd) + ":" + this.LSDateGetMinutes(esd);
    }

    $("#event-list-table").html(data);
    var tds = $("[data-type='startdatetime']");
    for(var i = 0; i < tds.length; i++){
        tds[i].innerText = this.getEventStartDateCol(tds[i].dataset.value)
    }
    $("small[data-type='event-link']").each((k, v) => {
        var composite_id = v.innerHTML;
        var provider_id = composite_id.split('-')[0];
        var event_id = composite_id.split('-').slice(1).join('-');
            v.innerHTML = '<a target="_blank" href="' + location.origin
            + '/ui/public-api/' + location.environment + '/event'
            + '?sport=' + location.sport
            + '&pid=' + provider_id
            + '&id=' + event_id
            + '">' + composite_id + '</a>'
    });

    if($("#live-only button")[0].attributes['aria-pressed'].value == "true"){
        toggleLiveEvents();
    }
    if($("#frozen-only button")[0].attributes['aria-pressed'].value == "true"){
        toggleFrozenEvents();
    }

}