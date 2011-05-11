$(document).keydown(function(event){
    if (event.keyCode == '71'){
        event.preventDefault();
        window.location.replace("/left");
    } else if (event.keyCode == '72'){
        window.location.replace("/right");
    }
});