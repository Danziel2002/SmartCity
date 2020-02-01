$("#test").click(function(){
    $.ajax({
        url : '/getTransport?vehicleId=' + document.getElementById('transportId').value,
        success : function(data){
                $("#transportItems").html($('#transportItems').html() + ' ' +data['vehicle'])
        }})
});

