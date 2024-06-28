function camera_recording_start_btn_onClick() {
    Swal.fire({
        title: '녹화시작', 
        text: '10초간 녹화를 시작할까요?', 
        icon: 'question', 
        showCancelButton: true, 
        confirmButtonText: '시작', 
        cancelButtonText: '취소', 
    }).then((result) => {
        if (result.isConfirmed) {
            // '열기'를 클릭했을 때
            console.log("OPEN!!");
            socket.emit('ret_camera_recording_start');
        } else {
            // '취소'
            console.log('Wallpad 열기가 취소되었습니다.');
        }
    });
}