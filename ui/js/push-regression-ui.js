import {RequestManager} from './RequestManager.js'

var RM = new RequestManager();
RM.getRegressionData()

$("#regression-form").on('submit', function(){
    RM.runPushRegression(this.env.value, this.spid.value, this.eid.value);
})