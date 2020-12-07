export function PAPILiveCount(data){

    data = data.Sports;

    for (var k in data){
        $("[data-sport-id='" + k + "']").text(data[k]);
    }

}