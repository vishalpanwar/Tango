$(document).ready(function(){
    $('#about-btn').click(function(){
        alert('You clicked the button using JQuery');
    });

    $("p").hover(function(){
        $(this).css('color','red');
    },function(){
        $(this).css('color','blue');
    });

    $('#abt-img').mouseover(function(){
        $(this).attr('src','/static/media/ntt-logo-horz.png');
    });
    $('#abt-img').mouseout(function(){
        $(this).attr('src','/static/media/ntt-logo.png');
    });

    $('#index-img').hover(function(){
        $(this).attr('src','/static/media/Hello_flip.png');
    },function(){
        $(this).attr('src','/static/media/Hello.png');
    });

    $('.index-li li').hover(function(){
        var deflt = $(this).css('background-color');
        $(this).css('background-color','#FFFDD0');
    },function(){
        $(this).css('background-color','white');
    });
});