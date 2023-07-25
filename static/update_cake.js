$(document).ready(function(){
    var cake_string = document.getElementById("cake_json").value;
    var cake_json = JSON.parse(cake_string);
    loadCake(cake_json);
});

function loadCake(cake){
    $("#cakenameid").val(cake.name);
    $("#cakedescrid").val(cake.description);
    $("#cakepriceid").val(cake.price);
    $("#cakeid").val(cake.id);
}

function SaveUpdates(){
    if (confirm("Do you wish to save the modifications?") == false) {
        return -1;
    }
    var my_form = document.getElementById("updateform");
    var name = my_form.name.value;
    var description = my_form.description.value;
    var price = my_form.price.value;
    var item_id = my_form.cakeitemNum.value;

    var formData = {
        id: item_id,
        name: name,
        description: description,
        price: price
    };
    
    $.ajax({
        url: '/cakes',
        type: 'PUT',
        data: formData,
        dataType: "json",
        encode: true,
        success: function(result) {
            window.location.href = '/cakes';
        }
    });
}

function cancelUpdate(){
    window.location.href = '/cakes';
}