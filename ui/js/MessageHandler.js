export function MessageHandler(text, status=null){

//    status can be:
//    primary, secondary, success, danger, warning, info, light, dark

    var container = $("#message_container");

    var message = document.createElement("div");
        message.className = (!status) ? "card row my-1" : "card row my-1 bg-" + status;
        setTimeout(function(){ message.remove(); }, 3000);

    var message_content = document.createElement("div");
        message_content.className = "card-body shadow";
        message_content.innerHTML =  text;

        message.append(message_content);
        container.append(message);

}