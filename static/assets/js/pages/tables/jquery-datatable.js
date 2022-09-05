$(function () {
    $('.js-basic-example').DataTable();

    //Exportable table
    $('.js-exportable').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        fixedHeader: true,
        scrollX: true,
        scrollY: '85vh',
        scrollCollapse: true,

    });
});