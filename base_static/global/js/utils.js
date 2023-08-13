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