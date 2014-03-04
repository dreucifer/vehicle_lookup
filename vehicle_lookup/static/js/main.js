function unload_list(dom) {
    $(dom).html(
            "<option val='-1' selected>Select a " + $(dom).attr("id") + "</option>"
            );
    $(dom).prop("disabled", true);
}

function load_list(dom, params) {
    $.post( "http://127.0.0.1:5000/vl" + dom, params, 'json')
        .done(function( response ) {
            var obj = $.parseJSON(response);
            $.each( obj.data, function( i, item) {
                $("#"+dom).append("<option>"+item+"</option>");
            });
            $("#"+dom).prop("disabled", false);
        })
        .fail(function() {
            alert("Failed");
        });
}

function get_vehicle(params) {
    $.post( "http://127.0.0.1:5000/vl", params, 'json')
        .done(function( response ) {
            var obj = $.parseJSON(response);
            get_parts("#results", {guid: obj.data[0]});
        })
        .fail(function() {
            alert("FUCK");
        });
}

function get_parts(dom, params) {
    $.getJSON( "http://127.0.0.1:5000/pt?callback=?", params)
        .done(function( response ) {
            if (response['status'] == 'Success') {
                $(dom).html("<table class='table table-striped' id='parts'><thead><th>Part Name</th></thead></table>")
                $.each( response['data'], function(key, val){
                    $(dom).children('#parts').append(
                        '<tr><td><a href="' + val['url'] + '">' + val['name'] + '</a></td></tr>');
                });
            }
        })
        .fail(function() {
            alert("Failed");
        });
}

$(function(){
    console.log("document ready");

    unload_list("#make");
    unload_list("#type");
    unload_list("#model");
    unload_list("#year");
    unload_list("#engine");

    load_list("make", {});
    $("#make").prop("disabled", false);
    $("#make").on("change", function(){
        console.log($(this).attr("id") + " changed to " + $(this).val());
        unload_list("#type");
        load_list("type", {
            make: $(this).val()});
        unload_list("model");
        unload_list("year");
        unload_list("engine");
    });

    $("#type").on("change", function(){
        console.log($(this).attr("id") + " changed to " + $(this).val());
        unload_list("#model");
        load_list("#model", {
            make: $('#make').val(),
            type: $(this).val()});
        unload_list("#year");
        unload_list("#engine");
    });

    $("#model").on("change", function(){
        console.log($(this).attr("id") + " changed to " + $(this).val());
        unload_list("#year");
        load_list("#year", {
            make: $("#make").val(),
            type: $("#type").val(),
            model: $(this).val()});
        unload_list("#engine");
    });

    $("#year").on("change", function(){
        console.log($(this).attr("id") + " changed to " + $(this).val());
        unload_list("#engine");
        load_list("#engine", {
            make: $("#make").val(),
            type: $("#type").val(),
            model: $("#model").val(),
            year: $(this).val()});
    });

    $("#engine").on("change", function(){
        console.log($(this).attr("id") + " changed to " + $(this).val());
        get_vehicle({
            make: $("#make").val(),
            type: $("#type").val(),
            model: $("#model").val(),
            year: $("#year").val(),
            engine: $(this).val()});
    });
});
