function input_invisivel(){
    input = document.getElementById('input_novo_assunto')
    return  input.style.display=='none'
}
function mostrarInputAssunto()
{
    if(input_invisivel()){
        input = document.getElementById('input_novo_assunto');
        botao_adicionar =  document.getElementById('botao_novo_assunto');
        botao_cancelar = document.getElementById('botao_cancelar');

        input.style.display = 'inline';
        botao_adicionar.style.display = 'inline';
        botao_cancelar.style.display = 'inline';
    
    }
}
function adicionarAssunto() {
    input = document.getElementById('input_novo_assunto');
    novoAssunto = input.value;
    if (novoAssunto) {
        var selectAssuntos = document.getElementById("assuntos");
        var option = document.createElement("option");
        option.value = "novo_"+novoAssunto;
        option.text = novoAssunto;
        selectAssuntos.add(option);

        ocultarInput();
    }

}
function ocultarInput(){
    input = document.getElementById('input_novo_assunto');
    botao_adicionar =  document.getElementById('botao_novo_assunto');
    botao_cancelar = document.getElementById('botao_cancelar');
    
    input.value = '';
    input.style.display = 'none';
    botao_adicionar.style.display = 'none';
    botao_cancelar.style.display = 'none';
}
function get_opcoes_escolhidas(id){
    select = document.getElementById(id)

    var assuntos = [];
    for(let i = 0; i < select.options.length; i++)
    {
        if (select.options[i].selected)
        {
            assuntos.push(select.options[i].value);
        }
    }

    return assuntos
}

function configuracao_toolbar(){
    var toolbarOptions = [
        ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
        ['blockquote', 'code-block'],

        [{ 'header': 1 }, { 'header': 2 }],               // custom button values
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
        [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
        [{ 'direction': 'rtl' }],                         // text direction

        [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],

        [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
        [{ 'font': [] }],
        [{ 'align': [] }],
        ['image'],
        ['clean']                                         // remove formatting button
    ];

    return toolbarOptions
}