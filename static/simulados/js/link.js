function copiarLink(id_simulado) {
    let textoCopiado = document.getElementById(id_simulado);
    textoCopiado.select();
    document.execCommand("copy");
}