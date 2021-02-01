import {RequestManager} from './RequestManager.js'
import {TabMemoriser} from './TabMemoriser.js'
import {ToggleSpinner} from './ToggleSpinner.js'
import {MessageHandler} from './MessageHandler.js'

export function FileManager(data){

	const RM = new RequestManager();

	var header_container = "pills-file-system";
	var body_container = "pills-tab-file-system";

	header_container = document.getElementById(header_container);
	body_container = document.getElementById(body_container);

	header_container.innerHTML = "";
	body_container.innerHTML = "";

	data.forEach( el => {
		var nav_item = document.createElement("li");
			nav_item.className = "nav-item";
			nav_item.setAttribute("role", "presentation");

		var nav_item_link = document.createElement("a");
			nav_item_link.id = "pills-" + el.folder + "-tab";
			nav_item_link.className = "nav-link";
			nav_item_link.dataset.toggle = "pill";
			nav_item_link.href = "#pills-" + el.folder;
			nav_item_link.setAttribute("role", "tab");
			nav_item_link.setAttribute("aria-controls", "pills-" + el.folder);
			nav_item_link.setAttribute("aria-selected", "false");
			nav_item_link.innerText = el.folder;

			nav_item.append(nav_item_link);
			header_container.append(nav_item);
	});

	data.forEach( el => {
		var current_timestamp = +new Date();
		var body_item = document.createElement("div");
			body_item.id = "pills-" + el.folder;
			body_item.className = "tab-pane";
			body_item.setAttribute("role", "tabpanel");
			body_item.setAttribute("aria-labelledby", "pills-" + el.folder + "-tab");

			var files_container = document.createElement("div");
			el.files.sort((a, b) => { return b.created - a.created; });
			el.files.forEach(file => {
				var p = document.createElement("p");
					if(file.created*1000 > current_timestamp - 5000){
						p.className = "list-group-item new";
					} else {
						p.className = "list-group-item";
					}
					p.style.padding = 0;
					p.style.margin = 0;

				var main_link = document.createElement("a");
//					main_link.href = "#";
//					main_link.onclick = function (){ ToggleSpinner(); RM.readFile(el.folder, file.name); }
					main_link.href = "/ui/collector/" + el.folder + "/" + file.name;
					main_link.target = "_blank";
					main_link.innerText = file.name;
				p.append(main_link);

				var descr = document.createElement("span");
					descr.className = "text-muted";
					if(file.size > 0){
						descr.innerHTML = " (Size: " + new Intl.NumberFormat('ru-RU').format(file.size) + " B, Created: " + new Date(file.created*1000).toLocaleString() + ")";
					} else {
						descr.innerHTML = " (<b>Size: " + new Intl.NumberFormat('ru-RU').format(file.size) + " B</b>, Created: " + new Date(file.created*1000).toLocaleString() + ")";
					}
				p.append(descr);
				
				if(file.size > 52428800){
					var separate_link = document.createElement("a");
						separate_link.className = "btn btn-light";
						separate_link.href = "#";
						separate_link.onclick = function (){ RM.separateFile(el.folder, file.name, function(){RM.getFiles();}) }
						separate_link.innerHTML = "<img src='/ui/img/separate_icon.png' width='15'>";
					p.append(separate_link);
				}

				if(el.folder == "results"){
					var move_link = document.createElement("a");
						move_link.className = "btn btn-light";
						move_link.href = "#";
						move_link.onclick = function (){ RM.moveFile(el.folder, "archive", file.name, function(){RM.getFiles();}); }
						move_link.innerHTML = "<img src='/ui/img/archive_icon.png' width='15'>";
					p.append(move_link);
				}

				var remove_link = document.createElement("a");
					remove_link.className = "btn btn-light";
					remove_link.href = "#";
					remove_link.onclick = function(){ if(confirm("Are you sure?")){RM.removeFile(el.folder, file.name, function(){RM.getFiles();})} }
					remove_link.innerHTML = "<img src='/ui/img/delete_icon.png' width='15'>";
				p.append(remove_link);

				files_container.append(p);
			
			});

			body_item.append(files_container);
			body_container.append(body_item);

	});

	new TabMemoriser("#pills-file-system", "last-file-system-folder");

}