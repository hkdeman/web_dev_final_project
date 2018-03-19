var university;
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
    $('.type').empty().append("Subject");
    var school = $(this).text();

        $.post('/school-details',{ 
            university: university,
            school:school,
            what:"query-subjects",
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },function(data) {
            data = data.courses;
            $('.pick-course').empty();
            var htmlstr="";
            for (var i in data) {
                htmlstr +='<button class="btn btn-teal full course"><h3>'+data[i]+'</h3></button>';
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

            $('.course').click(function() {
                if($(this).text()=="") {
                    return;
                }
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
        });

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