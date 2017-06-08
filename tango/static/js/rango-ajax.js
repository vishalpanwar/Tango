$(document).ready(function(){
    $('#likes').click(function(){
        console.log('ajax running!!!');
        var catid = $(this).attr('data-catid');
        $.ajax({
            url: '/rango/like_category/?category_id=' + catid,
            type : 'GET',

            success: function(data){
                console.log('success!!');
                $('#like_count').html(data);
                $('#likes').hide();
            },

            error: function(xhr,errmsg,err){
            console.log('failed!');
            console.log(xhr.status + '  ' + xhr.responseText);
            }


        });
    });

    $('#page li').click(function(e){
        e.preventDefault();
        page_id = $(this).children('a').attr('page_id');
        console.log(page_id);
        para_before = $(this).children('.page_views_before');
        para = $(this).children('.page_views');
        $.ajax({
            url:'/rango/goto/?page_id=' + page_id,
            type: 'GET',

            success: function(data){
                console.log('link ajax success!!!');
                para_before.hide();
                para.html('(' + data + '<strong> views </strong>)');
                console.log(data);
            },

            error: function(xhr,errmsg,err){
            console.log('failed!');
            console.log(xhr.status + '  ' + xhr.responseText);
            }
        });
    });

    $('#suggestion').keyup(function(){
        console.log('In suggestion!');
        var query = $(this).val();
        $.ajax({
            url: '/rango/suggest_category/?suggestion=' + query,
            type: 'GET',

            success:function(data){
            console.log('suggestion success!!!');
            console.log(data);
                $('#cats').html(data);
            },

            error: function(xhr,errmsg,err){
            console.log('failed!');
            console.log(xhr.status + '  ' + xhr.responseText);
            }
        });
    });
});