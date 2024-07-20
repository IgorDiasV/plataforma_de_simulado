
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
