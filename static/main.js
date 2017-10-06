var socket;
$(document).ready(function(){
    var mic_toggle = false;
    $("#mic").click(function () {
        if(mic_toggle){
            $("#mic").attr('style', 'background:gray;');
        }else{
            $("#mic").attr('style', '');
        }
        mic_toggle = !mic_toggle;
    });

    var url =window.location.href;
    var args =url.split('/');
    socket = io.connect('http://localhost:5000/meetings');
    var user = args[args.length-2];
    var room = args[args.length-1];
    console.log(user);
    console.log(room);
    socket.on('receivemsg', function(msg) {
        console.log(msg);
        $('ul#msgboard').append('<li>'+ msg.data +'</li>');
    });

    socket.emit('join', {
        user_id: user,
        room_id: room
    });

});