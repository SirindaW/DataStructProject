var updateBtns = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateBtns.length; i++) {

    updateBtns[i].addEventListener('click', function() {
        console.log("User:", user);
        // var productId = this.dataset.productId;
        var productSlug = this.dataset.productSlug;
        var action = this.dataset.action;
        var quantity = document.getElementById('items-quantity').value;

        if (user === "AnonymousUser") {
            console.log("USER IS NOT LOGGED IN");
        } else {
            updateUserOrder(productSlug, quantity, action)
        }
    });

}

var removeFromCartBtns = document.getElementsByClassName('cartpage-remove')

for (var i = 0; i < removeFromCartBtns.length; i++) {
    removeFromCartBtns[i].addEventListener('click', function() {
        var productSlug = this.dataset.productSlug;
        var action = this.dataset.action;
        var quantity = 0

        if (user == "AnonymousUser") {} else {
            updateUserOrder(productSlug, quantity, action)
        }
    })
}

function updateUserOrder(productSlug, quantity, action) {
    console.log("User is logged in, sending data...");

    var url = '/cart/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,

        },
        body: JSON.stringify({ 'productSlug': productSlug, 'quantity': quantity, 'action': action })
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:', data)
        location.reload()
    })


}