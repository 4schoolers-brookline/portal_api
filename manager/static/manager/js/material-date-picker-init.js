(function($) {
    "use strict"

    // MAterial Date picker
    $('#mdate').bootstrapMaterialDatePicker({
        weekStart: 0,
        time: false
    });
    $('#timepicker').bootstrapMaterialDatePicker({
        format: 'HH:mm',
        time: true,
        date: false
    });
    $('#date-format').bootstrapMaterialDatePicker({
        format: 'dddd DD MMMM YYYY - HH:mm'
    });

    $('#min-date').bootstrapMaterialDatePicker({
        format: 'YYYY/MM/DD HH:mm',
        minDate: new Date(1970, 1, 1)
    });
    $('#min-date-end').bootstrapMaterialDatePicker({
        format: 'YYYY/MM/DD HH:mm',
        minDate: new Date(1970, 1, 1)
    });
})(jQuery);
