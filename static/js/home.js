$('.university').click(function() {
    $.post('/home-details',{ 
        university: $(this).text(),
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
        })

    });
});

