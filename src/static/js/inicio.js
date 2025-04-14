function actualizarFormularioENL() {
    const metodo = document.getElementById("metodo").value;

    // Ocultar todos los campos primero
    document.getElementById("intervalo").style.display = "none";
    document.getElementById("punto_inicial").style.display = "none";
    document.getElementById("punto_inicial_secante").style.display = "none";
    document.getElementById("gx_input").style.display = "none";
    document.getElementById("derivada1_input").style.display = "none";
    document.getElementById("derivada2_input").style.display = "none";

    // Mostrar según método
    if (metodo === "Biseccion" || metodo === "Regla Falsa") {
document.getElementById("intervalo").style.display = "block";
    } else if (metodo === "Secante") {
        document.getElementById("punto_inicial_secante").style.display = "block";
    } else {
        document.getElementById("punto_inicial").style.display = "block";
    }

    if (metodo === "Punto Fijo") {
        document.getElementById("gx_input").style.display = "block";
    }

    if (metodo === "Newton" || metodo === "Newton M2") {
        document.getElementById("derivada1_input").style.display = "block";
    }

    if (metodo === "Newton M2") {
        document.getElementById("derivada2_input").style.display = "block";
    }
}

function showSection(id) {
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
      section.classList.remove('active');
    });
    document.getElementById(id).classList.add('active');
  }