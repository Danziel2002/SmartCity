$("#test").click(function(){
    console.log('dan')
    $.ajax({
        url : '/findName?name=' + document.getElementById('name').value,
        success : function(data){
            if(data['users'] == ''){
            $('#trueName').html("Nu e user cu acest nume")
            }
            else{
            for(var user of data['users']){
                $("#trueName").html($('#trueName').html() + ' ' +user)
        }}}
    });
});

