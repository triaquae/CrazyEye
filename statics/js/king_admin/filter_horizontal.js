/**
 * Created by alex on 11/24/16.
 */


//run this script before submit,to make sure all chosen options all selected
function CheckSelectedOptions() {
    $("select[data-type='m2m_chosen'] option").prop("selected",true);
    RemoveDisabledAttrs();
}


function RemoveDisabledAttrs() {
    $("input").removeAttr("disabled");
    $("select").removeAttr("disabled");
}

function ChoseAllOptions(from_select_ele_id,target_select_ele_id) {
    console.log(from_select_ele_id +'--' +  target_select_ele_id);
    var from_options = $("#"+from_select_ele_id + " option");

    console.log(from_options);
    $("#" +target_select_ele_id).append(from_options);
}