var university = "";
var school = "";

$('.university').click(function() {
    $('.pick-field').empty();
    $('.pick-subject').empty();
    if($(this).text()=="") {
        return;
    }
    university = $(this).text();
    $.post('/home-details',{ 
        university: university,
        what:"query-schools",
        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
    },function(data) {
        data = data.schools;
        $('.pick-field').empty();
        var htmlstr="";
        for (var i in data) {
            htmlstr +='<button class="btn btn-teal full school"><h3>'+data[i]+'</h3></button>';
        }
        $('.pick-field').append(htmlstr);            
        $('.pick-field').css({
            'max-height':'500px',
            'overflow-y':'scroll',
            'overflow-wrap':'break-word',
        });

        $('.pick-field button').css({
            'white-space':'normal'
        });
        
        $('.school').click(function() {
            if($(this).text()=="") {
                return;
            }
            school = $(this).text();    
            $.post('/home-details',{ 
                university: university,
                school:school,
                what:"query-subjects",
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
            },function(data) {
                data = data.courses;
                $('.pick-subject').empty();
                var htmlstr="";
                for (var i in data) {
                    htmlstr +='<button class="btn btn-teal full course"><h3>'+data[i]+'</h3></button>';
                }
                $('.pick-subject').append(htmlstr);            
                $('.pick-subject').css({
                    'max-height':'500px',
                    'overflow-y':'scroll',
                    'overflow-wrap':'break-word',
                });
        
                $('.pick-subject button').css({
                    'white-space':'normal'
                });

                
                $('.course').click(function() {
                    if($(this).text()=="") {
                        return;
                    }
                    course = $(this).text();
                    $.post('/home-details',{ 
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

    });
});



