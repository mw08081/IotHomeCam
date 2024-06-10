$(function () {
    $('.auto_switch').bootstrapSwitch();
    $('.onOff_switch').bootstrapSwitch();
    $(".onOff_switch").closest('.bootstrap-switch').addClass('hidden-switch').addClass('right_side_switch');


    // auto_switch의 상태에 따라 onOff_switch의 가시성 조정 함수
    function toggleOnOffSwitch(state = true) {
        if (state) {
        $(".onOff_switch").closest('.bootstrap-switch').addClass('hidden-switch');
        } else {
        $(".onOff_switch").closest('.bootstrap-switch').removeClass('hidden-switch');
        }
    }

    // 페이지 로드 시 초기 상태에 따라 onOff_switch 표시/숨기기
    toggleOnOffSwitch();

    // auto_switch 상태 변경 시 onOff_switch 표시/숨기기
    $('.auto_switch').on('switchChange.bootstrapSwitch', function(event, state) {
        toggleOnOffSwitch(state);
    });

});