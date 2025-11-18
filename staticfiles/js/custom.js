(function() {
	'use strict';

	var tinyslider = function() {
		var el = document.querySelectorAll('.testimonial-slider');

		if (el.length > 0) {
			var slider = tns({
				container: '.testimonial-slider',
				items: 1,
				axis: "horizontal",
				controlsContainer: "#testimonial-nav",
				swipeAngle: false,
				speed: 700,
				nav: true,
				controls: true,
				autoplay: true,
				autoplayHoverPause: true,
				autoplayTimeout: 3500,
				autoplayButtonOutput: false
			});
		}
	};
	tinyslider();

	


	var sitePlusMinus = function() {

		var value,
    		quantity = document.getElementsByClassName('quantity-container');

		function createBindings(quantityContainer) {
	      var quantityAmount = quantityContainer.getElementsByClassName('quantity-amount')[0];
	      var increase = quantityContainer.getElementsByClassName('increase')[0];
	      var decrease = quantityContainer.getElementsByClassName('decrease')[0];
	      increase.addEventListener('click', function (e) { increaseValue(e, quantityAmount); });
	      decrease.addEventListener('click', function (e) { decreaseValue(e, quantityAmount); });
	    }

	    function init() {
	        for (var i = 0; i < quantity.length; i++ ) {
						createBindings(quantity[i]);
	        }
	    };

	    function increaseValue(event, quantityAmount) {
	        value = parseInt(quantityAmount.value, 10);

	        console.log(quantityAmount, quantityAmount.value);

	        value = isNaN(value) ? 0 : value;
	        value++;
	        quantityAmount.value = value;
	    }

	    function decreaseValue(event, quantityAmount) {
	        value = parseInt(quantityAmount.value, 10);

	        value = isNaN(value) ? 0 : value;
	        if (value > 0) value--;

	        quantityAmount.value = value;
	    }
	    
	    init();
		
	};
	sitePlusMinus();


})()

document.addEventListener('DOMContentLoaded', function () {
    // Attach event to plus buttons
    document.querySelectorAll('.increase').forEach(button => {
        button.addEventListener('click', function () {
            updateQuantity(this, 1);
        });
    });

    // Attach event to minus buttons
    document.querySelectorAll('.decrease').forEach(button => {
        button.addEventListener('click', function () {
            updateQuantity(this, -1);
        });
    });

    function updateQuantity(button, change) {
        const row = button.closest('tr');
        const quantityInput = row.querySelector('.quantity-amount');
        let quantity = parseInt(quantityInput.value);
        if (isNaN(quantity)) quantity = 1;

        const itemId = row.dataset.itemId;

        const newQuantity = Math.max(1, quantity + change);
        quantityInput.value = newQuantity;

        fetch(`/update-cart/${itemId}/${newQuantity}/`, {
            method: 'GET',
        })
        .then(response => response.json())
        .then(data => {
            row.querySelector('.product-total').textContent = `₹${data.item_total}`;
            document.querySelectorAll('.cart-subtotal').forEach(e => e.textContent = `₹${data.cart_total}`);
        });
    }
});