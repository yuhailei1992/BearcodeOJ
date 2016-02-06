function populateList() {
    $.get("/code_challenge/add_comment")
      .done(function(data) {
          var list = $("#comments");
          list.data('max-entry', data['max-entry']);
          list.html('')
          for (var i = 0; i < data.items.length; i++) {
              item = data.items[i];
              var new_item = $(item.html);
              new_item.data("post_id", item.id);
              list.append(new_item);
          }
      });
}

function startComment(event) {
  var post_id = $(event.delegateTarget).parent().attr('data-comment')
  var startComment_url="/get_comments"

  if ($("div[name='post" + post_id + "comments']").length != 0)
    return;

  $.ajax({
    url: startComment_url,
    dataType: "json",
    method: "GET",
    data: {post_id:post_id}
  })
  .done(function(resp) {
    //console.log(getComment);
    var size = resp['size']
    var comments = resp['comments']

    var targetOl = $("ol[post-id="+post_id+"]")
    var text_area_html = "<textarea rows='2' name='comment-field' class=\"W_input\" action-type=\"check\" style=\"line-height: 10px; font-size: 10px; width: 250px\""+
               "</textarea>"
    var div = "<div name='post" + post_id + "comments' width='60%'></div>"
    
    targetOl.append(div)
    $("div[name='post" + post_id + "comments']").append("<table width='250'></table>")

    for (i = 0; i < size; i++){
      var url = comments[i].user_photo
      var user = comments[i].comment_user
      var created_at = comments[i].created_at
      var comment_text = comments[i].comment_text

      var item_html = "<tr><td><img src='" + url + "' width='20'><small><b>" + user + "</b></small></td>" 
      + "</tr><tr><td><b>&nbsp;&nbsp;Says:&nbsp;</b>" + comment_text + "</td></tr><tr><td><p style='font-size:8px'>&nbsp;&nbsp;&nbsp;&nbsp;On&nbsp;&nbsp;" + created_at + "</p10></td></tr>"
      $("div[name='post" + post_id + "comments'] table").append(item_html)
    }
    targetOl.append(text_area_html)

    targetOl.children("textarea").keyup(function (e) {
      if (e.which == 13) addComment(post_id, $(e.delegateTarget).val())
    });
  });
}

function addSingleComment(post_id, comment){
  var url = comment.user_photo
  var user = comment.comment_user
  var created_at = comment.created_at
  var comment_text = comment.comment_text
  var item_html = "<tr><td><img src='" + url + "' width='20'><small><b>" + user + "</b></small></td>" 
      + "</tr><tr><td><b>&nbsp;&nbsp;Says:&nbsp;</b>" + comment_text + "</td></tr><tr><td><p style='font-size:8px'>&nbsp;&nbsp;&nbsp;&nbsp;On&nbsp;&nbsp;" + created_at + "</p10></td></tr>"
      $("div[name='post" + post_id + "comments'] table").append(item_html)

  var targetOl = $("ol[post-id="+post_id+"]")
  targetOl.children("textarea").remove()

  targetOl.children("textarea").keyup(function (e) {
    if (e.which == 13) addComment(post_id, $(e.delegateTarget).val())
  });
}

function addComment(post_id, text) {
  var addcomment_url = "/add_comment"
  var text_area_html = "<textarea rows='2' name='comment-field' class=\"W_input\" action-type=\"check\" style=\"line-height: 10px; font-size: 10px; width: 250px\""+
               "</textarea>"
  $.ajax({
    url: addcomment_url,
    dataType: "json",
    method: "get",
    data: {post_id:post_id, new_comment:text}
  })
  .done(function(comment) {
    #console.log(comment);
    // get the targeted ol with specific post and comment
    var targetOl = $("ol[post-id="+post_id+"]")
    targetOl.children("textarea").remove()

    addSingleComment(post_id, comment)
    targetOl.append(text_area_html)

    targetOl.children("textarea").keyup(function (e) {
      if (e.which == 13) addComment(post_id, $(e.delegateTarget).val())
    });
  });
}

function getUpdates() {
    var list = $("#comments")
    var max_entry = list.data("max-entry")
    $.get("shared-todo-list/get-changes/"+ max_entry)
      .done(function(data) {
          list.data('max-entry', data['max-entry']);
          for (var i = 0; i < data.items.length; i++) {
              var item = data.items[i];
              if (item.deleted) {
                  $("#item_" + item.id).remove();
              } else {
                  var new_item = $(item.html);
                  new_item.data("post-id", item.id);
                  list.append(new_item);
              }
          }
      });
}

$(document).ready(function () {
  // Add event-handlers
  $("[name=add-btn]").click(startComment);
  $("#comment").click(deleteItem);

  // Set up to-do list with initial DB items and DOM data
  populateList();
  $("#comment-field").focus();

  // Periodically refresh list
  window.setInterval(getUpdates, 5000);

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

//window.setInterval(getUpdates, 5000);