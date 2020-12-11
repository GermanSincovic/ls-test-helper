export function CalendarInit() {

    function makeLSDate(y, m, d){
        var year = y.toString();
        var month = (m+1).toString();
        var day = d.toString();
        if(month.length == 1){
            month = "0" + month;
        }
        if(day.length == 1){
            day = "0" + day;
        }
        return year + month + day;
    }

    function Calendar(id, year, month) {
        var Dlast = new Date(year, month + 1, 0).getDate(),
            D = new Date(year, month, Dlast),
            DNlast = new Date(D.getFullYear(), D.getMonth(), Dlast).getDay(),
            DNfirst = new Date(D.getFullYear(), D.getMonth(), 1).getDay(),
            calendar = '<tr>',
            month = ["January", "February",
                "March", "April", "May",
                "June", "July", "August",
                "September", "October", "November", "December"
            ];
        if (DNfirst != 0) {
            for (var i = 1; i < DNfirst; i++) calendar += '<td>';
        } else {
            for (var i = 0; i < 6; i++) calendar += '<td>';
        }
        for (var i = 1; i <= Dlast; i++) {
            if(i == new Date().getDate() && D.getFullYear() == new Date().getFullYear() && D.getMonth() == new Date().getMonth() &&
                        i == new Date(location.date).getDate() && D.getFullYear() == new Date(location.date).getFullYear() && D.getMonth() == new Date(location.date).getMonth()){
                calendar += '<td class="today chosen">'
                            + '<a class="btn" href="'
                            + location.pathname
                            + "?sport=" + location.sport
                            + "&date=" + makeLSDate(D.getFullYear(), D.getMonth(), i) + '">' + i + '</a>'
                        + '</td>';
            } else if (i == new Date().getDate() && D.getFullYear() == new Date().getFullYear() && D.getMonth() == new Date().getMonth()) {
                calendar += '<td class="today">'
                            + '<a class="btn" href="'
                            + location.pathname
                            + "?sport=" + location.sport
                            + "&date=" + makeLSDate(D.getFullYear(), D.getMonth(), i) + '">' + i + '</a>'
                        + '</td>';
            } else if (i == new Date(location.date).getDate() && D.getFullYear() == new Date(location.date).getFullYear() && D.getMonth() == new Date(location.date).getMonth()) {
                calendar += '<td class="chosen">'
                            + '<a class="btn" href="'
                            + location.pathname
                            + "?sport=" + location.sport
                            + "&date=" + makeLSDate(D.getFullYear(), D.getMonth(), i) + '">' + i + '</a>'
                        + '</td>';
            } else {
                calendar += '<td>'
                            + '<a class="btn" href="'
                            + location.pathname
                            + "?sport=" + location.sport
                            + "&date=" + makeLSDate(D.getFullYear(), D.getMonth(), i) + '">' + i + '</a>'
                        + '</td>';
            }
            if (new Date(D.getFullYear(), D.getMonth(), i).getDay() == 0) {
                calendar += '<tr>';
            }
        }
        for (var i = DNlast; i < 7; i++) calendar += '<td>&nbsp;';
        document.querySelector('#' + id + ' tbody').innerHTML = calendar;
        document.querySelector('#' + id + ' thead td:nth-child(2)').innerHTML = month[D.getMonth()] + ' ' + D.getFullYear();
        document.querySelector('#' + id + ' thead td:nth-child(2)').dataset.month = D.getMonth();
        document.querySelector('#' + id + ' thead td:nth-child(2)').dataset.year = D.getFullYear();
        if (document.querySelectorAll('#' + id + ' tbody tr').length < 6) { // чтобы при перелистывании месяцев не "подпрыгивала" вся страница, добавляется ряд пустых клеток. Итог: всегда 6 строк для цифр
            document.querySelector('#' + id + ' tbody').innerHTML += '<tr><td>&nbsp;<td>&nbsp;<td>&nbsp;<td>&nbsp;<td>&nbsp;<td>&nbsp;<td>&nbsp;';
        }
    }
    Calendar("calendar", new Date(location.date).getFullYear(), new Date(location.date).getMonth());
    // переключатель минус месяц
    document.querySelector('#calendar thead tr:nth-child(1) td:nth-child(1)').onclick = function() {
            Calendar("calendar", document.querySelector('#calendar thead td:nth-child(2)').dataset.year, parseFloat(document.querySelector('#calendar thead td:nth-child(2)').dataset.month) - 1);
        }
        // переключатель плюс месяц
    document.querySelector('#calendar thead tr:nth-child(1) td:nth-child(3)').onclick = function() {
        Calendar("calendar", document.querySelector('#calendar thead td:nth-child(2)').dataset.year, parseFloat(document.querySelector('#calendar thead td:nth-child(2)').dataset.month) + 1);
    }
    var curDate = new Date();
    document.querySelector('#calendar-today-link').href = location.pathname + "?sport=" + location.sport + "&date=" + makeLSDate(curDate.getFullYear(), curDate.getMonth(), curDate.getDate())
}