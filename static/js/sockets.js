$(document).ready(function() {
    let socket = io('/app')
    let status_socket = io('/status')

    status_socket.on('status_subscription', function(msg, cb) {
        data = JSON.parse(msg)
        document.getElementById('number_1').value = data.number_1
        document.getElementById('number_2').value = data.number_2
        stopAnimation()
    });

    socket.on('some_event_response', function(msg, cb) {
        console.log('some_event_response')
        console.log(msg)
        showResponse(msg)
        stopAnimation()
    })

    socket.on('some_event_response2', function(msg, cb) {
        console.log('some_event_response')
        console.log(msg)
        showResponse(msg)
        stopAnimation()
    })

    $('form#emit').submit(function(event) {
        startAnimation()
        socket.emit('some_event', 'data')
        console.log('some_event emit occured.')
        return false
    })

    $('form#emit2').submit(function(event) {
        startAnimation()
        socket.emit('some_event2', 'data')
        console.log('some_event2 emit occured.')
        return false
    })
})

function showResponse(msg) {
    document.getElementById('response_input').value = msg
}

function startAnimation() {
    $('#loading').removeClass('hidden');
}

function stopAnimation() {
    $('#loading').addClass('hidden');
}
