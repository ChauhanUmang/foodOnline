$(document).ready(function(){
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();

        prod_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        data = {
            product_id: prod_id,
        }

        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response){
                console.log(response);
            }
        })
    })
});