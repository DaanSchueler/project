// function wantinfo(id) {
//     console.log("more info wanted")
//     $.ajax({
//         url: '/moreinfo',
//         data: {"id" : id},
//     });
// }

function like(){
    $(".like_button").click(function(event) {
 // / 1. form get value
 // / 2. Ajax call /addtodb + data=this.value()
 // / 3. addtodb vraag waarde op args.get
 // / 4. database.query

 var fired_button = $(this).val();
 var endpoint = "";
 if ($(event.target).html() == 'Like'){
   endpoint=  "/test"
 }
 else{
   endpoint = "/unlike"
 }
 $.ajax({
  type : 'POST',
  url : endpoint,
  data : JSON.stringify({fired_button}, null, '\t'),
  contentType: 'application/json;charset=UTF-8',
  success: function() 
  {
      alert("success");
      if ($(event.target).html() == 'Like'){
        $(event.target).html("Unlike");
    }
    else{

      $(event.target).html("Like");
    }
 }
 });

window.alert(fired_button);
})
}


function cannot(){
    $(".like_button").click(function(event) {
     
        window.alert("Login first")
        location.href = "/login";
       
       })
       }
    
