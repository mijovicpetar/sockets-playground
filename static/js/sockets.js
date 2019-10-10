$(document).ready(function() {
    let socket = io('/app')
    let status_socket = io('/status')

    status_socket.on('status_subscription', function(msg, cb) {
        data = JSON.parse(msg)
        document.getElementById('number_1').value = data.number_1
        document.getElementById('number_2').value = data.number_2
    });

    socket.on('some_event_response', function(msg, cb) {
        console.log('some_event_response')
        console.log(msg)
        showResponse(msg)
    })

    $('form#emit').submit(function(event) {
        socket.emit('some_event', 'data')
        console.log('some_event emit occured.')
        return false
    })
})

function showResponse(msg) {
    document.getElementById('response_input').value = msg
}
