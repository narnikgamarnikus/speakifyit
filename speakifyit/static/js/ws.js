    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    socket = new WebSocket(ws_scheme + "://" + window.location.host + "/chat/");

    socket.onmessage = function(e) {
      
      data = JSON.parse(e.data)
      console.log(data)

    }

    socket.onopen = function() {
      socket.send("connect");
    }

    socket.onclose = function() {
      socket.send("disconnect");   
    }

    if (socket.readyState == WebSocket.OPEN) socket.onopen();