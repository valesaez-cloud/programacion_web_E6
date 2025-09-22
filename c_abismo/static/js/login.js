$(function () {
  $("#loginForm").on("submit", function (event) {
    event.preventDefault();

    let isValid = true;

    // limpiar estado previo
    $(".error-message").hide().text("");
    $(".form-control").removeClass("is-invalid");

    // === validar CORREO ===
    const $mail = $("#mail");  
    const correo = $mail.val().trim();

    if (correo === "") {
      $mail.addClass("is-invalid");
      $mail.next(".error-message").text("El correo es obligatorio.").show();
      isValid = false;
    } else {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!re.test(correo)) {
        $mail.addClass("is-invalid");
        $mail.next(".error-message").text("El correo no es valido.").show();
        isValid = false;
      }
    }

    // === validar CONTRASEÑA ===
    const $clave = $("#clave");
    const clave = $clave.val().trim();

    if (clave === "") {
      $clave.addClass("is-invalid");
      $clave.next(".error-message").text("La contraseña es obligatoria.").show();
      isValid = false;
    } else if (clave.length < 7) {
      $clave.addClass("is-invalid");
      $clave.next(".error-message").text("La contraseña debe tener mínimo 7 caracteres.").show();
      isValid = false;
    }

    // === si todo está bien ===
    //if (isValid) {
      //alert("Bienvenido, Inicio de sesión exitoso.");
      //this.reset();

    if (isValid) {
    const datos = {
    correo: $("#mail").val().trim(),   // ojo: tu input es #mail (no #correo)
    clave:  $("#clave").val().trim()
    };

  // Lee el CSRF de la cookie
    function getCookie(name) {
    const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return v ? v.pop() : '';
    }

    $.ajax({
      url: "/iniciar_sesion",                // ruta Django que autentica
      type: "POST",
      data: JSON.stringify(datos),
      contentType: "application/json",
      headers: { "X-CSRFToken": getCookie("csrftoken") }, // importante para CSRF
      success: function (response) {
        alert(response.mensaje || "Inicio de sesión exitoso.");
        $("#loginForm")[0].reset();
        window.location.href = "/home";     // o donde quieras redirigir
      },
      error: function (xhr) {
        const res = xhr.responseJSON;
        alert(res?.error || "Credenciales inválidas.");
      }
    });
  }
});
});

