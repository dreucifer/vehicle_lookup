function unload_list(dom) {
    $(dom).html(
            "<option val='#' selected>Select a " + $(dom).attr("id") + "</option>"
            );
    $(dom).prop("disabled", true);
}

function load_list(dom, params) {
    $.getJSON( "http://127.0.0.1:5000/vl/?callback=?", params)
        .done(function( data ) {
            $.each( data, function( i, item) {
                $(dom).append("<option>"+item+"</option>");
            });
            $(dom).prop("disabled", false);
        })
        .fail(function() {
            alert("Failed");
        });
}

$(function(){
    console.log("document ready");

    unload_list("#make");
    unload_list("#model");
    unload_list("#year");
    unload_list("#engine");

    load_list("#make", {});
    $("#make").prop("disabled", false);
    $("#make").on("change", function(){
        console.log($(this).attr("id") + " changed to " + $(this).val());
        unload_list("#model");
        load_list("#model", {make: $(this).val()});
        unload_list("#year");
        unload_list("#engine");
    });

    $("#model").on("change", function(){
        console.log($(this).attr("id") + " changed to " + $(this).val());
        unload_list("#year");
        load_list("#year",
            {make: $("#make").val(), model: $(this).val()});
        unload_list("#engine");
    });

    $("#year").on("change", function(){
        console.log($(this).attr("id") + " changed to " + $(this).val());
        $("#engine").prop("disabled", false);
    });

    $("#engine").on("change", function(){
        console.log($(this).attr("id") + " changed to " + $(this).val());
        $("#results").html(
            "Boom, results for " + $("#year").val() + " " + $("#make").val() + " " + $("#model").val());
    });
});
