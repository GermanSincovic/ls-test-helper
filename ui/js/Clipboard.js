function Clipboard() {
    console.log("Here");
    $(".clipboard").on("click", function(){
        const el = document.createElement('textarea');
        el.value = this.dataset.text;
        document.body.appendChild(el);
        el.select();
        document.execCommand('copy');
        document.body.removeChild(el);
        console.log("Copied");
    });
}