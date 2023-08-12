$(document).ready(function(){
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();

        prod_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if(response.status == 'login_required'){
                    Swal.fire(response.message).then(function(){
                        window.location = '/login';
                    })
                }
                if(response.status == 'Failed'){
                    Swal.fire({
                      icon: 'error',
                      title: response.message
                    })
                    //console.log(response)
                }
                else{
                    $('#cart_counter').html(response.cart_counter["cart_count"]);
                    $('#qty-'+prod_id).html(response.qty);
                }
            }
        })
    })

    $('.remove_from_cart').on('click', function(e){
        e.preventDefault();

        prod_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if(response.status == 'login_required'){
                    Swal.fire(response.message).then(function(){
                        window.location = '/login';
                    })
                }
                if(response.status == 'Failed')
                {
                    Swal.fire({
                      icon: 'error',
                      title: response.message
                    })
                }
                else{
                    $('#cart_counter').html(response.cart_counter["cart_count"]);
                    $('#qty-'+prod_id).html(response.qty);
                }
            }
        })
    })

    //Place the cart item quantity on load
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')

        $('#'+the_id).html(qty)
    })
});