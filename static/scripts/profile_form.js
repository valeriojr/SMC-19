$(document).ready(function () {
    $("#id_birth_date").on('change', () => {
        var birth_date = new Date($("#id_birth_date").val());
        var today = new Date();
        var diff = new Date(milisecond = (today - birth_date));
        var age = Math.abs(diff.getFullYear() - 1970);
        $("#id_age").val(age);
    });

    $("#id_age").on("change", function () {
        const birthDateField = $("#id_birth_date");
        const birthDate = new Date(birthDateField.val());
        birthDate.setFullYear(new Date().getFullYear() - $(this).val());
        birthDateField.val(`${birthDate.toISOString().split('T')[0]}`);
    });

    if (typeof neighbourhoodListUrl !== 'undefined') {

        const citySelect = $("#id_address_set-0-city");
        const neighbourhoodSelect = $("#id_address_set-0-neighbourhood");
        const neighbourhoodInputText = $("#id_address_set-0-input_text_neighbourhood");

        neighbourhoodInputText.on("change", function () {
            const inputText = neighbourhoodInputText.val();
            neighbourhoodSelect.append(`<option value="${inputText}">${inputText}</option>`)
            neighbourhoodSelect.val(inputText).attr("selected", "selected");
        });

        neighbourhoodSelect.on("change", function () {
            neighbourhoodInputText.val(neighbourhoodSelect.val());
        });

        $("#id_address_set-0-state").change(function(){
            $.getJSON(`${countyListUrl}?uf=${$(this).val()}`, function(response){
                citySelect.empty();
                $.each(response, function (i, c) {
                     citySelect.append(`<option value="${c}">${c}</option>`);
                });
            });
        });

// initial load of neighbourhoods
        handleNeighbourhoodField();

        citySelect.on("change", handleNeighbourhoodField);

        function handleNeighbourhoodField() {
            $.getJSON(neighbourhoodListUrl + "?city=" + citySelect.val(), function (response) {
                if (response.length > 0) {
                    neighbourhoodInputText.parent().parent().hide();
                    neighbourhoodSelect.parent().parent().show();

                    neighbourhoodSelect.empty();

                    $.each(response, function (i, neighbourhood) {
                        neighbourhoodSelect.append(`<option value="${neighbourhood}">${neighbourhood}</option>`);
                    });
                    // set inital value for input text from select input
                    neighbourhoodInputText.val(neighbourhoodSelect.val());
                } else {
                    neighbourhoodSelect.parent().parent().hide();
                    neighbourhoodInputText.parent().parent().show();

                    neighbourhoodInputText.val("");
                }
            });
        }
    }
});
