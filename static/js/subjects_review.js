var rating=Math.floor(Math.random() * 5) + 1;
var course;
$(document).ready(function() {
    var str = window.location.href;
    var n = str.lastIndexOf('/');
    course = Number(str.substring(n + 1));
});

$('.btn-add-comment').click(function() {
    var textarea_styling= "<textarea id='text' style='width:100%;height:200px;padding:2%;font-family: 'Abel', sans-serif; \
     line-height: 25px;border: solid 1px #ddd;'></textarea>";
    swal({
        title: "Add Your Honest Opinion",
        text: textarea_styling,
        html: true,
        showCancelButton: true,
        closeOnConfirm: false,
        showLoaderOnConfirm: true,
        animation: "slide-from-top",
      }, function() {
        var review = document.getElementById('text').value;
        $.post('/add-review', {
            what:"course",            
            course: course,
            review: review,
            rating: rating,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
			location.reload()
        },function(data) {
            if (data == "Error") {
                swal("Error!", "The review could not be added", "error");
            }
        });
    });
});