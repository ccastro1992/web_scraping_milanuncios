$(document).ready(function(){
    $(document).on('click', '.subcategoryInfo', function(){
        var category_id = $(this).data('id');
        $.ajax({
            url: '/get_subcategory',
            type: 'POST',
            data: {category_id: category_id},
            timeout: 4000,
            beforeSend: function () {
                $('#loader').removeClass('hidden')
            },
            success: function(response){
                var html = '';
                $.each(response.data, function(i, item) {
                    html += '<li>'+item.name+'</li>'
                });

                $('#subcategoryModal .modal-body .list-subcategory').html(html);
                $('#subcategoryModal').modal('show');
            },
            complete: function () {
                $('#loader').addClass('hidden')
            },
        });
    });

    $("#categoryForm").submit(function(e) {
        e.preventDefault();

        var form = $(this);
        var url = form.attr('action');

        $('.dataTables_length').addClass('bs-select');

        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(),
            timeout: 4000,
            beforeSend: function () {
                $('#loader').removeClass('hidden')
            },
            success: function(data){
               $('#categoryTable').dataTable( {
                    "language": {
                        "url": "https://cdn.datatables.net/plug-ins/1.11.3/i18n/es_es.json"
                    },
                    "aaData": data.data,
                    "fixedHeader": {
                        header: true,
                        footer: true
                    },
                    "columns": [
                        { "data": "name" },
                        {
                            "data": "url",
                            "render": function(data, type, row, meta){
                                if(type === 'display'){
                                    data = '<button class="subcategoryInfo" data-id="' + row.id + '">Subcategorias</button>';
                                }
                            return data;
                            }
                        }
                    ]
               })
            },
            complete: function () {
                $('#loader').addClass('hidden')
            },
        });
    });


});