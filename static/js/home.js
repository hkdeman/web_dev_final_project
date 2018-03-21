var university = "";
var school = "";

$('.university').click(function() {
    $('.pick-field').empty();
    $('.pick-subject').empty();
    if($(this).text()=="") {
        return;
    }
    university = $(this).text();
    $.post('/uni-details',{
        university: university,
        what:"query-schools",
        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
    },function(data) {
        window.location.replace("/university/"+data.id);
    });
});


$(".search-bar-uni").on('input',function(){
    var text = $(this).val();
    $('.university').each(function(i,obj) {
        if($(this).text().indexOf(text) == -1) {
            $(this).hide();
        } else {
            $(this).show();
        }
    });
});