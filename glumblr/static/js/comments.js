function get_comments(message_id)
{
    var comment_list = $("#comments_for_message_" + message_id);
    console.log("comment_list");
    console.log(comment_list);

    $.get("/get_comments/" + message_id).done(function(data){
        comment_list.html('');

        for(var i = 0; i < data.comments.length; i++)
        {
            comment = data.comments[i];
            var picture = comment['picture'];
            var username = comment['username'];
            var content = comment['content'];
            var time = comment['time'];
            console.log(time);
            if(!picture)
                picture = "photo_id/default.png";
            var new_comment = $("<div class='timeline-item' date-is=' " + time + " ' id='message_"+ message_id + "' >" +
                                    "<div class='w3-container w3-cell' style='width:80%'>" +
                                        "<div class='w3-container w3-cell' style='width:20%'>" +
                                         "<img class='comment_img' src='/photo/" + username + "'>" +
                                         "&nbsp;&nbsp;&nbsp;" + "<a href='/profile/"+ username +"' id='a_underscore'>" + username + "</a>" + "</div>" +
                                         "<div class='w3-container w3-cell' style='width:80%'>" +
                                               content + "</div>" +
                                         "</div>" +
                                 "</div>");
            comment_list.append(new_comment);
        }
    });
}

function show_comments(){
//show_comment_
    console.log("click show_comments");
//    id="show_comment_button_"
	var message_id = $(this).attr('id').split("_")[3];
	console.log(message_id);
	var comment_place = $("#show_comment_" + message_id);
	if(comment_place.css("display") == "none")
	{
	    comment_place.show();
	    console.log("1");
	    get_comments(message_id);
	    console.log("2");

    }
    else{
        comment_place.hide();
        $("comments_for_message_"+message_id).html("");
    }

}

function post_comments_btn(){
// id='comments_for_message_'" + message.id
    console.log("post_comments_btn");
	var message_id = $(this).attr('id').split("_")[3];

	var comment_field = $("#write_comment_for_message_" + message_id);
    if(comment_field.val())
    {
        $.post("/post_comment/" + message_id,{"comment":comment_field.val()}).done(function(){
        get_comments(message_id);
		comment_field.val("");
	    });
    }


}


$(function () {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
    });

    $(".comment_button").click(show_comments);
    $(".write_comment_btn").click(post_comments_btn);
});