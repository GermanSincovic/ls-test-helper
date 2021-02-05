import {HealthViewer} from './HealthViewer.js'
import {FileManager} from './FileManager.js'
import {LoggerPanel} from './LoggerPanel.js'
import {Comparator} from './Comparator.js'
import {MessageHandler} from './MessageHandler.js'
import {ToggleSpinner} from './ToggleSpinner.js'
import {PAPILiveCount} from './PAPILiveCount.js'
import {PAPIDaily} from './PAPIDaily.js'
import {PAPIEvent} from './PAPIEvent.js'

export function RequestManager(){

	this.BASE_API_URL = location.origin + "/";

	this.getHealthPage = function(){
		$.ajax({
			url: this.BASE_API_URL + "health-page",
			success: function(response){
				new HealthViewer(response.message);
			}
		})
	}

	this.sendHealthDelta = function(data){
	    $.ajax({
			url: "/push",
			method: "post",
			headers: { "Content-Type": "application/json" },
			data: JSON.stringify(data)
		})
	}

	this.readFile = function(folder, file_name){
	    $.ajax({
			url: this.BASE_API_URL + "files/" + folder + "/" + file_name,
			success: function(response){
			    new Comparator(response.message, file_name);
			}
		})
	}

	this.getFiles = function(){
		$.ajax({
			url: this.BASE_API_URL + "files",
			success: function(response){
				new FileManager(response.message);
			}
		})
	}

	this.prepareLoggerControlPanel = function(){
		$.ajax({
			url: this.BASE_API_URL + "config",
			success: function(response){
				new LoggerPanel(response.message);
			}
		})
	}

	this.runCollector = function(data){
		var tmp_json = data.serializeArray();
		var res_json = {additional:{}};
		for(var key in tmp_json) {
			switch (tmp_json[key].name){
				case 'dtl': if(tmp_json[key].value){
					res_json[tmp_json[key].name] = tmp_json[key].value.split(":")[0];
				} break;
				case 'component': res_json[tmp_json[key].name] = tmp_json[key].value; break;
				case 'endpoint': res_json[tmp_json[key].name] = tmp_json[key].value; break;
				default: res_json.additional[tmp_json[key].name] = tmp_json[key].value; break;
			}
		}
		$.ajax({
			url: this.BASE_API_URL + "collector/run",
			headers: { "Content-Type": "application/json" },
			method: "post",
			data: JSON.stringify(res_json),
			success: function(response){
			    ToggleSpinner();
			    MessageHandler("<b>" + response.message + "</b><br>Collection finished");
			}
		});
	}

	this.moveFile = function(old_folder, new_folder, file_name, callback=null){
		$.ajax({
			url: this.BASE_API_URL + "files/" + old_folder + "/" + file_name + "?moveto=" + new_folder,
			success: function(response){
				MessageHandler("<b>" + file_name + "</b><br>File moved to " + new_folder);
				if(callback){callback();}
			}
		})
	}

    this.removeFile = function(folder, file_name, callback=null){
        $.ajax({
            url: this.BASE_API_URL + "files/" + folder + "/" + file_name,
            method: "delete",
            success: function(response){
                MessageHandler("<b>" + file_name + "</b><br>File has been removed");
                if(callback){callback();}
            }
        })
    }

    this.separateFile = function(folder, file_name, callback=null){
        $.ajax({
            url: this.BASE_API_URL + "files/" + folder + "/" + file_name + "?separate=true",
            success: function(response){
                MessageHandler("<b>" + file_name + "</b><br>File has been separated");
                if(callback){callback();}
            }
        })
    }

    this.uploadFile = function(form){

        var formData = new FormData();
        $.each(form[0].file.files, function(i, file) {
            formData.append('file', file);
        });

        $.ajax({
            url: this.BASE_API_URL + "files/upload",
            data: formData,
            processData: false,
            contentType: false,
            type: 'POST',
            success: function(){
                MessageHandler("File has been uploaded");
                $("#files-uploader-form").trigger("reset");
                ToggleSpinner();
            },
            error: function(){
                MessageHandler("Error while uploading");
                $("#files-uploader-form").trigger("reset");
                ToggleSpinner();
            }
        });
    }

    this.produceToKafka = function(form){
        var tmp_json = form.serializeArray();
		var res_json = {};
		for(var key in tmp_json) {
            res_json[tmp_json[key].name] = tmp_json[key].value;
		}

		try{
		    JSON.parse(res_json.kafka_message);
		} catch (SyntaxError) {
            MessageHandler("Error. Message is not a valid JSON");
            return false;
		}

		$.ajax({
		    url: this.BASE_API_URL + "kafka/produce/" + res_json.kafka_env + "/" + res_json.kafka_topic + "?key=" + res_json.kafka_key,
		    method: "post",
            headers: { "Content-Type": "application/json" },
		    data: res_json.kafka_message,
		    success: function(){
		        MessageHandler("Message produced");
		    },
		    error: function(){
		        MessageHandler("Error while producing");
		    }
		})

    }

    this.getPublicAPILiveCount = function(link){
        $.ajax({
            url: link,
            success: function(res){
                new PAPILiveCount(res.message);
            },
            error: function(res){
                MessageHandler("<b>Can't get API data:</b><br>" + link, "danger");
            }
        })
    }

    this.getPublicAPIDaily = function(link){
        $.ajax({
            url: link,
            success: function(res){
                new PAPIDaily(res);
            },
            error: function(res){
                MessageHandler("<b>Can't get API data:</b><br>" + link, "danger");
            }
        })
    }

    this.getPublicAPIEvent = function(link){
        $.ajax({
            url: link,
            success: function(res){
                new PAPIEvent(res);
            },
            error: function(res){
                MessageHandler("<b>Can't get API data:</b><br>" + link, "danger");
            }
        })
    }

}