function wallpad_open_onClick() {
    Swal.fire({
        title: 'Wallpad 열기', // 제목 설정
        text: 'Wallpad를 열까요?', // 내용 설정
        icon: 'question', // 아이콘 설정 (info, success, warning, error)
        showCancelButton: true, // 취소 버튼 표시 여부
        confirmButtonText: '열기', // 확인 버튼 텍스트 설정
        cancelButtonText: '취소', // 취소 버튼 텍스트 설정
    }).then((result) => {
        if (result.isConfirmed) {
            // '열기'를 클릭했을 때
            console.log("OPEN!!");
            socket.emit('ret_wallpad_open');
        } else {
            // '취소'를 클릭했을 때 또는 대화상자가 닫혔을 때 수행할 작업 추가 가능
            console.log('Wallpad 열기가 취소되었습니다.');
        }
    });

    // // 확인 대화상자 표시
    // var confirmation = confirm("Wallpad를 열까요?");

    // // 'Yes'를 클릭했을 때
    // if (confirmation) {
    //     console.log("OPEN!!");
    //     socket.emit('ret_wallpad_open')
    // } else {
    //     // 'No'를 클릭했을 때 또는 대화상자가 닫혔을 때 수행할 작업 추가 가능
    //     console.log('Wallpad 열기가 취소되었습니다.');
    // }
}