$(function () {
    // $('.rgb-3color-led-switch').bootstrapSwitch();
    $('.homecam-switch').bootstrapSwitch();

    // 스위치 상태 변경 이벤트 핸들러 등록
    $('.homecam-switch').on('switchChange.bootstrapSwitch', function (event, state) {
        const img = document.getElementById('streamHomecam');

        if (state) {
            console.log("스위치가 ON 상태입니다.");
            // 스위치가 켜진 상태일 때 수행할 작업
            img.style.display = 'block';
            socket.emit('set_homecam_state', {'data':'on'});
        } else {
            console.log("스위치가 OFF 상태입니다.");
            // 스위치가 꺼진 상태일 때 수행할 작업
            img.style.display = 'none';
            socket.emit('set_homecam_state', {'data':'off'});
        }
    });

    socket.on('ret_homecam_active', function (data) {
      console.log('homecam streaming ...');
      // Blob URL 생성
      const blob = new Blob([data], { type: 'image/jpeg' });
      const blobURL = URL.createObjectURL(blob);
    
      // `img` 요소에 Blob URL 적용
      const img = document.getElementById('streamHomecam');
      img.src = blobURL;
      
    });
});