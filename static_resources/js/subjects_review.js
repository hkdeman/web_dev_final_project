var course;
$(document).ready(function() {
    var str = window.location.href;
    var n = str.lastIndexOf('/');
    course = Number(str.substring(n + 1));
});

$('.btn-save-teacher').hide();


$('.btn-add-comment').click(function() {
    var textarea_styling= "<textarea id='text' style='width:100%;height:200px;padding:2%;font-family: 'Abel', sans-serif; \
     line-height: 25px;border: solid 1px #ddd;'></textarea><br>\
     <span> Add a rating </span> <br>\
     <label class='radio-inline'><input type='radio' name='rateRadio' value='1'>1</label>\
    <label class='radio-inline'><input type='radio' name='rateRadio' value='2'>2</label>\
    <label class='radio-inline'><input type='radio' name='rateRadio' value='3'>3</label>\
    <label class='radio-inline'><input type='radio' name='rateRadio' value='4'>4</label>\
    <label class='radio-inline'><input type='radio' name='rateRadio' value='5'>5</label>";

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

        var rating = Number($("input[name='rateRadio']:checked").val());

        $.post('/add-review', {
            what:"course",
            course: course,
            review: review,
            rating: rating,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            },function(data) {            
            if (data == "Success") {
                swal.close();
                location.reload();
            } else {
                swal("Error!", "The review could not be added", "error");                
            }
        }, location.reload());
    });
});



$('.teacher-list-name').click(function() {
    $('.btn-save-teacher').show();
    var name = $(this).text();
    $('.selected-teacher').empty().append(name);
});

$('.btn-save-teacher').click(function(){
    var name = $('.selected-teacher').text();
    $.post('/review-course/'+course, {
        what:"update-teacher",
        teacher: name,
        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
        },function(data) {            
        if (data == "Success") {
            swal("Submitted!", "Your request has been submitted! Our team will look into it ASAP!", "success");                            
        } else if (data=="Exists") {
            swal("Exists", "You cannot add two requests for a subject! Please wait for your last request to be resolved!", "error");                
        } else {
            swal("Error!", "The review could not be added", "error");                            
        }
    });
})