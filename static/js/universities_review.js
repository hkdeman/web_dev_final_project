
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
