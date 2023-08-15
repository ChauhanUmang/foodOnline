$(document).ready(function(){
    function addToCartAjax(url, delete_cart_url){
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if(response.status == 'login_required'){
                    Swal.fire(response.message).then(function(){
                        window.location = '/login';
                    })
                }
                else if(response.status == 'different_vendors'){
                    Swal.fire({
                        title: response.message,
                        text: 'Your cart contains items from other restaurant. Would you like to reset your cart for adding items from this restaurant?',
                        showCancelButton: true,
                        cancelButtonText: 'NO',
                        confirmButtonColor: '#3085d6',
                        cancelButtonColor: '#d33',
                        confirmButtonText: 'YES, START AFRESH',
                    }).then((result) => {
                        if(result.isConfirmed){
                            // Delete complete cart made ajax call
                            $.ajax({
                                type: 'GET',
                                url: delete_cart_url,
                                success: function(res){
                                    $('#cart_counter').html(res.cart_counter["cart_count"]);
                                    // Add the new product in cart
                                    // Call the addToCartAjax function again recursively
                                    addToCartAjax(url, delete_cart_url);
                                }
                            })
                        }
                    });
                }
                else if(response.status == 'Failed'){
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
    }

    $('.add_to_cart').on('click', function(e) {
    e.preventDefault();

    prod_id = $(this).attr('data-id');
    url = $(this).attr('data-url');
    delete_cart_url = $(this).attr('data-delete-cart-url');

    // Call the addToCartAjax function for the first time
    addToCartAjax(url, delete_cart_url);
    });

    $('.remove_from_cart').on('click', function(e){
        e.preventDefault();

        prod_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');

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

                    // Since we are calling below functions in the delete from the cart. So if we are on the marketplace page
                    // and decrease the number of items to zero, it will give an error and there is no cart-item object
                    // on the marketplace page.
                    // we should check if we are on the cart page.
                    if(window.location.pathname == "/cart/"){
                        removeCartItem(response.qty, cart_id);
                        checkEmptyCart();
                    }
                }
            }
        })
    })

    // Delete from cart function
    $('.delete_from_cart').on('click',function(e){
        e.preventDefault();

        cart_id = $(this).attr('data-id');
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
                    Swal.fire( response.status , response.message, 'success');
                    removeCartItem(0, cart_id);
                    checkEmptyCart();
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

    //Check if cart is empty
    function checkEmptyCart()
    {
        var cart_counter = document.getElementById('cart_counter').innerHTML;
        if(cart_counter <= 0)
        {
            document.getElementById('empty-cart').style.display = 'block';
            document.getElementById('cart-content').style.display = 'none';
        }
    }

    // Delete the cart element if the quantity is zero
    function removeCartItem(cartItemQty, cart_id)
    {
        if(cartItemQty <= 0)
        {
            //remove the cart item element
            document.getElementById('cart-item-'+cart_id).remove();
        }
    }

});