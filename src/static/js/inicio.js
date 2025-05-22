document.getElementById("size_A").addEventListener("input", generarMatriz);

function showSection(id, linkElement) {
  // Oculta todas las secciones
  const sections = document.querySelectorAll(".section");
  sections.forEach(section => section.classList.remove("active"));
  sections.forEach(section => section.classList.remove("iterativos"));

  // ❌ Elimina los mensajes de todas las secciones
  const allMessages = document.querySelectorAll(".messages");
  allMessages.forEach(msg => msg.remove());

  // Muestra solo la sección correspondiente
  const selectedSection = document.getElementById(id);
  if (selectedSection) {
      selectedSection.classList.add("active");
  }

  // Remueve clase activa de todos los enlaces
  const links = document.querySelectorAll(".navegacion a");
  links.forEach(link => link.classList.remove("active-link"));

  // Añade clase activa al enlace actual
  if (linkElement) {
      linkElement.classList.add("active-link");
  }
}

function initPage() {
  const activeSection = document.querySelector('.section.active');
  
  if (!activeSection) {
    const defaultLink = document.querySelector('nav a');
    showSection('enl', defaultLink);
  } else {
    const sectionId = activeSection.id;

    // Buscar el enlace correspondiente que activa esta sección
    const correspondingLink = document.querySelector(`.navegacion a[data-target="${sectionId}"]`);
    
    if (correspondingLink) {
      correspondingLink.classList.add('active-link');
    }
  }
}

function actualizarFormularioENL() {
  const metodo = document.getElementById("metodo").value;

  // Ocultar todos los campos primero
  console.log('Método seleccionado:', metodo); // Verificar el valor de 'metodo'

  document.getElementById("intervalo").classList.remove('visible');
  document.getElementById("punto_inicial").classList.remove('visible');
  document.getElementById("punto_inicial_secante").classList.remove('visible');
  document.getElementById("gx_input").classList.remove('visible');
  document.getElementById("derivada1_input").classList.remove('visible');
  document.getElementById("derivada2_input").classList.remove('visible');

  document.getElementById("intervalo").classList.add('oculto');
  document.getElementById("punto_inicial").classList.add('oculto');
  document.getElementById("punto_inicial_secante").classList.add('oculto');
  document.getElementById("gx_input").classList.add('oculto');
  document.getElementById("derivada1_input").classList.add('oculto');
  document.getElementById("derivada2_input").classList.add('oculto');

  // Mostrar según el método seleccionado
  if (metodo === "Biseccion" || metodo === "Regla Falsa") {
    document.getElementById("intervalo").classList.add('visible');
    document.getElementById("intervalo").classList.remove('oculto');
  } else if (metodo === "Secante") {
    document.getElementById("punto_inicial_secante").classList.remove('oculto');
    document.getElementById("punto_inicial_secante").classList.add('visible');
  } else {
    document.getElementById("punto_inicial").classList.remove('oculto');
    document.getElementById("punto_inicial").classList.add('visible');
  }

  if (metodo === "Punto Fijo") {
    document.getElementById("gx_input").classList.remove('oculto');
    document.getElementById("gx_input").classList.add('visible');
  }

  if (metodo === "Newton" || metodo === "Newton M2") {
    document.getElementById("derivada1_input").classList.remove('oculto');
    document.getElementById("derivada1_input").classList.add('visible');
  }

  if (metodo === "Newton M2") {
    document.getElementById("derivada2_input").classList.remove('oculto');
    document.getElementById("derivada2_input").classList.add('visible');
  }

  if (metodo == "") {
    document.getElementById("intervalo").classList.remove('visible');
    document.getElementById("punto_inicial").classList.remove('visible');
    document.getElementById("punto_inicial_secante").classList.remove('visible');
    document.getElementById("gx_input").classList.remove('visible');
    document.getElementById("derivada1_input").classList.remove('visible');
    document.getElementById("derivada2_input").classList.remove('visible');

    document.getElementById("intervalo").classList.add('oculto');
    document.getElementById("punto_inicial").classList.add('oculto');
    document.getElementById("punto_inicial_secante").classList.add('oculto');
    document.getElementById("gx_input").classList.add('oculto');
    document.getElementById("derivada1_input").classList.add('oculto');
    document.getElementById("derivada2_input").classList.add('oculto');
  }
}

function actualizarFormularioIterativas(){
    const metodo = document.getElementById("metodo_iterativo").value;

    document.getElementById("peso_w_input").classList.remove('visible');
    document.getElementById("peso_w_input").classList.add('oculto');

    if (metodo === "sor") {
      document.getElementById("peso_w_input").classList.remove('oculto');
      document.getElementById("peso_w_input").classList.add('visible');
    } 

    else {
      document.getElementById("peso_w_input").classList.remove('visible');
      document.getElementById("peso_w_input").classList.add('oculto');
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
    labelX0.textContent = "Vector X₀:";
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