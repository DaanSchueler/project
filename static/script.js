// Function for like buttons
function like() {

  // Listens for click on the like button
  $(".like_button").click(function(event) {

      // Make variable to save value button
      var fired_button = $(this).val();

      // Create url endpoint
      var endpoint = "";

      //Change endpoint if button == like or unlike
      if ($(event.target).html() == 'Like') {
          endpoint = "/like"
      } else {
          endpoint = "/unlike"
      }

      //Ajax post request to respective approute 
      $.ajax({
          type: 'POST',
          url: endpoint,
          data: JSON.stringify({
              fired_button
          }, null, '\t'),
          contentType: 'application/json;charset=UTF-8',

          // If succesvol change text like button to like/unlike
          success: function() {
              if ($(event.target).html() == 'Like') {
                  $(event.target).html("Unlike");
              } else {

                  $(event.target).html("Like");
              }
          }
      });


  })
}

// Function for like buton if not logged in

function cannot() {
  $(".like_button").click(function(event) {

      document.getElementById("alert").style.display = "block";

  })
}

// Disable find user at more-info.html

$("#likerfield").change(function() {
  $('#find_user').prop('disabled', false);
});