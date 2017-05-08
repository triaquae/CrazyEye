/**
 * Created by alex on 12/12/16.
 */


function PopUpWindow(src) {
    //console.log("pop up src", src);
    popname =window.open(src,'','width=800,height=700');
    popname.window.focus();


}


function popupCallback(str,obj_id,obj_name,column_name){
    //alert("This is callback:" + str);
    //console.log("popup callback ",str,obj_id,obj_name,model_name)
    var target_ele = $("#id_"+column_name);
    target_ele.append("<option value='"+ obj_id +"' selected>"+ obj_name +"</option>" );
    //console.log(target_ele.children())

}