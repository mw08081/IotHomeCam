$(function () {
  
    //새로고침하면 그냥 한번 껏다켜기
    socket.emit('set_homecam_state', {'data' : 'off'});
    socket.emit('set_homecam_state', {'data' : 'on'});
    
    socket.on('ret_homecam_active', function (data) {
      console.log('homecam streaming ... ');

      // Binary data to base64
      const base64String = btoa(
          new Uint8Array(data).reduce((data, byte) => data + String.fromCharCode(byte), '')
      );

      // Data URL 생성
      const imgElement = document.getElementById('streamHomecam');
      imgElement.src = `data:image/jpeg;base64,${base64String}`;
    });
});