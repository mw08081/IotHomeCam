function log_refresh_btn_onClick() {
    console.log("log_refresh_btn_onClick")

    socket.emit('ret_log_refresh')
}

$(function () {
    console.log("refresh log.html")

    socket.emit('ret_log_refresh');
});