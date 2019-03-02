//var min_forms = parseInt($('#id_form-MIN_NUM_FORMS').val());
//var max_forms = parseInt($('#id_form-MAX_NUM_FORMS').val());

function get_total_forms() {
    return $('#id_form-TOTAL_FORMS');
}

function updateElementIndex(el, ndx) {
    var id_regex = new RegExp('(form-\\d+)');
    var replacement = 'form-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function add_form(selector) {
    var newElement = $(selector).clone(true);
    var total = parseInt(get_total_forms().val());
    console.log('newElement: ' + newElement);
    newElement.find(':input').not(':button').each(function() {
        console.log('this: '+$(this))
        console.log('name: ' + $(this).attr('name'))
        var name = $(this).attr('name').replace('-' + (total-1) + '-', '-' + total + '-');
        console.log('New name: ' + name);
        var id = 'id_' + name;
        console.log('New id: ' + id);
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    total++;
    get_total_forms().val(total);
    $(selector).after(newElement);
    var conditionRow = $('.form-row:not(:last)');
    conditionRow.find('.btn.add-form-row')
    .removeClass('btn-success').addClass('btn-danger')
    .removeClass('add-form-row').addClass('remove-form-row')
    .html('-');
    return false;
}

function delete_form(btn) {
    var total = parseInt(get_total_forms().val());
    if (total > 1){
        btn.closest('.form-row').remove();
        var forms = $('.form-row');
        get_total_forms().val(forms.length);
        for (var i = 0, formCount = forms.length; i < formCount; i++) {
            $(forms.get(i)).find(':input').each(function() {
                updateElementIndex(this, i);
            });
        }
    }
    return false;
}

$(document).on('click', '.add-form-row', function(e) {
    e.preventDefault();
    add_form('.form-row:last');
    return false;
});

$(document).on('click', '.remove-form-row', function(e){
    e.preventDefault();
    delete_form($(this));
    return false;
});