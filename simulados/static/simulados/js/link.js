async function gerar_link(id_simulado, url)
{
    
        var csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
        const configuracao = {
            method : 'POST',
            headers:{
                "Content-Type":'application/json',
                'X-CSRFToken': csrf_token
        },
          body: JSON.stringify({'id_simulado':id_simulado})
        }
        
        const reposta = await fetch(url,configuracao)
        const link = await reposta.json()        
                      
        var inputLink = document.getElementById('link'+id_simulado)
        inputLink.setAttribute("value", link.link);
        inputLink.style.display = 'inline-block'

        var botaoGerar = document.getElementById('botaoGerar'+id_simulado)
        botaoGerar.remove()
        var botaoCopiar = document.getElementById('botaoCopiar'+id_simulado)
        botaoCopiar.style.display = 'block'
  
}

function copiarLink(id_simulado) {
    let textoCopiado = document.getElementById(id_simulado);
    textoCopiado.select();
    document.execCommand("copy");
}