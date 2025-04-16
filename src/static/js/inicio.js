document.getElementById("size_A").addEventListener("input", generarMatriz);

function showSection(id) {
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
      section.classList.remove('active');
    });
    document.getElementById(id).classList.add('active');
  }

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
    if (metodo == "") {
        document.getElementById("intervalo").style.display = "none";
        document.getElementById("punto_inicial").style.display = "none";
        document.getElementById("punto_inicial_secante").style.display = "none";
        document.getElementById("gx_input").style.display = "none";
        document.getElementById("derivada1_input").style.display = "none";
        document.getElementById("derivada2_input").style.display = "none";
    }
}

function actualizarFormularioIterativas(){
    const metodo = document.getElementById("metodo_iterativo").value;

    document.getElementById("peso_w_input").style.display = "none";

    if (metodo === "sor") {
        document.getElementById("peso_w_input").style.display = "block";
    } 

    else {
        document.getElementById("peso_w_input").style.display = "none";
    }
}

let matrizGenerada = false;
function generarMatriz() {
    const size = parseInt(document.getElementById("size_A").value);
  
    // Obtener contenedores
    const contenedorMatriz = document.getElementById("contenedor-matriz");
    const contenedorB = document.getElementById("contenedor-vector-b");
    const contenedorX0 = document.getElementById("contenedor-vector-x0");
  
    // Limpiar contenido anterior
    contenedorMatriz.innerHTML = "";
    contenedorB.innerHTML = "";
    contenedorX0.innerHTML = "";
  
    if (isNaN(size) || size < 1 || size > 10) {
      return;
    }
  
    // === MATRIZ A ===
    const labelA = document.createElement("label");
    labelA.textContent = "Matriz A:";
    labelA.style.display = "block";
    labelA.style.marginTop = "10px";
    contenedorMatriz.appendChild(labelA);
  
    const gridA = document.createElement("div");
    gridA.style.display = "grid";
    gridA.style.gridTemplateColumns = `repeat(${size}, 1fr)`;
    gridA.style.gap = "5px";
    gridA.style.marginTop = "10px";
  
    for (let i = 1; i <= size; i++) {
      for (let j = 1; j <= size; j++) {
        const input = document.createElement("input");
        input.type = "number";
        input.step = "any";
        input.name = `a${i}${j}`;
        input.placeholder = `a${i}${j}`;
        input.required = true;
        input.style.width = "50px";
        input.style.textAlign = "center";
        gridA.appendChild(input);
      }
    }
  
    contenedorMatriz.appendChild(gridA);
  
    // === VECTOR b ===
    const labelB = document.createElement("label");
    labelB.textContent = "Vector b:";
    labelB.style.display = "block";
    labelB.style.marginTop = "20px";
    contenedorB.appendChild(labelB);
  
    const gridB = document.createElement("div");
    gridB.style.display = "grid";
    gridB.style.gridTemplateColumns = "1fr";
    gridB.style.gap = "5px";
    gridB.style.marginTop = "10px";
  
    for (let i = 1; i <= size; i++) {
      const input = document.createElement("input");
      input.type = "number";
      input.step = "any";
      input.name = `b${i}`;
      input.placeholder = `b${i}`;
      input.required = true;
      input.style.width = "50px";
      input.style.textAlign = "center";
      gridB.appendChild(input);
    }
  
    contenedorB.appendChild(gridB);
  
    // === VECTOR X0 ===
    const labelX0 = document.createElement("label");
    labelX0.textContent = "Vector de valores iniciales X₀:";
    labelX0.style.display = "block";
    labelX0.style.marginTop = "20px";
    contenedorX0.appendChild(labelX0);
  
    const gridX0 = document.createElement("div");
    gridX0.style.display = "grid";
    gridX0.style.gridTemplateColumns = "1fr";
    gridX0.style.gap = "5px";
    gridX0.style.marginTop = "10px";
  
    for (let i = 1; i <= size; i++) {
      const input = document.createElement("input");
      input.type = "number";
      input.step = "any";
      input.name = `x${i}`;
      input.placeholder = `x${i}`;
      input.required = true;
      input.style.width = "50px";
      input.style.textAlign = "center";
      gridX0.appendChild(input);
    }
  
    contenedorX0.appendChild(gridX0);
    matrizGenerada = true;
}

function validarFormulario() {
  if (!matrizGenerada) {
    alert("Debes generar la matriz antes de enviar el formulario.");
    return false;
  }

  // Verifica si todos los inputs tienen valor
  const inputs = document.querySelectorAll("#contenedor-matriz input, #contenedor-vector-b input, #contenedor-vector-x0 input");
  for (let input of inputs) {
    if (input.value.trim() === "") {
      alert("Por favor, completa todos los campos de la matriz y vectores.");
      return false;
    }
  }

  return true; // Todo bien, permitir envío
}