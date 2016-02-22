$(document).ready(function() {
	$('#prof_pic').click(function () {
		$('#myModal').modal('show'); 
	});

	$('#my-photo').click(function () {
		$('#favorites').removeClass("btn-primary").addClass("btn-default");
		$('#friends').removeClass("btn-primary").addClass("btn-default");
		user = $('#user-name').text();
		display_photos($(this), user);
	});

	$('#favorites').click(function () {
		$(this).removeClass("btn-default").addClass("btn-primary");
		$('#my-photo').removeClass("btn-primary").addClass("btn-default");
		$('#friends').removeClass("btn-primary").addClass("btn-default");
	});

	$('#friends').click(function () {
		$(this).removeClass("btn-default").addClass("btn-primary");
		$('#favorites').removeClass("btn-primary").addClass("btn-default");
		$('#my-photo').removeClass("btn-primary").addClass("btn-default");
	});

	function display_photos(button, user) {
		$.ajax({
			url: '/photos',
			type: 'post',
			data: {user: user},
			dataType: 'json'
		}).done(function(data){
			console.log(data);
		}).fail(function(){
			alert('AJAX error');
		});
		$('.container').remove();
		var container = '<div class="container">'
					  + '<div class="row">'
					  + '<div class="col-lg-12">'
					  + '<h1 class="page-header">Photo'
					  + '<small>&nbsp;&nbsp;gallery</small>'
					  + '</h1></div></div></div>'
		if(!button.hasClass("btn-primary")) {
			$('#content').append(container);
			button.removeClass("btn-default").addClass("btn-primary");
		}
	}
});
