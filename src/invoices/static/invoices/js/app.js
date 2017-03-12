
$(document).ready(function () {
    var template = $('#invoice_item').html();
    var data = {
        quantity:'',
        name:'',
        measure:'',
        discount:'',
        total: '',
        unit_price: '',
    };
    $.tmpl(template, data).appendTo('#invoice_items');

    $('#invoice_items').find('input').on('keydown', function (event) {
        // var field = $(event.target);
        // var currentRow = field.parent().parent();
        // var newRow = currentRow.clone();

        // newRow.insertAfter(currentRow);
        // newRow.find('input').attr('value', '');
    })
})