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

/* MÁSCARA DE TELEFONE */
function mascaraTelefone(input) {
    let valor = input.value.replace(/\D/g, "");

    if (valor.length > 11) valor = valor.slice(0, 11);

    if (valor.length > 6) {
        input.value = `(${valor.slice(0,2)}) ${valor.slice(2,7)}-${valor.slice(7)}`;
    } else if (valor.length > 2) {
        input.value = `(${valor.slice(0,2)}) ${valor.slice(2)}`;
    } else {
        input.value = valor.replace(/^(\d{0,2})/, "($1");
    }
}
