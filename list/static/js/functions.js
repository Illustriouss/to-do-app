$('.item').on('click', '.js-check-item', (e) => {
	let pk = $(e.currentTarget.closest('.item')).attr('id').replace('item-', '');

	$.ajax({
		url: '/toggle_done/',
		data: {'pk': pk},
	}).done(function(response) {
		$("#item-"+response['pk']).toggleClass('item--checked');
		$('.js-checked').text('Done ' + response['nrChecked']);
	});
});

$('.item').on('click', '.js-remove-item', (e) => {
	let pk = $(e.currentTarget.closest('.item')).attr('id').replace('item-', '');
	
	$.ajax({
		url: '/remove_item/',
		data: {'pk': pk},
	}).done(function(response) {
		$("#item-"+response['pk']).remove();
	});
})
 
$('.lists').on('click', '.js-remove-list', (e) => {
	let pk = $(e.currentTarget.closest('.list--selector')).attr('id').replace('list-', '');

	$.ajax({
		url: '/remove_list/',
		data: {'pk': pk},
	}).done(function(response) {
		$('#list-'+response['pk']).remove();
	});
})

$('#new-item-form').submit(function(e) {
	e.preventDefault();
	$.ajax({
		url: '/add_item/',
		data: $(this).serialize(),
		type: 'POST'
	}).done(function(response) {
		if (response['committed']) {
			$('.list').append("<div>an item was added, please refresh</div>");
		}
		$('.box').slideToggle();
		$('#new-item-form').trigger("reset");

	});
})

$('.js-form-list input').keypress(function(e){
	if(e.keyCode == 13){
		$('#new-list-form').submit(function(e) {
			e.preventDefault();
			$.ajax({
				url: '/add_list/',
				data: $(this).serialize(),
				type: 'POST'
			}).done(function(response) {
				if (response['committed']) {
					console.log(response['pk']);
					console.log(response['slug']);
					console.log(response['title']);
					
					let new_list = 
					"<div class='list--selector' id='list-" + response['pk'] + "'>" + 
						"<a href='/list/" + response['pk'] +"/" + response['slug'] + "'>" + response['title'] + "</a>" + 
						"<span class='list--remove js-remove-list'><i class='fa fa-times fa-fw' aria-hidden='true'></i></span>" + 
                    "</div>"

					$('.lists').append(new_list);
				}
				$('.js-form-list').hide();
				$('#new-list-form').trigger("reset");
			});
		});
	}
});

$('.js-add-list').on('click', () => {
	$('.js-form-list').show();
	$('.js-form-list input').focus();
});

$('.js-add-item').on('click', () => {
	$('.box').slideToggle();
	$('.js-add-item i').toggleClass('rotated', 500);
});

let placeholder_vals = [
	'What to do?',
	'Where?',
	'before when? (yyyy-mm-dd)'
]

$('#new-item-form').find("input[type=text]").each(function(key, val) {
	$(this).attr("placeholder", placeholder_vals[key]);
});

$('.js-change-title').on('click', () => {
	$('.js-change-title').hide();
	$('.js-change-title-input').show().val($('.js-change-title').text()).focus();
});

$('.js-change-title-input').keypress(function(e) {
	if (e.keyCode == 13) {
		pk = $('.js-change-title').attr('id').replace('list-', '');
		new_title = $('.js-change-title-input').val();
		$.ajax({
			url: '/update_title/',
			data: {
				'pk': pk,
				'new_title': new_title
			},
		}).done(function(response) {
			if (response['committed']) {
				$('.js-change-title').text($('.js-change-title-input').val()).show();
				$('.js-change-title-input').hide();
				$('#list-' + response['pk']).text($('.js-change-title-input').val());
			}
		});
	}
})
