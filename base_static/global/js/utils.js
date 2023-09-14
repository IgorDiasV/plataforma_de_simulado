function mudar_ocultar_questao(id_div_questao, id_seta_questao, tamanho='200px'){
    let div_questao = document.getElementById(id_div_questao);
    let seta_questao = document.getElementById(id_seta_questao);

    if (div_questao.style.height == 'auto'){
      div_questao.style.height = tamanho
      seta_questao.classList.remove('fa-chevron-up')
      seta_questao.classList.add('fa-chevron-down')
    }else{
      div_questao.style.height = 'auto'
      seta_questao.classList.remove('fa-chevron-down')
      seta_questao.classList.add('fa-chevron-up')
    }
  }

  function parametros_para_redirecionar(criar_simulado=false){
      
    const parametros = new URLSearchParams();
    
    if(criar_simulado){
      let id_simulado = document.getElementById('id_simulado')
      let titulo = document.getElementById('titulo')
      let id_perguntas_selecionadas = get_questoes_escolhidas()
      const parametroListaQuestoes = id_perguntas_selecionadas.join(',');
      parametros.append('id_questao', parametroListaQuestoes);
      parametros.append('titulo', titulo.value)
      parametros.append('id_simulado', id_simulado.value)
    }

    let ids_filtro = get_filtros_escolhidos()
    let ids_filtro_assuntos = ids_filtro[0]
    let ids_filtro_anos = ids_filtro[1]
    let ids_filtro_origens = ids_filtro[2]

    const parametroListaAssuntos = ids_filtro_assuntos.join(',');
    const parametroListaAnos = ids_filtro_anos.join(',');
    const parametroListaOrigens = ids_filtro_origens.join(',');

    parametros.append('id_assuntos_filtro', parametroListaAssuntos);
    parametros.append('id_anos_filtro', parametroListaAnos);
    parametros.append('ids_filtro_origens', parametroListaOrigens);


    return parametros.toString();


}


function mudar_pagina(pagina, criar_simulado=false, tem_parametros_gerais=true){
  const parametros = new URLSearchParams();
  parametros.append('page', pagina)
  history.replaceState(null, null, window.location.pathname);

  let url;

  if (tem_parametros_gerais){

    let parametros_gerais = parametros_para_redirecionar(criar_simulado)
    url = window.location.href + '?' + parametros.toString() + '&' + parametros_gerais;
  }else{
    url = window.location.href + '?' + parametros.toString();
  }

  window.location.href = url
}