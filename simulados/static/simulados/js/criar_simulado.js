function adicionar_remover_questao(checkbox, id_questao){
    if (checkbox.checked){
      adicionar_questao(id_questao)
    }else{
      remover_questao(id_questao)
    }
  }

  function adicionar_questao(id)
  {
      
      let select_questoes_escolhidas = document.getElementById('questoes_escolhidas')
      let option = document.createElement("option");
      option.id = "option" + id;
      option.value = id;
      option.text = id;
      option.selected = true;
      select_questoes_escolhidas.add(option);

      let container_questoes_escolhidas = document.getElementById('container_questoes_escolhidas')
      let conteudo_questao = document.getElementById('questao'+id).querySelector('.container-questao')
      
      let html = `<div id='questao_escolhida${id}' class='questao'>`
      html += `<button class='btn btn-danger' onclick='remover_questao(${id})'>Remover Questão</button>`
      html += ` <i id="seta_questao_escolhida${id}" class="fa-solid fa-chevron-down" onclick="mudar_ocultar_questao('questao_escolhida${id}','seta_questao_escolhida${id}')"></i>`
      html +=  `${conteudo_questao.innerHTML}</div>`
      container_questoes_escolhidas.innerHTML+= html
        
  }
  function remover_questao(id)
  {
    document.getElementById('questao_escolhida'+id).remove()
    
    let checkbox = document.getElementById('input'+id)
    checkbox.checked = false
    
    id = "option" + id
    let option = document.getElementById(id)
    option.remove()


  

  }

  function get_questoes_escolhidas(){
    let select_questoes = document.getElementById('questoes_escolhidas')
    let questoes_escolhidas = select_questoes.querySelectorAll('option:checked')
    id_perguntas_selecionadas = []
    questoes_escolhidas.forEach((pergunta) => {
          id_perguntas_selecionadas.push(pergunta.value)
    })
    return id_perguntas_selecionadas
  }


