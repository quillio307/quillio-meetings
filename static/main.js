var socket;
$(document).ready(function(){
    var url =window.location.href;
    var args =url.split('/');

    var user = args[args.length-2];
    var room = args[args.length-1];

    var mic_toggle = false;
    $("#mic").click(function () {

        $("#mic").attr('style', '');
        mic_toggle = true;
        socket.emit('silenceAll', {room: room, user: user})
    });

    $("#start").click(function () {
        socket.emit('start', {room: room, user: user})
    });
    $("#end").click(function () {
        socket.emit('end', {room: room, user: user})
    });
    socket = io.connect('http://localhost:5000/meetings');

    socket.on('receivemsg', function(msg) {
        console.log(msg);
        msglog(msg.data);
    });

    socket.emit('join', {
        user_id: user,
        room_id: room
    });

    socket.on('silence', function () {
        console.log("Received silence command.");
        mic_toggle = !mic_toggle;
        $("#mic").attr('style', 'background:gray;');
    });

    socket.on('startMeeting', function () {
        msglog("Meeting Started");
    });
    socket.on('endMeeting', function () {
        msglog("Meeting Ended");
    });

    var msglog = function(txt) {
        $('ul#msgboard').append('<li>'+ txt +'</li>');
    };

});