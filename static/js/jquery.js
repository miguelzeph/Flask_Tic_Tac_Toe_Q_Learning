$(document).ready( function() {
$(".block").on('click',function(){
    var postData = {'number':321};
    $.ajax({
        type: "POST",
        url: 'http://127.0.0.1:5000/',
        data: postData ,
        contentType: "application/json",
        dataType: "json", 
        processdata: true,
        success: function (response) {
  
        },
        error: function(error){
        }
      });
  
  });

});
