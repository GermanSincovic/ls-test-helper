export function TabMemoriser(container_id, name_in_storage){
	// $(window).load(function(){
		if(localStorage.getItem(name_in_storage)){
		    $('#' + localStorage.getItem(name_in_storage)).trigger("click");
		}

	// });

	$(container_id).on('click', function (e) {
	    if(e.target.nodeName === "A"){
	        localStorage.setItem(name_in_storage, e.target.id);
	    }
	});
}