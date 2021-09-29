$(document).ready(function() {

	var $header = $('.header');
	var $hbEl = $('html, body');
	var $body = $('body');


	// datepicker
	var $date_btn = $('.date_box .date_btn'),
	$input = $('.date_box #datepicker'),
	dp = $input.datepicker().data('datepicker');

	$date_btn.on('click', function() {
			dp.show();
			$input.focus();
	});

    // 이미지업로드 미리보기
	function readURL(input) {
		if (input.files && input.files[0]) {
			var reader = new FileReader();
                     //console.log(reader);
			reader.onload = function(e) {
				$('.image_box1').css('background-image', 'url('+e.target.result +')');
				$('.image_box1').hide();
				$('.image_box1').fadeIn(650);
			}
			reader.readAsDataURL(input.files[0]);
			$('.avatar_upload .avatar_preview').css({'z-index':'4'});
		}
	}	
       
	$("#file_up1").change(function() {
		var image = $(this).parent('.upload_wrap').find('.image_box');
		readURL(this);
	});

	function readURL2(input) {
		if (input.files && input.files[0]) {
			var reader = new FileReader();
                     //console.log(reader);
			reader.onload = function(e) {
				$('.image_box2').css('background-image', 'url('+e.target.result +')');
				$('.image_box2').hide();
				$('.image_box2').fadeIn(650);
			}
			reader.readAsDataURL(input.files[0]);
			$('.avatar_upload .avatar_preview').css({'z-index':'4'});
		}
	}	
       
	$("#file_up2").change(function() {
		var image = $(this).parent('.upload_wrap').find('.image_box');
		readURL2(this);
	});

	function readURL3(input) {
		if (input.files && input.files[0]) {
			var reader = new FileReader();
                     //console.log(reader);
			reader.onload = function(e) {
				$('.image_box3').css('background-image', 'url('+e.target.result +')');
				$('.image_box3').hide();
				$('.image_box3').fadeIn(650);
			}
			reader.readAsDataURL(input.files[0]);
			$('.avatar_upload .avatar_preview').css({'z-index':'4'});
		}
	}	
       
	$("#file_up3").change(function() {
		var image = $(this).parent('.upload_wrap').find('.image_box');
		readURL3(this);
	});


});