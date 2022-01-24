//faz a busca de health_centers pelo nome, sigla, endereço... durante a criação de atendimetos
var select_health_centers = $("#id_health_center");//aqui onde ele vai mostrar os health_centers encontrados
var health_center_button = $("#search_health_center_button");//aqui o botão onde clicka pra buscar
var health_center_search_input = $("#search-health_center");//aqui o valor informado pra busca

health_center_button.on('click', () => {
    var term = health_center_search_input.val();
    $.get("/unidades/" + term + "/buscar", (health_centers, status) => {

        select_health_centers.html("");

        if (health_centers.length === 0) {
            //não achou health_centers
            //Aqui é uns html pra deixar no padrão do crispy form...
            var option = $("<option selected></option>");
            option.val("");
            option.text("Nenhuma unidade de saúde encontrada encontrado.");

            select_health_centers.append(option);
        } else {
            health_centers.forEach((health_center) => {//achou health_centers
                //Aqui é uns html pra deixar no padrão do crispy form...
                var option = $("<option></option>");
                option.text(
                    health_center.center_name + " - " + health_center.street_name + ", " +
                    (health_center.number || "S/N") + ' - ' + health_center.neighbourhood + ", " +
                    health_center.city + ", " + health_center.postal_code
                );
                option.val(health_center.id);
                select_health_centers.append(option);
            });
        }
    })
});