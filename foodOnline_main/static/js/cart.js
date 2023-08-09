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
                console.log(response.cart_counter["cart_count"]);
                $('#cart_counter').html(response.cart_counter["cart_count"]);
                $('#qty-'+prod_id).html(response.qty);
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