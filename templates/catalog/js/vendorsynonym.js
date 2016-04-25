{% if perms.catalog.add_vendorsynonym or perms.catalog.change_vendorsynonym or perms.catalog.delete_vendorsynonym %}
$("body").delegate("[data-do='filter-vendorsynonyms']", "change", function(){
	location.href = "/catalog/vendorsynonyms/" + $("#filter-updater").val() + "/" + $("#filter-distributor").val() + "/" + $("#filter-vendor").val() + "/";
	return true;
});
{% endif %}


{% if perms.catalog.add_vendorsynonym %}
$("body").delegate("[data-do='open-new-vendorsynonym']", "click", function(){

	model = 'vendorsynonym';

	$('#modal-edit-' + model + '-header').text('Добавить синоним производителя');

	$('#edit-' + model + '-id').val('0');
	$('#edit-' + model + '-name').val('');
	$('#edit-' + model + '-updater').val('0');
	$('#edit-' + model + '-distributor').val('0');
	$('#edit-' + model + '-vendor').val('0');

	$('#modal-edit-' + model).foundation('reveal', 'open');

	return false;
});
{% endif %}


{% if perms.catalog.change_vendorsynonym %}
$("body").delegate("[data-do='open-edit-vendorsynonym']", "click", function(){

	model = 'vendorsynonym';

	$.post('/catalog/ajax/get/' + model + '/', {
		id : $(this).data(model + '-id'),
		csrfmiddlewaretoken : '{{ csrf_token }}'
	},
	function(data) {
		if ('success' == data.status){

			$('#modal-edit-' + model + '-header').text('Редактировать синоним производителя');

			$('#edit-' + model + '-id').val(data[model]['id']);
			$('#edit-' + model + '-name').val(data[model]['name'])
			if (data[model]['updater']) {
				$('#edit-' + model + '-updater').val(data[model]['updater']['id']);
			} else {
				$('#edit-' + model + '-updater').val(0);
			}
			if (data[model]['distributor']) {
				$('#edit-' + model + '-distributor').val(data[model]['distributor']['id']);
			} else {
				$('#edit-' + model + '-distributor').val(0);
			}
			if (data[model]['vendor']) {
				$('#edit-' + model + '-vendor').val(data[model]['vendor']['id']);
			} else {
				$('#edit-' + model + '-vendor').val(0);
			}

			$('#modal-edit-' + model).foundation('reveal', 'open');
		}
	}, "json");
	return false;
});
{% endif %}


{% if perms.catalog.change_vendorsynonym %}
$("body").delegate("[data-do='edit-vendorsynonym-save']", "click", function(){

	model = 'vendorsynonym';

	$.post('/catalog/ajax/save/' + model + '/', {
		id             : $('#edit-' + model + '-id').val(),
		name           : $('#edit-' + model + '-name').val(),
		updater_id     : $('#edit-' + model + '-updater').val(),
		distributor_id : $('#edit-' + model + '-distributor').val(),
		vendor_id      : $('#edit-' + model + '-vendor').val(),
		csrfmiddlewaretoken : '{{ csrf_token }}'
	},
	function(data) {

		if ('success' == data.status){

			$('[data-' + model + '-name="' + data[model]['id'] + '"]').text(data[model]['name']);

			if (data[model]['updater']) {
				$('[data-' + model + '-updater-name="' + data[model]['id'] + '"]').text(data[model]['updater']['name']);
				$('[data-' + model + '-updater-name="' + data[model]['id'] + '"]').data('updater-id', data[model]['updater']['id']);
				$('[data-' + model + '-updater-name="' + data[model]['id'] + '"]').data('updater-name', data[model]['updater']['id']);
			} else {
				$('[data-' + model + '-updater-name="' + data[model]['id'] + '"]').text('');
				$('[data-' + model + '-updater-name="' + data[model]['id'] + '"]').data('updater-id', '0');
				$('[data-' + model + '-updater-name="' + data[model]['id'] + '"]').data('updater-name', '0');
			}

			if (data[model]['distributor']) {
				$('[data-' + model + '-distributor-name="' + data[model]['id'] + '"]').text(data[model]['distributor']['name']);
				$('[data-' + model + '-distributor-name="' + data[model]['id'] + '"]').data('distributor-id', data[model]['distributor']['id']);
				$('[data-' + model + '-distributor-name="' + data[model]['id'] + '"]').data('distributor-name', data[model]['distributor']['id']);
			} else {
				$('[data-' + model + '-distributor-name="' + data[model]['id'] + '"]').text('');
				$('[data-' + model + '-distributor-name="' + data[model]['id'] + '"]').data('distributor-id', '0');
				$('[data-' + model + '-distributor-name="' + data[model]['id'] + '"]').data('distributor-name', '0');
			}

			if (data[model]['vendor']) {
				$('[data-' + model + '-vendor-name="' + data[model]['id'] + '"]').text(data[model]['vendor']['name']);
				$('[data-' + model + '-vendor-name="' + data[model]['id'] + '"]').data('vendor-id', data[model]['vendor']['id']);
				$('[data-' + model + '-vendor-name="' + data[model]['id'] + '"]').data('vendor-name', data[model]['vendor']['id']);
			} else {
				$('[data-' + model + '-vendor-name="' + data[model]['id'] + '"]').text('');
				$('[data-' + model + '-vendor-name="' + data[model]['id'] + '"]').data('vendor-id', '0');
				$('[data-' + model + '-vendor-name="' + data[model]['id'] + '"]').data('vendor-name', '0');
			}

			$('#edit-' + model + '-id').val('0');
			$('#edit-' + model + '-name').val('');
			$('#edit-' + model + '-updater').val('0');
			$('#edit-' + model + '-distributor').val('0');
			$('#edit-' + model + '-vendor').val('0');

			$('#modal-edit-' + model).foundation('reveal', 'close');
		}
	}, "json");

	return false;
});
{% endif %}


