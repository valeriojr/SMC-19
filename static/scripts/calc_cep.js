function addressQuery(form, input) {
    const maxlength = parseInt(input.attr('maxlength'));

    if (maxlength === input.val().length) {
        console.log("Consultando CEP...");
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "http://cep.la/" + input.val(), true);
        xhr.setRequestHeader("Accept", "application/json");
        xhr.onreadystatechange = function () {
            if ((xhr.readyState === 0 || xhr.readyState === 4) && xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                console.log(xhr.responseText);

                $('.street-name-field').val(response.logradouro);
                $('.neighbourhood-field').val(response.bairro);
                $('.city-field').val(response.cidade);

                // form.find(`#id_street_name`).val(response.logradouro);
                // form.find(`#id_neighbourhood`).val(response.bairro);
                // form.find(`#id_city`).val(response.cidade);

            }
        };
        xhr.send(null);
    }
}

$(document).ready(function () {
    $(".postal-code-field").each(function () {
        const input = $(this);
        const form = input.closest("form");
        console.log(input.attr("id"));
        input.on('input', function () {
            addressQuery(form, input);
        });
    });
});