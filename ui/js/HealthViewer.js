import {TabMemoriser} from './TabMemoriser.js'
import {RequestManager} from './RequestManager.js'

export function HealthViewer(data){

    var RM = new RequestManager();

    if(localStorage.getItem("health-history") != JSON.stringify(data)){
        var delta = [];
        var old_data = JSON.parse(localStorage.getItem("health-history"))[0];
        var new_data = data[0];
        for (var env in new_data){
            for(var component in new_data[env]){
                if(new_data[env][component].version != old_data[env][component].version){
                    var text = "<b>Version changed!</b>\n"
                        + env.toUpperCase() + " - "
                        + old_data[env][component].component + " - "
                        + new_data[env][component].version;
                    RM.sendHealthDelta({"text": text});
                }
            }
        }
    }
    localStorage.setItem("health-history", JSON.stringify(data));

	function getEnvironmentCrashCount(env_data){
		var count = 0;
		env_data.forEach(c => {
			if(c.hasOwnProperty("status") && c.status == "CRASHED"){ count++; }
		}, count)
		return count;
	}

	function getTableHeaders(json){
		var tr = document.createElement("tr");
		Object.keys(json).forEach(key => {
			if(key != "status" && key != "updated"){
				var th = document.createElement("th");
					th.innerText = key;
				tr.append(th);
			}
		})
		return tr;
	}

	function getTableLines(json, env=null){
		var tr = document.createElement("tr");
		if(json.status){
			tr.className = json.status.toLowerCase();
		}
		Object.keys(json).forEach(key => {
			if(key != "status" && key != "updated"){
				var td = document.createElement("td");
				    if((env=="dev" || env=="test") && key == "version"){
				        td.innerHTML = "<a target='_blank' href='https://ls-bp-ls-g.dev-i.net/view/newVersionBuild/job/" + json['component'] + "-build/'>" + json['version'] + "</a>";
				    } else {
					    td.innerText = json[key];
				    }
				tr.append(td);
			}
		})
		return tr;
	}

	function filterLines(string){
	    $("tr:not(:contains('" + string + "'))").addClass("d-none");
	    $("tr:contains('" + string + "')").removeClass("d-none");
	}

	function getLastFilterValue(){
        return localStorage.getItem('health-filter');
	}

	function saveFilterValue(val){
        localStorage.setItem('health-filter', val);
	}

	var environment_list = [];
	var crash_count_list = [];

	var header_container = "pills-tab-monitoring-nav";
	var body_container = "pills-tab-monitoring";
	header_container = document.getElementById(header_container);
	body_container = document.getElementById(body_container);

	// clear health page
	header_container.innerHTML = "";
	body_container.innerHTML = "";

	// header + statistic
	data.forEach(el => {
		var env_name = Object.keys(el)[0];
			environment_list.push(env_name);
			crash_count_list.push(getEnvironmentCrashCount(el[env_name]));
	}, environment_list, crash_count_list)

	// rendering header
	environment_list.forEach( (env, index) =>{
		var header_item = document.createElement("li");
			header_item.className = "nav-item";
			header_item.setAttribute("role", "presentation");
			
		var header_link = document.createElement("a");
			header_link.id = "pills-" + env + "-tab";
			header_link.className = "nav-link";
			header_link.dataset.toggle = "pill";
			header_link.dataset.env = env;
			header_link.href= "#pills-" + env;
			header_link.setAttribute("role", "tab");
			header_link.setAttribute("aria-controls", "pills-" + env);
			header_link.setAttribute("aria-selected", "false");
			header_link.innerText = env.toUpperCase();

		var crash_count = crash_count_list[index];
		var header_badge = document.createElement("span");
			header_badge.className = "badge badge-pill badge-danger";
			header_badge.innerText = crash_count;

			if(crash_count > 0){
				header_link.append(header_badge);
			}
			header_item.append(header_link)
			header_container.append(header_item);
	});

	// rendering body with tables
	data.forEach(el => {
		var body_item = document.createElement("div");
			body_item.id = "pills-" + Object.keys(el)[0];
			body_item.className = "tab-pane fade";
			body_item.setAttribute("role", "tabpanel");
			body_item.setAttribute("aria-labelledby", "pills-" + Object.keys(el)[0] + "-tab");

		var table = document.createElement("table");
			table.className = "table table-sm small";
			table.dataset.env = Object.keys(el)[0];

		var thead = document.createElement("thead");
		var tbody = document.createElement("tbody");

		var components = el[Object.keys(el)[0]];
			thead.append(getTableHeaders(components[0]));

			components.forEach(component => {
				tbody.append(getTableLines(component, Object.keys(el)[0]));
			});

			table.append(thead);
			table.append(tbody);
			body_item.append(table);
				body_container.append(body_item);

	}, body_container);

    setTimeout(function(){
        $("#health-filter").val(getLastFilterValue());
        filterLines(getLastFilterValue());
    }, 100);

    $("#health-filter").on("keyup", function(){
        var string = $("#health-filter").val();
            saveFilterValue(string);
            filterLines(string);
    });


	new TabMemoriser("#pills-tab-monitoring-nav", "last-env-monitoring-nav-tab");

}