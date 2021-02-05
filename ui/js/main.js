import {RequestManager} from './RequestManager.js'
import {Repeater} from './Repeater.js'
import {TabMemoriser} from './TabMemoriser.js'
import {MessageHandler} from './MessageHandler.js'
import {ToggleSpinner} from './ToggleSpinner.js'

const RM = new RequestManager();
	RM.getHealthPage();
	RM.getFiles();
	RM.prepareLoggerControlPanel();

new Repeater( () => {RM.getHealthPage()}, 30000 );

$("#main_form_submit").on("click", function(){
    ToggleSpinner();
	RM.runCollector($("#main_form")); 
});

$("#files-uploader-form").change(function(){
    ToggleSpinner();
	RM.uploadFile($("#files-uploader-form"));
});

$("#kafka-producer-form").on("submit", function(){
    RM.produceToKafka($("#kafka-producer-form"));
})

new Repeater( () => {RM.getFiles()}, 5000 );

new TabMemoriser("#pills-tab", "last-nav-tab");
