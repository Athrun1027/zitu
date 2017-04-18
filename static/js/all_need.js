// 验证码框
$("#id_captcha_1").addClass('form-control');
// 刷新验证码
$('.captcha').on('click', function(){
    $.getJSON("/refresh",
        function (result) {
            $('.captcha').attr('src', result['image_url']);
            $('#id_captcha_0').val(result['key'])
    });
});