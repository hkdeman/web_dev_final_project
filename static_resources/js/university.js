var university;
var choosingTeachers = false;
var global_school;

$(document).ready(function() {
    var str = window.location.href;
    var n = str.lastIndexOf('/');
    university = Number(str.substring(n + 1));
    $("#rateYo").rateYo({
      rating: parseFloat($('.rating').text()),
      readOnly: true
    });
});

$(".school").click(function() {
    var temp = $(this).text();
    global_school = temp;
    query_info(temp);
});

function query_info(school) {

    var what = "query-subjects";
    var class_type = "course";

    if (choosingTeachers) {
        what = "query-teachers";
        class_type = "teacher"
    }

    if (window.matchMedia('(max-width: 800px)').matches) {
        $('.pick-from-here').css({
            'display': 'unset',
            'margin-top':'2%',
        });
    }

        $.post('/school-details',{ 
            university: university,
            school:school,
            what:what,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },function(data) {
            data = data.info;
            $('.pick-course').empty();
            var htmlstr="";
            for (var i in data) {
                htmlstr +='<button class="btn btn-teal full '+class_type+'"><h3>'+data[i]+'</h3></button>';
            }
            $('.pick-course').append(htmlstr);            
            $('.pick-course').css({
                'max-height':'500px',
                'overflow-y':'scroll',
                'overflow-wrap':'break-word',
            });

            $('.pick-course button').css({
                'white-space':'normal'
            });

            $('.'+class_type).click(function() {
                if($(this).text()=="") {
                    return;
                }

                if (choosingTeachers) {
                    teacher = $(this).text();
                    $.post('/school-details',{ 
                        university: university,
                        school:school,
                        teacher:teacher,
                        what:"teacher-selected",
                        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
                    },function(data) {
                        window.location.replace("/review-teacher/"+data.id);
                    });
                } else {
                    course = $(this).text();
                    $.post('/school-details',{ 
                        university: university,
                        school:school,
                        course:course,
                        what:"course-selected",
                        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
                    },function(data) {
                        window.location.replace("/review-course/"+data.id);
                    });
                }
                
        });

    });
}

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
            what:"university",
            university: university,
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


$(".rateYo").each(function() {
	var item = $(this);
    item.rateYo({
		rating: item.data('id')
    });
});


function initMap() {
    var lat = parseFloat($('.map-lat').val());
    var lng = parseFloat($('.map-lng').val());
    var zoom = 16;
    if(lat == 0.0) {
        zoom = 4;
        lat = 51.5074;
        lng = 0.1278;
    }
    var uluru = {lat: lat, lng: lng};
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: zoom,
        center: uluru
    });
    var marker = new google.maps.Marker({
        position: uluru,
        map: map
    });
}


$('.btn-view-more').click(function() {
    location.href = "/review-uni/"+university;
});


$("#toggle-teacher-course").change(function() {
    if($(this).prop('checked')) {
        $(".type").empty().append("Teacher");
        choosingTeachers = true;
    } else {
        $(".type").empty().append("Course");   
        choosingTeachers = false;
    }

    query_info(global_school);
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

