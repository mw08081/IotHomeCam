function wallpad_open_onClick() {
    Swal.fire({
        title: 'Wallpad 열기', 
        text: 'Wallpad를 열까요?', 
        icon: 'question', 
        showCancelButton: true, 
        confirmButtonText: '열기', 
        cancelButtonText: '취소', 
    }).then((result) => {
        if (result.isConfirmed) {
            // '열기'를 클릭했을 때
            console.log("OPEN!!");
            socket.emit('ret_wallpad_open');
        } else {
            // '취소'
            console.log('Wallpad 열기가 취소되었습니다.');
        }
    });
}