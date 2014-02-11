$(function(){
    console.log("document ready");
    $("#make").removeAttr('disabled');
    $("#make").on('change', function(){
        console.log($(this).attr('id') + " changed to " + $(this).val());
        $("#model").prop('disabled', false);
        $("#year").prop('disabled', true);
        $("#engine").prop('disabled', true);
    });

    $("#model").on('change', function(){
        console.log($(this).attr('id') + " changed to " + $(this).val());
        $("#year").prop('disabled', false);
        $("#engine").prop('disabled', true);
    });

    $("#year").on('change', function(){
        console.log($(this).attr('id') + " changed to " + $(this).val());
        $("#engine").prop('disabled', false);
    });

    $("#engine").on('change', function(){
        console.log($(this).attr('id') + " changed to " + $(this).val());
        $("#results").html("Boom, results for " + $("#year").val() + " " + $("#make").val() + " " + $("#model").val());
    });
});
