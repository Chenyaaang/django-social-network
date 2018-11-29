//global page：update new post, update new comment, add comment
function write_html(username, time, content, id, picture){
    var html = "<div class='timeline-item' date-is=' " + time + " ' id='message_"+ id + "'>" +
                                    "<div class='w3-container w3-cell' style='width:80%'>" +
                                        "<a href='/profile/"+ username +"' id='a_underscore'>" + username + "</a> &nbsp;&nbsp;" +
                                            content + "</div>" +
                                    "<div class='w3-container w3-cell' style='width:20%'>" +
                                        "<button class='comment_button' id='show_comment_button_" + id +"'>" + "show comments" + "</button>" + "</div>" +
                                    "<div class='comment' id='show_comment_" + id +"'>" +
                                        "<div class='w3-container w3-cell' id='comment_left'>" +
                                        "<img class='comment_img' src='../static/" + picture + "'>" +"</div>" +
                                    "<div class='w3-container w3-cell' id='comment_middle'>" +
                                        "<input name='comment' class='add_comment' id='write_comment_for_message_" + id + "' type='text' placeholder='say something'>" +
                                    "<div class='w3-container w3-cell' id='comment_right'>" +
                                        "<button class = 'write_comment_btn' id='write_comment_btn_" + id + "'> post </button>" + "</div>" +
                                      "<div class='show_comments' id='comments_for_message_" + id + "'>" + "</div>" +
                                    "</div>"+
                                "</div>";
     return html;
}



function global_messagelist(){
    console.log("function");
    $.get("/get_global_message/")
      .done(function(data){
        console.log("data ready");
//        global-message-list
        var list = $("#global-message-list");
        list.data('max_time', data['max_time']);

        list.html("");
        var picture = data.picture;
//        console.log(picture);
        if(!picture)
            picture = "photo_id/default.png";
//            console.log("no picture");
        for(var i = 0; i < data.messages.length; i++)
        {
            message = data.messages[i];
            var time = message['last_changed'];
            var content = message['content'];
            var username = message['username'];
            var new_message = $(write_html(username, time, content, message.id, picture));
            new_message.data("message-id", message.id);
            list.append(new_message);
        }
        if(data.messages.length > 0){
          $(".comment_button").click(show_comments);
          $(".write_comment_btn").click(post_comments_btn);
        }
        


      })

}

function getUpdates(){
    console.log("get_Updates");
    var list = $("#global-message-list")
    var max_time = list.data("max_time")

    $.get("/get_changes_global/" + max_time)
      .done(function(data){
          list.data('max_time', data['max_time']);
          var picture = data.picture;
          for(var i = 0; i < data.messages.length; i++){
              var message = data.messages[i];
              if(message.deleted)
                  $("#message_" + message.id).remove();
              else{
                  var time = message['last_changed'];
                  var content = message['content'];
                  var username = message['username'];
                  var new_message = $(write_html(username, time, content, message.id, picture));
                  console.log("new_message");
                  new_message.data("message-id", message.id);
                  list.prepend(new_message);
              }

          }
          if(data.messages.length > 0){
            $(".comment_button").click(show_comments);
            $(".write_comment_btn").click(post_comments_btn);
        }

      });
}
$(document).ready(function(){

    global_messagelist();
    window.setInterval(getUpdates,5000);
    // CSRF set-up copied from Django docs
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