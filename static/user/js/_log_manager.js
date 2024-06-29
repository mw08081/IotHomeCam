function log_refresh_btn_onClick() {
    console.log("log_refresh_btn_onClick")

    socket.emit('ret_log_refresh')
}

$(function () {
    console.log("refresh log.html")

    //로그 받는 이벤트 함수 만들고
    socket.on('get_log_data', function(data) {
        const pTag = document.getElementById('log_area');

        pTag.innerText = data;
    });

    //로그 보내라고 하기(로그 전송 함수 실행)
    socket.emit('ret_log_refresh');
});