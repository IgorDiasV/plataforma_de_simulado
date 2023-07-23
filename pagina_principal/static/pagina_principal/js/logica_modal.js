function filtrar_questoes() {
    asssuntos_escolhidos = get_opcoes_escolhidas("assuntos");
    div_questoes = document.getElementsByClassName('questoes_com_id_assunto')
    for(let i=0;i < div_questoes.length;i++)
    {
        let questao_escolhida = false;
        assuntos_questao = div_questoes[i].getAttribute('id_assuntos')
        for(let index in asssuntos_escolhidos){
          assunto_aux = '*'+asssuntos_escolhidos[index]+'*'
          if(assuntos_questao.includes(assunto_aux)){
            questao_escolhida = true;
            break;
            
          }
        }
        if(questao_escolhida){
            div_questoes[i].style.display='block'; 
        }else
        {
            div_questoes[i].style.display='none'   
        }
    } 
  }
  function fecharModal() {
    var questionModal = document.getElementById("modal_questoes");
    questionModal.style.display = "none";
  }
  document.addEventListener("DOMContentLoaded", function () {
    var addQuestionBtn = document.getElementById("adicionar_questao");
    var questionModal = document.getElementById("modal_questoes");
    var addSelectedQuestionsBtn = document.getElementById(
      "add_questoes_selecionadas"
    );
    var div_questoes = document.getElementById("div_questoes_escolhidas");
    addQuestionBtn.addEventListener("click", function () {
      questionModal.style.display = "block";
    });

    addSelectedQuestionsBtn.addEventListener("click", function () {
      var selectedQuestions = [];
      var checkboxes = document.querySelectorAll(
        'input[name="questoes_selecionadas"]:checked'
      );
      var select_questoes_escolhidas = document.getElementById(
        "questoes_escolhidas"
      );
      for (var i = 0; i < checkboxes.length; i++) {
        text_html = `<label for='questao${checkboxes[i].value}' >${checkboxes[i].labels[0].innerHTML}</label><input id='questao${checkboxes[i].value}' style="display:none" value=${checkboxes[i].value}></br>`;
        div_questoes.innerHTML += text_html;

        var option = document.createElement("option");
        option.value = checkboxes[i].value;
        option.text = checkboxes[i].value;
        option.selected = true;
        select_questoes_escolhidas.add(option);
        checkboxes[i].checked = false;
      }

      questionModal.style.display = "none";
    });
  });