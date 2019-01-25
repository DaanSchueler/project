// function wantinfo(id) {
//     console.log("more info wanted")
//     $.ajax({
//         url: '/moreinfo',
//         data: {"id" : id},
//     });
// }



$(".button").click(function() {
    // / 1. form get value
    // / 2. Ajax call /addtodb + data=this.value() 
    // / 3. addtodb vraag waarde op args.get
    // / 4. database.query
   
    var fired_button = $(this).val();
    $.ajax({
    type : 'POST',
    url : "{{url_for('test')}}",
    data : JSON.stringify({fired_button}, null, '\t'),
    contentType: 'application/json;charset=UTF-8',
   //  success:function(response){document.write(response);}
    
   
    });
   window.alert(fired_button);
   })
