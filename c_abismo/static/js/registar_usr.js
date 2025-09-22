$(document).ready(function () {
  $("#registroForm").submit(function (event) {
    event.preventDefault();
    let isValid = true;

    // limpiar errores previos
    $(".error-message").hide();
    $(".form-control, .form-select").removeClass("is-invalid");

    // Campos obligatorios (usa tus IDs: #nombre, #apellidos, #mail, #direccion, #telefono, #clave, #rol)
    const campos = ["#nombre", "#apellidos", "#mail", "#direccion", "#telefono", "#clave", "#rol"];
    const mensajes = [
      "El nombre es obligatorio.",
      "Los apellidos son obligatorios.",
      "El correo es obligatorio.",
      "La dirección es obligatoria.",
      "El teléfono es obligatorio.",
      "La contraseña es obligatoria.",
      "Selecciona un rol."
    ];

    campos.forEach((campo, i) => {
      if ($(campo).val().trim() === "") {
        $(campo).addClass("is-invalid");
        $(campo).next(".error-message").text(mensajes[i]).show();
        isValid = false;
      }
    });

    if (!isValid) return;
      // alert("Usuario nuevo registrado correctamente.");
      // $("#registroForm")[0].reset();

    const datos = {
      nombre: $("#nombre").val().trim(),
      apellidos: $("#apellidos").val().trim(),
      correo: $("#mail").val().trim(),
      direccion: $("#direccion").val().trim(),
      telefono: $("#telefono").val().trim(),
      clave: $("#clave").val().trim(),
      rol: $("#rol").val().trim()
    };

    // ===== AÑADIDO: CSRF y AJAX =====
    function getCookie(name) {
      const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
      return m ? m.pop() : '';
    }

    $.ajax({
      url: "/registrar_usuario",                 
      type: "POST",
      data: JSON.stringify(datos),
      contentType: "application/json",
      headers: { "X-CSRFToken": getCookie("csrftoken") },
      success: function (response) {
        alert(response.mensaje || "Usuario registrado correctamente.");
        $("#registroForm")[0].reset();
        window.location.href = "/home";      
      },
      error: function (xhr) {
        const res = xhr.responseJSON;
        alert(res?.error || "Error al registrar.");
      }
    });
  });
});