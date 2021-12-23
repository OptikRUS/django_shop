'use strict';

window.onload = function () {
    console.log('DOM ready');
    $('.basket_record').on('change', "input[type='number']", function (event){
        let qty = event.target.value;
        let basketItemPk = event.target.name;
        console.log(qty, basketItemPk);
        $.ajax({
            url: "/basket/update/" + basketItemPk + "/" + qty + "/",
            success: function (data) {
                if (data.status) {
                    $('.basket_summary').html(data.basket_summary);
                }
            },
        });
    });
}