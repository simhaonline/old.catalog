// Open New
{% if perms.catalog.add_parameter %}
$("body").delegate("[data-do='open-new-parameter']", "click", function(){

	model_name = 'parameter';

	$('#modal-edit-' + model_name + '-header').text('Добавить параметр');

	$('#edit-' + model_name + '-id').val('0');
	$('#edit-' + model_name + '-name').val('');
	$('#edit-' + model_name + '-alias').val('');
	$('#edit-' + model_name + '-parametertype').val('0');
	$('#edit-' + model_name + '-order').val('0');
	$('#edit-' + model_name + '-state').prop('checked', true);

	$('#modal-edit-' + model_name).foundation('reveal', 'open');

	return false;
});
{% endif %}


// Open Edit
{% if perms.catalog.change_parameter %}
$("body").delegate("[data-do='open-edit-parameter']", "click", function(){

	model_name = 'parameter';

	$.post('/catalog/ajax/get/' + model_name + '/', {
		id : $(this).data(model_name + '-id'),
		csrfmiddlewaretoken : '{{ csrf_token }}'
	},
	function(data) {
		if ('success' == data.status){

			$('#modal-edit-' + model_name + '-header').text('Редактировать параметр');

			$('#edit-' + model_name + '-id').val(data[model_name]['id']);
			$('#edit-' + model_name + '-name').val(data[model_name]['name']);
			$('#edit-' + model_name + '-alias').val(data[model_name]['alias']);
			if (data[model_name]['parametertype']) {
				$('#edit-' + model_name + '-parametertype').val(data[model_name]['parametertype']['id']);
			} else {
				$('#edit-' + model_name + '-parametertype').val(0);
			}
			$('#edit-' + model_name + '-order').val(data[model_name]['order']);
			$('#edit-' + model_name + '-state').prop('checked', data[model_name]['state']);

			$('#modal-edit-' + model_name).foundation('reveal', 'open');
		}
	}, "json");

	return false;
});
{% endif %}


// Save
{% if perms.catalog.change_parameter %}
$("body").delegate("[data-do='edit-parameter-save']", "click", function(){

	model_name = 'parameter';

	$.post('/catalog/ajax/save/' + model_name + '/', {
		id               : $('#edit-' + model_name + '-id').val(),
		name             : $('#edit-' + model_name + '-name').val(),
		alias            : $('#edit-' + model_name + '-alias').val(),
		parametertype_id : $('#edit-' + model_name + '-parametertype').val(),
		order            : $('#edit-' + model_name + '-order').val(),
		state            : $('#edit-' + model_name + '-state').prop('checked'),
		csrfmiddlewaretoken : '{{ csrf_token }}'
	},
	function(data) {

		if ('success' == data.status){


			$('[data-' + model_name + '-name="' + data[model_name]['id'] + '"]').text(data[model_name]['name']);
			$('[data-' + model_name + '-state="' + data[model_name]['id'] + '"]').prop('checked', data[model_name]['state']);

			if (data[model_name]['parametertype']) {
				$('[data-' + model_name + '-parametertype-name="' + data[model_name]['id'] + '"]').text(data[model_name]['parametertype']['name']);
				$('[data-' + model_name + '-parametertype-name="' + data[model_name]['id'] + '"]').data('parametertype-id', data[model_name]['parametertype']['id']);
				$('[data-' + model_name + '-parametertype-name="' + data[model_name]['id'] + '"]').data('parametertype-name', data[model_name]['parametertype']['id']);
			} else {
				$('[data-' + model_name + '-parametertype-name="' + data[model_name]['id'] + '"]').text('');
				$('[data-' + model_name + '-parametertype-name="' + data[model_name]['id'] + '"]').data('parametertype-id', '0');
				$('[data-' + model_name + '-parametertype-name="' + data[model_name]['id'] + '"]').data('parametertype-name', '0');
			}

			$('#edit-' + model_name + '-id').val('0');
			$('#edit-' + model_name + '-name').val('');
			$('#edit-' + model_name + '-alias').val('');
			$('#edit-' + model_name + '-parametertype').val('');
			$('#edit-' + model_name + '-order').val('0');
			$('#edit-' + model_name + '-state').prop('checked', false);

			$('#modal-edit-' + model_name).foundation('reveal', 'close');
		}
	}, "json");

	return false;
});
{% endif %}


// Cancel Edit
{% if perms.catalog.change_parameter %}
$("body").delegate("[data-do='edit-parameter-cancel']", "click", function(){

	model_name = 'parameter';

	$('#edit-' + model_name + '-id').val('0');
	$('#edit-' + model_name + '-name').val('');
	$('#edit-' + model_name + '-alias').val('');
	$('#edit-' + model_name + '-parametertype').val('');
	$('#edit-' + model_name + '-order').val('0');
	$('#edit-' + model_name + '-state').prop('checked', false);

	$('#modal-edit-' + model_name).foundation('reveal', 'close');

	return false;
});
{% endif %}


// Open Delete
{% if perms.catalog.delete_parameter %}
$("body").delegate("[data-do='open-delete-parameter']", "click", function(){

	model_name = 'parameter';

	$.post('/catalog/ajax/get/' + model_name + '/', {
		id : $(this).data(model_name + '-id'),
		csrfmiddlewaretoken : '{{ csrf_token }}'
	},
	function(data) {
		if ('success' == data.status){

			$('#delete-' + model_name + '-id').val(data[model_name]['id']);
			$('#delete-' + model_name + '-name').text(data[model_name]['name'])

			$('#modal-delete-' + model_name).foundation('reveal', 'open');
		}
	}, "json");

	return false;
});
{% endif %}


// Delete
{% if perms.catalog.delete_parameter %}
$("body").delegate("[data-do='delete-parameter-apply']", "click", function(){

	model_name = 'parameter';

	$.post('/catalog/ajax/delete/' + model_name + '/', {
		id : $('#delete-' + model_name + '-id').val(),
		csrfmiddlewaretoken : '{{ csrf_token }}'
	},
	function(data) {
		if ('success' == data.status) {

			$('[data-' + model_name + '="' + data['id'] + '"]').empty();

			$('#modal-delete-' + model_name).foundation('reveal', 'close');
		}
	}, "json");

	return false;
});
{% endif %}


// Cancel Delete
{% if perms.catalog.delete_parameter %}
$("body").delegate("[data-do='delete-parameter-cancel']", "click", function(){

	model_name = 'parameter';

	$('#delete-' + model_name + '-id').val(0);

	$('#modal-delete-' + model_name).foundation('reveal', 'close');

	return false;
});
{% endif %}


// Switch State
{% if perms.catalog.change_parameter %}
$("body").delegate("[data-do='switch-parameter-state']", "click", function(){

	model_name = 'parameter';

	$.post('/catalog/ajax/switch-state/' + model_name + '/', {
		id    : $(this).data(model_name + '-id'),
		state : $(this).prop('checked'),
		csrfmiddlewaretoken : '{{ csrf_token }}'
	},
	function(data) {
		if ('success' == data.status) {
			return false;
		} else {
			return true;
		}
	}, "json");

	return true;
});
{% endif %}
