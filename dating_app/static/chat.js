
$(document).ready(function () {
    // if logged in get userid, else random id
    var client_id;
    if (sessionStorage.getItem('user')) {
        client_id = sessionStorage.getItem('user')
    } else {
        client_id = Date.now()
    }
    var socket = new WebSocket(`ws://localhost:8001/ws/${client_id}`);
    socket.onmessage = function (event) {
        console.log("data: ")
        console.log(event.data)
        var parent = $("#messages");
        var data = JSON.parse(event.data);
        var sender = data['sender'];
        console.log("sender = ", sender)
        if (sender == client_id)
            sender = "You";
        var message = data['message']
        var content = "<p><strong>" + sender + " </strong> <span> " + message + "</span></p>";
        parent.append(content);
    };
    $("#chat-form").on("submit", function (e) {
        e.preventDefault();
        var message = $("input").val();
        console.log("message is " + message)
        if (message) {
            data = {
                "sender": client_id,
                "message": message
            };
            socket.send(JSON.stringify(data));
            $("input").val("");
            document.cookie = 'X-Authorization=; path=/;';
        }
    });
});
