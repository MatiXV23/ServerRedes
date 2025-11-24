let imageBase64 = "";

const BASE_URL = "http://10.4.200.117:8080";

let requests = [];
let responses = [];
let flow = [];

//////////////////////////////
// INTERCEPTOR DE REQ Y RES //
//////////////////////////////
const originalFetch = window.fetch;
window.fetch = async function (...args) {
  console.log("FETCH REQUEST:", args);

  const url = args[0];
  const options = args[1] || {};
  const requestDetails = {
    method: options.method || "GET",
    url: url,
    headers: options.headers || {},
    body: options.body || null,
  };

  requests.push(requestDetails);
  flow.push("req");

  const response = await originalFetch.apply(this, args);

  const clonedResponse = response.clone();
  const responseHeaders = {};
  clonedResponse.headers.forEach((value, key) => {
    responseHeaders[key] = value;
  });

  let responseBody = null;
  const contentType = clonedResponse.headers.get("content-type");

  try {
    if (contentType && contentType.includes("application/json")) {
      responseBody = await clonedResponse.json();
    } else if (contentType && contentType.includes("text")) {
      responseBody = await clonedResponse.text();
    } else {
      responseBody = "[Binary Data]";
    }
  } catch (e) {
    responseBody = "[Unable to parse response body]";
  }

  const responseDetails = {
    status: response.status,
    statusText: response.statusText,
    headers: responseHeaders,
    body: responseBody,
  };

  responses.push(responseDetails);
  flow.push("res");

  return response;
};

async function closeConection() {
  try {
    await fetch(BASE_URL + "/close");
  } catch (error) {
    console.error("Error al cerrar conexión:", error);
  }
}

async function loadTitle() {
  try {
    const response = await fetch(BASE_URL + "/titulo");
    const title = await response.text();
    console.log({ title });
    document.getElementById("pageTitle").innerHTML = title;
  } catch (error) {
    console.error("Error cargando título:", error);
    document.getElementById("pageTitle").textContent = "Gestión de Usuarios";
  }
}

async function loadUsers() {
  try {
    const response = await fetch(BASE_URL + "/usuarios");
    const users = await response.json();

    document.getElementById("loadingContainer").style.display = "none";
    const grid = document.getElementById("usersGrid");
    grid.innerHTML = "";

    users.forEach((user) => {
      const card = document.createElement("div");
      card.className = "user-card";
      card.innerHTML = `
                              <div class="user-id">ID: ${user.id}</div>
                              <div class="user-name">${user.nombre}</div>
                              <button class="btn btn-secondary" onclick="viewPhoto('${user.foto}')">
                                  Ver Foto
                              </button>
                              <button class="btn btn-secondary" onclick="editUser(${user.id})">
                                Editar
                              </button>
                          `;
      grid.appendChild(card);
    });
  } catch (error) {
    console.error("Error cargando usuarios:", error);
    showError("Error al cargar los usuarios");
    document.getElementById("loadingContainer").style.display = "none";
  }
}

async function viewPhoto(fotoNombre) {
  const photoContainer = document.getElementById("photoContainer");
  photoContainer.innerHTML =
    '<div class="loading" style="color: #333;">Cargando imagen...</div>';
  document.getElementById("photoModal").classList.add("active");

  try {
    const response = await fetch(`${BASE_URL}/fotos/${fotoNombre}`);
    console.log({ response });
    const blob = await response.blob();
    const imageUrl = URL.createObjectURL(blob);

    photoContainer.innerHTML = `<img src="${imageUrl}" alt="Foto de usuario" class="modal-image">`;
  } catch (error) {
    console.error("Error cargando foto:", error);
    photoContainer.innerHTML =
      '<div class="error">Error al cargar la imagen</div>';
  }
}

function previewImage(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      imageBase64 = e.target.result.split(",")[1];
      const preview = document.getElementById("imagePreview");
      preview.src = e.target.result;
      preview.style.display = "block";
    };
    reader.readAsDataURL(file);
  }
}

