var socket;
$(document).ready(function(){
    socket = io.connect('http://localhost:5000/test');
    socket.on('my response', function(msg) {
        console.log(msg);
    });
    $('form#emit').submit(function(event) {
        socket.emit('my event', {data: $('#emit_data').val()});
        return false;
    });
    $('form#broadcast').submit(function(event) {
        socket.emit('my broadcast event', {data: $('#broadcast_data').val()});
        return false;
    });
});