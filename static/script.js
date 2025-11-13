function validarFormulario() {
    const nome = document.getElementById('nome').value.trim();
    const feedback = document.getElementById('feedback').value.trim();

    if (!nome || !feedback) {
        alert("Preencha todos os campos!");
        return false;
    }
    return true;
}