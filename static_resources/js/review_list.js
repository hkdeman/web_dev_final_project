$('.like').click(function(){
    id = $(this).data('id');
    var elem = $(this);
    $.post('/like',{ 
        id:id,
        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
    },function(data) {
        liked_before = Number(elem.attr('title').split(" ")[0]);        
            if(data.what=="like") {
                liked_before+=1;
                elem.addClass(" liked");
            } else if (data.what=="unlike"){
                liked_before-=1
                elem.removeClass(" liked");
            }
            elem.attr('title',liked_before+" have liked this");
        }
    );
});

$(".rateYo").each(function() {
	var item = $(this);
    item.rateYo({
		rating: item.data('id')
    });
});
