var socket;
$(document).ready(function(){
    socket = io.connect('http://localhost:5000/meetings');
    var user;
    var room;
    socket.on('receivemsg', function(msg) {
        console.log(msg);
        $('ul').append('<li>'+ msg.data +'</li>');
    });
    $( "#chatBut" ).click(function() {
        socket.emit('sendmsg', {
            username: user,
            room: room,
            data: $("#chat" ).val()
        });
    });
    $( "#roomBut" ).click(function() {
        room = $("#room" ).val();
        user = $("#user" ).val();
        socket.emit('join', {
            username: user,
            room: room
        });
        console.log("Join emitted.");
    });

});