{% if perms.catalog.change_vendorsynonym %}
$("body").delegate("[data-do='edit-vendorsynonym-cancel']", "click", function(){

	model = 'vendorsynonym';


	$('#edit-' + model + '-id').val('0');
	$('#edit-' + model + '-name').val('');
	$('#edit-' + model + '-updater').val('0');
	$('#edit-' + model + '-distributor').val('0');
	$('#edit-' + model + '-category').val('0');

	$('#modal-edit-' + model).foundation('reveal', 'close');

	return false;
});
{% endif %}


{% if perms.catalog.delete_vendorsynonym %}
$("body").delegate("[data-do='open-delete-vendorsynonym']", "click", function(){

	model = 'vendorsynonym';

	$.post('/catalog/ajax/get/' + model + '/', {
		id : $(this).data(model + '-id'),
		csrfmiddlewaretoken : '{{ csrf_token }}'
	},
	function(data) {
		if ('success' == data.status){

			$('#delete-' + model + '-id').val(data[model]['id']);
			$('#delete-' + model + '-name').text(data[model]['name'])

			$('#modal-delete-' + model).foundation('reveal', 'open');
		}
	}, "json");

	return false;
});
{% endif %}


{% if perms.catalog.delete_vendorsynonym %}
$("body").delegate("[data-do='delete-vendorsynonym-apply']", "click", function(){

	model = 'vendorsynonym';

	$.post('/catalog/ajax/delete/' + model + '/', {
		id : $('#delete-' + model + '-id').val(),
		csrfmiddlewaretoken : '{{ csrf_token }}'
	},
	function(data) {
		if ('success' == data.status) {

			$('[data-' + model + '="' + data['id'] + '"]').empty();

			$('#modal-delete-' + model).foundation('reveal', 'close');
		}
	}, "json");

	return false;
});
{% endif %}


{% if perms.catalog.delete_vendorsynonym %}
$("body").delegate("[data-do='delete-vendorsynonym-cancel']", "click", function(){

	model = 'vendorsynonym';

	$('#delete-' + model + '-id').val(0);

	$('#modal-delete-' + model).foundation('reveal', 'close');

	return false;
});
{% endif %}


{% if perms.catalog.change_vendorsynonym %}
$("body").delegate("[data-do='link-vendorsynonym-same-vendor']", "click", function(){

	model = 'vendorsynonym';
	foreign = 'vendor';

	$.post('/catalog/ajax/link/' + model + '/same/' + foreign + '/', {
		id : $(this).data(model + '-id'),
		csrfmiddlewaretoken : '{{ csrf_token }}'
	},
	function(data) {
		if ('success' == data.status) {

			$('[data-vendorsynonym-vendor-name="' + data[model]['id'] + '"]').text(data[model]['vendor']['name']);
			$('[data-vendorsynonym-vendor-name="' + data[model]['id'] + '"]').data('vendor-id', data[model]['vendor']['id']);
			$('[data-vendorsynonym-vendor-name="' + data[model]['id'] + '"]').data('vendor-name', data[model]['vendor']['id']);

			// TODO Обновляем список производителей в окне редактирования синонимов
		}
	}, "json");
	return false;
});
{% endif %}