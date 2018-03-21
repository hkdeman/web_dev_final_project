$('.like').click(function(){
    username = $(this).data('username');
    id = $(this).data('id');
    var elem = $(this);
    $.post('/like',{ 
        username: username,
        id:id,
        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
    },function(data) {
        console.log(data);
            if(data.what=="like") {
                elem.addClass(" liked");
            } else if (data.what=="unlike"){
                elem.removeClass(" liked");
            }
        }
    );
});

$(".rateYo").each(function() {
	var item = $(this);
    item.rateYo({
		rating: item.data('id')
    });
});
