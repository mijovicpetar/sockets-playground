$(document).ready(function() {
    let socket = io('/app')

    // setTimeout(function(){
    //     let eventSource = new EventSource("/stream")

    //     eventSource.onmessage = function(e) {
    //         data = JSON.parse(e.data)
    //         document.getElementById('number_1').value = data.number_1
    //         document.getElementById('number_2').value = data.number_2
    //     }
    // }, 3000);

    socket.on('some_event_response', function(msg, cb) {
        console.log('some_event_response')
        console.log(msg)
        showResponse(msg)
    })

    socket.on('subscription_event_response', function(msg, cb) {
        console.log('subscription_event_response')
        console.log(msg)
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
