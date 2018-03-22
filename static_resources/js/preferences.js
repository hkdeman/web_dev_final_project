$('.save-review-text').hide();
$('.delete-review-text').hide();
$('.preferences-info-details').show();
$('.preferences-info-reviews').hide();
$('.preferences-info-settings').hide();

$('.btn-preferences-info-details').click(function(){
    $('.preferences-info-title').empty();
    $('.preferences-info-title').append("Details");    
    $('.preferences-info-details').show();
    $('.preferences-info-reviews').hide();
    $('.preferences-info-settings').hide();
});



$('.btn-preferences-info-reviews').click(function() {
    $('.preferences-info-title').empty();
    $('.preferences-info-title').append("Reviews"); 
    $('.preferences-info-details').hide();
    $('.preferences-info-reviews').show();
    $('.preferences-info-settings').hide();
});

$('.btn-preferences-info-settings').click(function() {
    $('.preferences-info-title').empty();
    $('.preferences-info-title').append("Settings"); 
    $('.preferences-info-details').hide();
    $('.preferences-info-reviews').hide();
    $('.preferences-info-settings').show();
});




$(".rateYo").each(function() {
	var item = $(this);
    item.rateYo({
		rating: item.data('id'),
    });
});

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

$('.edit').click(function() {
    var id = $(this).data('id');
    var elem = $("."+id+'-review');
    if(elem.attr("contenteditable")=="false") {
        elem.attr("contenteditable","true");
        $(this).addClass("edited");
        $("#"+id+"-rating").rateYo("option", "readOnly", false);
        $('.'+id+'-save').show();
        $('.'+id+'-delete').show();        
    }
});

$('.save-review-text').click(function() {
    var id = $(this).data("id");
    var elem = $('.'+id+'-review');
    elem.attr("contenteditable","false");
    $("."+id+"edit").removeClass("edited");
    $("#"+id+"-rating").rateYo("option", "readOnly", true);
    $(this).hide();
    $('.'+id+'-delete').hide();    
    
    var review = $("."+id+"-review").text();
    var rating = Math.round($("#"+id+"-rating").rateYo("option", "rating"));
    $.post('/update-review',{
        what:"update",        
        id:id,
        review:review,
        rating:rating,
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


$('.delete-review-text').click(function() {
    var id = $(this).data("id");
    swal({
        title: "Are you sure?",
        text: "Once deleted, you will not be able to recover your review",
        icon: "warning",
        buttons: true,
        dangerMode: true,
      })
      .then((willDelete) => {
        if (willDelete) {

            $.post('/update-review',{
                what:"delete",
                id:id,
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
            },function(data) {
                    swal("Your review has been deleted!", {
                        icon: "success",
                    }).then((value) => {
                        $('.review-'+id+'-div').remove();                            
                    });
                }
            );

        } else {
            swal("Your review is fine!");
          }
        });
});





$('.delete-account').click(function(){
    swal({
        title: "Are you sure?",
        text: "Once deleted, you will not be able to recover your account",
        icon: "warning",
        buttons: true,
        dangerMode: true,
      })
      .then((willDelete) => {
        if (willDelete) {
        
            $.post('/preferences',{
                what:"delete-account",
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
            },function(data) {
                swal("Your account has been deleted. You will be directed soon!", {
                    icon: "success",
                  }).then((value) => {
                    location.href="/";      
                  });
                }
            );
            
        } else {
          swal("Your account is fine!");
        }
      });
});


$('.save-details').click(function() {
    var first_name = $('.input-first-name').val();
    var last_name = $('.input-last-name').val();
    
    $.post('/preferences',{
        what:"update-details",
        first_name:first_name,
        last_name:last_name,
        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
    },function(data) {
        swal("Your details have been saved!", {
            icon: "success",
          }).then((value) => {
            location.reload();              
          });
        }
    );
});