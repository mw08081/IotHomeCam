$(function () {
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

    socket.emit('get_homecam_state', {});
    socket.on('set_homecam_switch_state', function(data) {
      console.log('homecam switch state : ', data);

      const img = document.getElementById('streamHomecam');
      if(data.state) {
        $('.homecam-switch').bootstrapSwitch('state', true, true);  // 스위치를 ON 상태로 설정
        img.style.display = 'block';
        socket.emit('set_homecam_state', {'data':'on'});
      } else {
        $('.homecam-switch').bootstrapSwitch('state', false, true);  // 스위치를 Off 상태로 설정
        img.style.display = 'none';
        socket.emit('set_homecam_state', {'data':'off'});
      }
    })
    
    socket.on('ret_homecam_active', function (data) {
      console.log('homecam streaming ... ');
      // Blob URL 생성
      const blob = new Blob([data], { type: 'image/jpeg' });
      const blobURL = URL.createObjectURL(blob);
    
      // `img` 요소에 Blob URL 적용
      const img = document.getElementById('streamHomecam');
      img.src = blobURL;
      
    });
});