export function MessageHandler(text){

    var container = $("#message_container");

    var message = document.createElement("div");
        message.className = "card row my-1";
        setTimeout(function(){ message.remove(); }, 3000);

    var message_content = document.createElement("div");
        message_content.className = "card-body shadow";
        message_content.innerHTML =  text;

        message.append(message_content);
        container.append(message);

}