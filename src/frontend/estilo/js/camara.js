const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const registroForm = document.getElementById("registro-form");
const nombreInput = document.getElementById("nombre");
const codigoInput = document.getElementById("codigo");
const programaInput = document.getElementById("programa");

const btnCapturarRegistro = document.getElementById("capturar-registro");
const btnReconocer = document.getElementById("capturar-reconocimiento");
const btnCargarHistorial = document.getElementById("cargar-historial");

const registroFeedback = document.getElementById("registro-feedback");
const camaraFeedback = document.getElementById("camara-feedback");

const tablaEstudiantes = document.getElementById("tabla-estudiantes");
const tablaAsistencias = document.getElementById("tabla-asistencias");

let fotoRegistro = null;


function showFeedback(node, message, type = "success") {
	node.textContent = message;
	node.className = `feedback ${type}`;
}


async function iniciarCamara() {
	try {
		const stream = await navigator.mediaDevices.getUserMedia({
			video: { width: 960, height: 540 },
			audio: false,
		});
		video.srcObject = stream;
	} catch (error) {
		showFeedback(camaraFeedback, "No fue posible acceder a la camara.", "error");
	}
}


function capturarFoto() {
	if (!video.videoWidth || !video.videoHeight) {
		throw new Error("La camara no esta lista.");
	}

	canvas.width = video.videoWidth;
	canvas.height = video.videoHeight;
	ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

	return canvas.toDataURL("image/jpeg", 0.9);
}


async function requestApi(url, method = "GET", body = null) {
	const options = {
		method,
		headers: { "Content-Type": "application/json" },
	};
	if (body) {
		options.body = JSON.stringify(body);
	}

	const response = await fetch(url, options);
	const data = await response.json();
	if (!response.ok || !data.ok) {
		throw new Error(data.error || "Error en la solicitud");
	}
	return data.data;
}


function renderEstudiantes(estudiantes) {
	tablaEstudiantes.innerHTML = "";
	estudiantes.forEach((item) => {
		const row = document.createElement("tr");
		row.innerHTML = `
			<td>${item.id}</td>
			<td>${item.nombre}</td>
			<td>${item.codigo}</td>
			<td>${item.programa}</td>
		`;
		tablaEstudiantes.appendChild(row);
	});
}


function renderAsistencias(asistencias) {
	tablaAsistencias.innerHTML = "";
	asistencias.forEach((item) => {
		const row = document.createElement("tr");
		row.innerHTML = `
			<td>${item.fecha_hora}</td>
			<td>${item.nombre}</td>
			<td>${item.codigo}</td>
			<td>${item.programa}</td>
		`;
		tablaAsistencias.appendChild(row);
	});
}


async function cargarEstudiantes() {
	const estudiantes = await requestApi("/api/estudiantes");
	renderEstudiantes(estudiantes);
}


async function cargarHistorial() {
	const asistencias = await requestApi("/api/asistencias?limit=100");
	renderAsistencias(asistencias);
}


btnCapturarRegistro.addEventListener("click", () => {
	try {
		fotoRegistro = capturarFoto();
		showFeedback(camaraFeedback, "Foto lista para registrar al estudiante.", "success");
	} catch (error) {
		showFeedback(camaraFeedback, error.message, "error");
	}
});


registroForm.addEventListener("submit", async (event) => {
	event.preventDefault();

	if (!fotoRegistro) {
		showFeedback(registroFeedback, "Primero debes capturar una foto de registro.", "error");
		return;
	}

	try {
		await requestApi("/api/estudiantes", "POST", {
			nombre: nombreInput.value,
			codigo: codigoInput.value,
			programa: programaInput.value,
			fotoBase64: fotoRegistro,
		});

		showFeedback(registroFeedback, "Estudiante registrado correctamente.", "success");
		registroForm.reset();
		fotoRegistro = null;
		await cargarEstudiantes();
	} catch (error) {
		showFeedback(registroFeedback, error.message, "error");
	}
});


btnReconocer.addEventListener("click", async () => {
	try {
		const foto = capturarFoto();
		const data = await requestApi("/api/reconocimiento", "POST", { fotoBase64: foto });
		showFeedback(
			camaraFeedback,
			`Ingreso registrado: ${data.estudiante.nombre} (${data.estudiante.codigo})`,
			"success"
		);
		await cargarHistorial();
	} catch (error) {
		showFeedback(camaraFeedback, error.message, "error");
	}
});


btnCargarHistorial.addEventListener("click", async () => {
	try {
		await cargarHistorial();
		showFeedback(camaraFeedback, "Historial actualizado.", "success");
	} catch (error) {
		showFeedback(camaraFeedback, error.message, "error");
	}
});


iniciarCamara();
cargarEstudiantes().catch(() => {});
cargarHistorial().catch(() => {});