async function createUser(event) {
  event.preventDefault();

  const userData = {
    nombre: document.getElementById("userName").value,
    imagen_base64: imageBase64,
  };

  try {
    const response = await fetch(BASE_URL + "/usuarios", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userData),
    });

    if (response.ok) {
      closeCreateModal();
      loadUsers();
      document.getElementById("createUserForm").reset();
      document.getElementById("imagePreview").style.display = "none";
      imageBase64 = "";
    } else {
      showError("Error al crear el usuario");
    }
  } catch (error) {
    console.error("Error creando usuario:", error);
    showError("Error al crear el usuario");
  }
}

async function searchUser() {
  const userId = document.getElementById("searchUserId").value.trim();

  if (!userId) {
    showError("Debe ingresar un ID");
    return;
  }

  try {
    const response = await fetch(`${BASE_URL}/usuarios`);

    if (!response.ok) {
      showError("Usuario no encontrado");
      return;
    }

    const user = await response.json();

    // Mostramos los datos como vos prefieras
    displaySearchedUser(user);
  } catch (error) {
    console.error("Error buscando usuario:", error);
    showError("Error al buscar usuario");
  }
}

async function editUser(userId) {
  console.log("CLICK PUT");
  const updatedData = {
    nombre: "editado",
    imagen_base64: null,
  };

  try {
    const response = await fetch(`${BASE_URL}/usuarios`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updatedData),
    });

    if (response.ok) {
      closeEditModal();
      loadUsers();

      document.getElementById("editUserForm").reset();
      document.getElementById("editImagePreview").style.display = "none";

      imageBase64 = "";
    } else {
      showError("Error al editar el usuario");
    }
  } catch (error) {
    console.error("Error editando usuario:", error);
    showError("Error al editar el usuario");
  }
}

function previewEditImage(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      imageBase64 = e.target.result.split(",")[1];
      const preview = document.getElementById("editImagePreview");
      preview.src = e.target.result;
      preview.style.display = "block";
    };
    reader.readAsDataURL(file);
  }
}

function openEditModal(user) {
  document.getElementById("editUserName").value = user.nombre;

  const preview = document.getElementById("editImagePreview");
  preview.src = `${BASE_URL}/fotos/${user.foto}`;
  preview.style.display = "block";

  document.getElementById("editModal").classList.add("active");
}

function loadReqRes() {
  let template = ``;
  let reqCont = 0;
  let resCont = 0;

  if (flow.length === 0) {
    return `<div class="empty-state">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
            </svg>
            <p>No hay requests/responses aún</p>
          </div>`;
  }

  for (r of flow) {
    if (r === "req") {
      const req = requests[reqCont];
      const formattedReq = JSON.stringify(req, null, 2);
      template += `<div class="request-item"><pre>${formattedReq}</pre></div>`;
      reqCont++;
      continue;
    }
    const res = responses[resCont];
    const formattedRes = JSON.stringify(res, null, 2);
    template += `<div class="response-item"><pre>${formattedRes}</pre></div>`;
    resCont++;
  }

  return template;
}

function openDrawer() {
  document.getElementById("drawer").classList.add("active");
  document.getElementById("drawerOverlay").classList.add("active");
  document.getElementById("drawerContent").innerHTML = loadReqRes();
}

function closeDrawer() {
  document.getElementById("drawer").classList.remove("active");
  document.getElementById("drawerOverlay").classList.remove("active");
}

function openCreateModal() {
  document.getElementById("createModal").classList.add("active");
}

function closeCreateModal() {
  document.getElementById("createModal").classList.remove("active");
}

function closePhotoModal() {
  document.getElementById("photoModal").classList.remove("active");
}

function showError(message) {
  const errorContainer = document.getElementById("errorContainer");
  errorContainer.innerHTML = `<div class="error">${message}</div>`;
  setTimeout(() => {
    errorContainer.innerHTML = "";
  }, 5000);
}

window.onclick = function (event) {
  const photoModal = document.getElementById("photoModal");
  const createModal = document.getElementById("createModal");

  if (event.target === photoModal) {
    closePhotoModal();
  }
  if (event.target === createModal) {
    closeCreateModal();
  }
};

loadTitle();
loadUsers();
