//profile post message, delete message, see new comments:

function write_html(username, time, content, id, picture){
    var html = "<div class='timeline-item' date-is=' " + time + " ' id='message_"+ id + "' >" +
                                    "<div class='w3-container w3-cell' style='width:80%'>" +
                                            content + "</div>" +
                                    "<div class='w3-container w3-cell' style='width:20%'>" +
                                        "<button class='comment_button' id='show_comment_button_" + id +"'>" + "show comments" + "</button>" + "</div>" +
                                    "<div class='comment' id='show_comment_" + id +"'>" +
                                        "<div class='w3-container w3-cell' id='comment_left'>" +
                                        "<img class='comment_img' src='/photo/" + username + "'>" +"</div>" +
                                    "<div class='w3-container w3-cell' id='comment_middle'>" +
                                        "<input name='comment' class='add_comment' id='write_comment_for_message_" + id + "' type='text' placeholder='say something'>" + "</div>" +
                                    "<div class='w3-container w3-cell' id='comment_right'>" +
                                        "<button class = 'write_comment_btn' id='write_comment_btn_" + id + "'> post </button>" + "</div>" +
                                      "<div class='show_comments' id='comments_for_message_" + id + "'>" + "</div>" +
                                    "</div>"+
                                "</div>";
     return html;
}




function profile_messagelist(){
    var profile_username = $("#profile_owner").text();
    var login_username = $("#login_username").text();
    login_username = login_username.split(" ")[1];
    $.get("/get_profile_message/" +  profile_username)
      .done(function(data){
        console.log("data")
        var list = $("#profile-message-list");
        list.data('max_time', data['max_time']);
        list.html('');
        var picture = data.picture;
        if(!picture)
            picture = "photo_id/default.png";
        for(var i = 0; i < data.messages.length; i++)
        {
            message = data.messages[i];
            var time = message['last_changed'];
            var content = message['content'];
            var username = message['username'];
            var new_message = $(write_html(username, time, content, message.id, picture))
            new_message.data("message-id", message.id);
            list.prepend(new_message);
        }
        if(data.messages.length > 0){
            $(".comment_button").click(show_comments);
            $(".write_comment_btn").click(post_comments_btn);
        }
      });
}

function postMessage(){
//    console.log("postMessage");
    var messageField = $("#message-field");
    if (messageField.val()){
         $.post("/post_message/", {"message": messageField.val()})
          .done(function(data){
              getUpdates();
              messageField.val("").focus();
          });
    }

}

/*function deleteMessage(e){
    console.log("delete");
    var id = $(e.target).parent().parent().data("message-id");

    console.log(id);
    $.post("/delete_message/" + id)
      .done(function(data){
          getUpdates();
          $("#message-field").val("");
      });
}*/
function getUpdates(){
    console.log("get_updates");
    var profile_username = $("#profile_owner").text();
    var login_username = $("#login_username").text();
    login_username = login_username.split(" ")[1];
    var list = $("#profile-message-list")
    var max_time = list.data("max_time")
    $.get("/get_changes_profile/" + profile_username + "/" + max_time)
      .done(function(data){
          list.data('max_time', data['max_time']);
          var picture = data.picture;
          for(var i = 0; i < data.messages.length; i++){
              var message = data.messages[i];
              var time = message['last_changed'];
              var content = message['content'];
              var username = message['username'];
              var new_message = $(write_html(username, time, content, message.id, picture));
              new_message.data("message-id", message.id);
              list.prepend(new_message);
          }

          if(data.messages.length > 0){
              $(".comment_button").click(show_comments);
              $(".write_comment_btn").click(post_comments_btn);
          }
      });
}

$(document).ready(function(){
    $("#post-message-btn").click(postMessage);
    $("#message-field").keypress(function(e){if(e.which == 13) postMessage();});
    profile_messagelist();

    window.setInterval(getUpdates, 5000);
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    });
});
