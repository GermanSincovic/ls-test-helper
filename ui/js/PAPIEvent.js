export function PAPIEvent(data){

    this.LSDateGetYear = function(ls_date){
        return ls_date.toString().substr(0,4);
    }

    this.LSDateGetMonth = function(ls_date){
        return ls_date.toString().substr(4,2)
    }

    this.LSDateGetMonthText = function(month_n){
        var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        return months[month_n];
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

    this.getEventStartTimeCol = function(esd){
        return this.LSDateGetHours(esd) + ":" + this.LSDateGetMinutes(esd);
    }

    this.getEventISOStartDateTime = function(ls_date){
        return new Date(
            this.LSDateGetYear(ls_date) + "-" +
            this.LSDateGetMonth(ls_date) + "-" +
            this.LSDateGetDay(ls_date) + "T" +
            this.LSDateGetHours(ls_date) + ":" +
            this.LSDateGetMinutes(ls_date) + ":" +
            this.LSDateGetSeconds(ls_date)
        )
    }

    this.getEventStartDateTime = function(ls_date){
        var date = this.getEventISOStartDateTime(ls_date);
        var trimmed_date =
            date.getDate() + " " +
            this.LSDateGetMonthText(date.getMonth()) + " " +
            date.getFullYear() + ", " +
            this.LSDateGetHours(ls_date) + ":" +
            this.LSDateGetMinutes(ls_date)
        return trimmed_date;
    }

    $("#event-data").html(data);
    var esd = $("[data-type='startdatetime']");
        esd[0].innerText = this.getEventStartDateTime(esd[0].dataset.value)

}