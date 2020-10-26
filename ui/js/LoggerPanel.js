export function LoggerPanel(config){

	function renderAdditionalFields(){
		var arr = config[$("#component_selector").val()].endpoints[$("#endpoint_selector").val()].fields;
		$("#dynamic_input").empty();
		$.each(arr, function(item){
			var input = document.createElement('input');
				input.className = "form-control";
				input.type = arr[item].type;
				input.name = arr[item].name;
				input.placeholder = arr[item].placeholder;
				input.required = true;
			$("#dynamic_input").append(input);
		});
	}	

	$.each(config, function(item){
		$("#component_selector").append("<option value=\"" + item + "\">" + config[item].name + "</option>");
	});

	if($("#component_selector").val() == null){
		$("#endpoint_selector").hide();
	}

	$("#component_selector").on("change", function(){
		if($("#component_selector").val() != null){
			$("#endpoint_selector").show();
		}
		var arr = config[this.value].endpoints;
		$("#endpoint_selector").empty();
		$.each(arr, function(item){
			$("#endpoint_selector").append("<option value=\"" + item + "\">" + arr[item].name + "</option>");
			renderAdditionalFields();
		});
	});

	$("#endpoint_selector").on("change", function(){
		renderAdditionalFields();
	});

}