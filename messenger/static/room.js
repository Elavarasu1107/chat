const username = JSON.parse(document.getElementById('user').textContent);
const roomName = JSON.parse(document.getElementById('room-name').textContent);
let scroll = document.querySelector('.chat-area')
scroll.scrollTop = scroll.scrollHeight


const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    let listTag = document.createElement('li')
    let pTag = document.createElement('p')
    pTag.textContent = data.message
    if(data.username == username){
        listTag.className = 'send'
        pTag.className = 'send-text'
    }
    else{
        listTag.className = 'replies'
        pTag.className = 'reply-text'
    }
    listTag.appendChild(pTag)
    document.querySelector('#chat-log').appendChild(listTag)
    scroll.scrollTop = scroll.scrollHeight
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) { 
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'username': username,
        'room_name': roomName
    }));
    messageInputDom.value = '';
};