$(document).on('click', '.imageChat', function (e) {
    // initate chat by clicking on user profiles
    email = e.currentTarget.dataset["email"];
    console.log("click image via doc for " + email);
    client_id = sessionStorage.getItem('user')
    // call to initiate_chat returns a chat_session_id
    $.ajax({
        url: 'api/chat/initiate_chat',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({ user_initiating_id: client_id, user_receiving_id: email }),
        success: function (chat_session_id) {
            console.log("created chat chat_session_id?", chat_session_id);
            console.log("showing modal")
            $('#chatModal').modal('show')
            socket = create_socket(chat_session_id)
        }
    });
});

// user submits message, is sent to websocket
$("#chat-form").on("submit", function (e) {
    e.preventDefault();
    var message = $("#chat-input").val();
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

// create websocket (for a chat_session) and attach onmessage listener
function create_socket(chat_session_id) {
    var socket = new WebSocket(`ws://localhost:8001/ws/${chat_session_id}`);

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
    return socket
}
