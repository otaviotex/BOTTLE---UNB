const VerEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function validateFields() {
    const email = document.getElementById("email").value;
    const botao = document.getElementById("entrar");

    botao.disabled = !VerEmail.test(email);
}

function validarFormulario() {
    const email = document.getElementById("email").value;

    if (!VerEmail.test(email)) {
        alert("Por favor, insira um email válido!");
        return false;
    }

    return true;
}
