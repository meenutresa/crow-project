$(document).ready(function() {
 $('#userPanel').hover(function() {
    $("#userDrop").css('display','block');
 }, function(){
    $("#userDrop").css('display','none');
 });
  
 $('a.closep').click(function() {
    $("#blur").css('display','none');
    $("#login_pop").css('display','none');
    $("#signup_pop").css('display','none');
 });
 
 $('#blur').click(function() {
    $("#blur").css('display','none');
    $("#login_pop").css('display','none');
    $("#signup_pop").css('display','none');
 });
 
 
  
});
