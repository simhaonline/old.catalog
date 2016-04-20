// Open New
{% if perms.catalog.change_pricetype %}
$("body").delegate("[data-do='open-new-pricetype']", "click", function(){

	model_name = 'pricetype';

	$('#modal-edit-' + model_name + '-header').text('Добавить тип данных параметров');

	$('#edit-' + model_name + '-id').val('0');
	$('#edit-' + model_name + '-name').val('');
	$('#edit-' + model_name + '-alias').val('');
	$('#edit-' + model_name + '-multiplier').val('1.0');
	$('#edit-' + model_name + '-alias').val('');
	$('#edit-' + model_name + '-state').prop('checked', true);

	$('#modal-edit-' + model_name).foundation('reveal', 'open');

	return false;
});
{% endif %}

// Open Edit
{% if perms.catalog.change_pricetype %}
$("body").delegate("[data-do='open-edit-pricetype']", "click", function(){

	model_name = 'pricetype';

	$.post('/catalog/ajax/get/' + model_name + '/', {
		id : $(this).data(model_name + '-id'),
		csrfmiddlewaretoken : '{{ csrf_token }}'
	},
	function(data) {
		if ('success' == data.status){

			$('#modal-edit-' + model_name + '-header').text('Редактировать тип цены');

			$('#edit-' + model_name + '-id').val(data[model_name]['id']);
			$('#edit-' + model_name + '-name').val(data[model_name]['name']);
			$('#edit-' + model_name + '-alias').val(data[model_name]['alias']);
			$('#edit-' + model_name + '-multiplier').val(data[model_name]['multiplier']);
			$('#edit-' + model_name + '-state').prop('checked', data[model_name]['state']);

			$('#modal-edit-' + model_name).foundation('reveal', 'open');

		}
	}, "json");

	return false;
});
{% endif %}


// Save
{% if perms.catalog.change_pricetype %}
$("body").delegate("[data-do='edit-pricetype-save']", "click", function(){

	model_name = 'pricetype';

	$.post('/catalog/ajax/save/' + model_name + '/', {
		id         : $('#edit-' + model_name + '-id').val(),
		name       : $('#edit-' + model_name + '-name').val(),
		alias      : $('#edit-' + model_name + '-alias').val(),
		multiplier : $('#edit-' + model_name + '-multiplier').val(),
		state      : $('#edit-' + model_name + '-state').prop('checked'),
		csrfmiddlewaretoken : '{{ csrf_token }}'
	},
	function(data) {

		if ('success' == data.status){

			$('[data-' + model_name + '-name="' + data[model_name]['id'] + '"]').text(data[model_name]['name']);
			$('[data-' + model_name + '-multiplier="' + data[model_name]['id'] + '"]').text(data[model_name]['multiplier']);
			$('[data-' + model_name + '-state="' + data[model_name]['id'] + '"]').prop('checked', data[model_name]['state']);

			$('#edit-' + model_name + '-id').val('0');
			$('#edit-' + model_name + '-name').val('');
			$('#edit-' + model_name + '-alias').val('');
			$('#edit-' + model_name + '-multiplier').val('1.0');
			$('#edit-' + model_name + '-state').prop('checked', false);

			$('#modal-edit-' + model_name).foundation('reveal', 'close');
		}
	}, "json");

	return false;
});
{% endif %}


// Cancel Edit
{% if perms.catalog.change_pricetype %}
$("body").delegate("[data-do='edit-pricetype-cancel']", "click", function(){

	model_name = 'pricetype';

	$('#edit-' + model_name + '-id').val('0');
	$('#edit-' + model_name + '-name').val('');
	$('#edit-' + model_name + '-alias').val('');
	$('#edit-' + model_name + '-multiplier').val('1.0');
	$('#edit-' + model_name + '-state').prop('checked', false);

	$('#modal-edit-' + model_name).foundation('reveal', 'close');

	return false;
});
{% endif %}


// Open Delete
{% if perms.catalog.delete_pricetype %}
$("body").delegate("[data-do='open-delete-pricetype']", "click", function(){

	model_name = 'pricetype';

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
{% if perms.catalog.delete_pricetype %}
$("body").delegate("[data-do='delete-pricetype-apply']", "click", function(){

	model_name = 'pricetype';

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
{% if perms.catalog.delete_pricetype %}
$("body").delegate("[data-do='delete-pricetype-cancel']", "click", function(){

	model_name = 'pricetype';

	$('#delete-' + model_name + '-id').val(0);

	$('#modal-delete-' + model_name).foundation('reveal', 'close');

	return false;
});
{% endif %}


// Switch State
{% if perms.catalog.change_pricetype %}
$("body").delegate("[data-do='switch-pricetype-state']", "click", function(){

	model_name = 'pricetype';

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
