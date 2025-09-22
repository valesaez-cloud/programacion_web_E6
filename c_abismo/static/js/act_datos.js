$(function () {
  const $form = $("#actualizarForm");
  if ($form.length === 0) return;

  $form.on("submit", function (e) {
    e.preventDefault();
    let ok = true;

    // limpiar errores previos
    $form.find(".error-message").hide().text("");
    $form.find(".form-control, .form-select").removeClass("is-invalid");

    // helper para marcar error
    function err($el, msg) {
      if (!$el || !$el.length) return;
      $el.addClass("is-invalid");
      const $err = $el.next(".error-message");
      if ($err.length) $err.text(msg).show();
      ok = false;
    }

    // campos
    const $nombre    = $("#nombre");
    const $apellidos = $("#apellidos");
    const $mail      = $("#mail");
    const $direccion = $("#direccion");
    const $telefono  = $("#telefono");
    const $rol       = $("#rol");

    const nombre    = $nombre.val().trim();
    const apellidos = $apellidos.val().trim();
    const correo    = $mail.val().trim();
    const direccion = $direccion.val().trim();
    const telefono  = $telefono.val().trim();
    const rol       = $rol.val().trim();

    // si todo está vacío => bloquear
    const todosVacios = [nombre, apellidos, correo, direccion, telefono, rol].every(v => v === "");
    if (todosVacios) {
      alert("Primero debes modificar algo antes de actualizar.");
      return;
    }

    // validar SOLO si el campo tiene algo escrito
    if (nombre && nombre.length < 2)       err($nombre, "El nombre debe tener al menos 2 caracteres.");
    if (apellidos && apellidos.length < 2) err($apellidos, "Los apellidos deben tener al menos 2 caracteres.");

    if (correo) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!re.test(correo)) err($mail, "Ingresa un correo válido.");
    }

    if (direccion && direccion.length < 5) err($direccion, "La dirección es demasiado corta.");
    if (telefono && !/^\d{8,15}$/.test(telefono)) err($telefono, "Solo dígitos (8–15).");
    if (rol && !["1","2","3","4"].includes(rol)) err($rol, "Selecciona un rol válido.");

    if (!ok) return;
    const payload = {};
    if (nombre)    payload.nombre = nombre;
    if (apellidos) payload.apellidos = apellidos;
    if (correo)    payload.correo = correo;
    if (direccion) payload.direccion = direccion;
    if (telefono)  payload.telefono = telefono;
    if (rol)       payload.rol = rol;

    // ===== AÑADIDO: CSRF y AJAX =====
    function getCookie(name) {
      const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
      return m ? m.pop() : '';
    }

    $.ajax({
      url: "/actualizar_datos",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({
      nombre: $("#nombre").val(),
      apellidos: $("#apellidos").val(),
      correo: $("#mail").val(),
      direccion: $("#direccion").val(),
      telefono: $("#telefono").val(),
      rol: $("#rol").val()
      }),
    success: function(resp) {
      alert(resp.mensaje || "Actualizado!");
    },
      error: function(xhr) {
        alert("Error: " + (xhr.responseJSON?.error || "No se pudieron actualizar los datos."));
      }
    });
  });
});