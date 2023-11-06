function  mudar_visibilidade_filtro(id_campo_filtro, id_seta)
{
    let lista_itens = document.getElementById(id_campo_filtro);
    let seta =  document.getElementById(id_seta)

    if (lista_itens.style.display == 'none' || lista_itens.style.display == '' ) {
        seta.classList.remove('fa-chevron-down')
        seta.classList.add('fa-chevron-up')
        lista_itens.style.display = 'flex';
        lista_itens.parentNode.style.height = 'auto'
    } else {
        seta.classList.remove('fa-chevron-up')
        seta.classList.add('fa-chevron-down')
        lista_itens.style.display = 'none';
        lista_itens.parentNode.style.height = '25px'
    }
}

function busca_filtrar(id_busca, id_item){
    let busca = document.getElementById(id_busca);
    let itens_do_filtro = document.querySelectorAll(id_item);
    let filtro = busca.value.toLowerCase();
    for (let item of itens_do_filtro) {
        let nome_item = item.querySelector('label').textContent.toLowerCase();
        if (nome_item.includes(filtro)){
            item.style.display = 'block'
        }else{
            item.style.display = 'none'
        }
        
    }
}
