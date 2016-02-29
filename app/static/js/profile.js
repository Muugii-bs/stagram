$(document).ready(function() {
	user = $('#user-name').text();
	display_photos(user);
	$('#prof_pic').click(function () {
		$('#avatarModal').modal('show'); 
	});

	$(document).on('click', '#upload_link', function () {
		$('#photoModal').modal('show');
	});

	$('#my-photo').click(function () {
		$(this).removeClass("btn-default").addClass("btn-primary");
		$('#favorites').removeClass("btn-primary").addClass("btn-default");
		$('#friends').removeClass("btn-primary").addClass("btn-default");
		$('#photo-gallery').removeClass("hidden");
	});

	$('#favorites').click(function () {
		$(this).removeClass("btn-default").addClass("btn-primary");
		$('#my-photo').removeClass("btn-primary").addClass("btn-default");
		$('#friends').removeClass("btn-primary").addClass("btn-default");
		$('#photo-gallery').addClass("hidden");
	});

	$('#friends').click(function () {
		$(this).removeClass("btn-default").addClass("btn-primary");
		$('#favorites').removeClass("btn-primary").addClass("btn-default");
		$('#my-photo').removeClass("btn-primary").addClass("btn-default");
		$('#photo-gallery').addClass("hidden");
	});

	function display_photos(user) {
		$('.photos').remove();
		var container = '<div class="container hidden" id="photo-gallery">'
					  + '<div class="row">'
					  + '<div class="col-lg-12">'
					  + '<h1 class="page-header">My gallery'
					  + '<small>&nbsp;&nbsp;<a href="#" id="upload_link">upload photo</a></small>'
					  + '</h1></div></div>'
		var photos = [];
		$.ajax({
			url: '/photos',
			type: 'post',
			data: {user: user},
			dataType: 'json'
		}).done(function(data) {
			if(data.error == '') {
				photos = data.photos;
				var cnt = 0;
				var row = '<div class="row">'
				console.log(photos);
				for(i = 0; i < photos.length; i++) {
					cnt ++;
					var block = '<div class="col-md-4 portfolio-item">'
						    	+ '<a href="#"><img class="img-responsive" src="'
								+ photos[i]
								+ '" alt=""></a><h3><a href="#">Project Name</a></h3>'
								+ '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam viverra euismod odio, gravida pellentesque urna varius vitae.</p> </div>'
					row += block;
					if(cnt == 3 || i == photos.length - 1) {
						container = container + row + '</div>'
						var row = '<div class="row">'
						cnt = 0;
					}	
				}
				container += '</div>'
				$('#content').append(container);
			}
		}).fail(function(){
			alert('AJAX error');
		});
	}
});
