//faz a busca de pacientes pelo nome, cpf, rg... durante a criação de atendimetos
var select_profiles = $("#id_profile");//aqui onde ele vai mostrar os pacientes encontrados
var button = $("#search_profile_button");//aqui o botão onde clicka pra buscar
var search_input = $("#search-profile");//aqui o valor informado pra busca

button.on('click', () => {
    var term = search_input.val();
    $.get("/pacientes/" + term + "/buscar", (profiles, status) => {

        select_profiles.html("");

        if (profiles.length === 0) {
            //não achou pacientes
            //Aqui é uns html pra deixar no padrão do crispy form...
            var option = $("<option selected></option>");
            option.val("");
            option.text("Nenhum paciente encontrado.");

            select_profiles.append(option);
        } else {
            profiles.forEach((profile) => {//achou pacientes
                //Aqui é uns html pra deixar no padrão do crispy form...
                var option = $("<option></option>");
                option.text(profile.full_name + ", cpf:" + profile.cpf);
                option.val(profile.id);
                select_profiles.append(option);
            });
        }
    })
});