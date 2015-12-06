      $(document).ready(function() {
        $('#problems').DataTable( {
            "pagingType": "full_numbers",
            "ordering": false,
             "lengthMenu": [[5,10, 25, 50, -1], [5,10, 25, 50, "All"]],
             "iDisplayLength": 10
        } );
      });