$(document).ready(function() {

    //hides dropdown content
    $(".size_chart").hide();

    //unhides first option content
    $("#option0").show();

    //listen to dropdown for change
    $("#language_select").change(function() {
        //rehide content on change
        $('.size_chart').hide();
        //unhides current item
        $('#' + $(this).val()).show();
    });

});