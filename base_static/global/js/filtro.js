function get_values_checked_filter(form, input_name){
  const query = "[name=" + input_name + "]:checked"
  let inputs_checked = form.querySelectorAll(query)
  let ids_filtro_checked = []
  inputs_checked.forEach((input_checked) => {
    ids_filtro_checked.push(input_checked.value)
  })
  return ids_filtro_checked
}

function get_filtros_escolhidos(){
    let form = document.getElementById('form_filtro')
    let ids_filtro_assuntos = get_values_checked_filter(form, 'assuntos')
    let ids_filtro_anos = get_values_checked_filter(form, 'anos')
    return [ids_filtro_assuntos, ids_filtro_anos]
  }

  function filtrar(criar_simulado=false){
      
      let parametros_gerais = parametros_para_redirecionar(criar_simulado)     
      history.replaceState(null, null, window.location.pathname);
      const url = window.location.href + '?' + parametros_gerais
      window.location.href = url
  }

