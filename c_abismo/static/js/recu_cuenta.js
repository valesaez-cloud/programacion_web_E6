$(function () { 
  const $form = $("#recuperarForm");
  if ($form.length === 0) return;

  $form.on("submit", function (e) {
    e.preventDefault();

    let isValid = true;

    // limpiar estado previo
    $form.find(".error-message").hide().text("");
    $form.find(".form-control").removeClass("is-invalid");

    // === validar CORREO ===
    const $mail = $("#mail");
    const correo = ($mail.val() || "").trim();

    if (correo === "") {
      $mail.addClass("is-invalid");
      $mail.next(".error-message").text("El correo es obligatorio.").show();
      isValid = false;
    } else {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!re.test(correo)) {
        $mail.addClass("is-invalid");
        $mail.next(".error-message").text("Ingresa un correo válido.").show();
        isValid = false;
      }
    }

    if (!isValid) return; // <- corta aquí si hay errores

    // CSRF desde cookie
    function getCookie(name) {
      const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
      return m ? m.pop() : '';
    }

    $.ajax({
      url: "/recuperar_clave",          // o "/recuperar_clave/" si tu URL lleva slash
      type: "POST",
      contentType: "application/json",
      headers: { "X-CSRFToken": getCookie("csrftoken") },
      data: JSON.stringify({ correo: correo }),
      success: function (resp) {
        if (resp && resp.success) {
          alert("Ahora puedes restablecer tu contraseña");
          // usa la redirección que devuelva el backend, o fallback
          window.location.href = resp.redirect || "/recuperar_clave";
        } else {
          alert(resp?.error || "No se pudo procesar la solicitud.");
        }
      },
      error: function (xhr) {
        const res = xhr.responseJSON;
        alert(res?.error || "Error al enviar la solicitud.");
      }
    });
  });
});
