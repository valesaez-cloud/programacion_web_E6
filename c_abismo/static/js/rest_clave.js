
$(function () {
  const $form = $("#restablecerForm");
  if ($form.length === 0) return;

  function getCookie(name){
    const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return m ? m.pop() : '';
  }

  $form.on("submit", function (e) {
    e.preventDefault();

    const $c1 = $("#clave1");
    const $c2 = $("#clave2");
    const c1 = ($c1.val() || "").trim();
    const c2 = ($c2.val() || "").trim();

    // limpiar errores visuales
    $(".error-message").hide().text("");
    $(".form-control").removeClass("is-invalid");

    // validaciones rápidas
    let ok = true;
    if (c1.length < 7){
      $c1.addClass("is-invalid");
      $c1.next(".error-message").text("Mínimo 7 caracteres.").show();
      ok = false;
    }
    if (c1 !== c2){
      $c2.addClass("is-invalid");
      $c2.next(".error-message").text("No coincide.").show();
      ok = false;
    }
      // Validaciones adicionales
    if (!/[A-Z]/.test(c1)) {
      $c1.addClass("is-invalid");
      $c1.next(".error-message").text("Debe incluir al menos una letra mayúscula.").show();
      ok = false;
    }

    if (!/[a-z]/.test(c1)) {
      $c1.addClass("is-invalid");
      $c1.next(".error-message").text("Debe incluir al menos una letra minúscula.").show();
      ok = false;
    }

    if (!/[0-9]/.test(c1)) {
      $c1.addClass("is-invalid");
      $c1.next(".error-message").text("Debe incluir al menos un número.").show();
      ok = false;
    }

    if (!/[!@#$%^&*(),.?":{}|<>]/.test(c1)) {
      $c1.addClass("is-invalid");
      $c1.next(".error-message").text("Debe incluir al menos un carácter especial.").show();
      ok = false;
    }
    if (!ok) return;

    $.ajax({
      url: "/restablecer_clave",    // <-- DEBE coincidir con tu path
      type: "POST",
      contentType: "application/json",
      headers: { "X-CSRFToken": getCookie("csrftoken") },
      data: JSON.stringify({ clave1: c1, clave2: c2 }),
      success: function(resp){
        if (resp && resp.success){
          alert(resp.mensaje || "Contraseña actualizada. Inicia sesión.");
          window.location.href = "/login";
        } else {
          alert(resp?.error || "No se pudo actualizar la contraseña.");
        }
      },
      error: function(xhr){
        const res = xhr.responseJSON;
        alert(res?.error || "Error al procesar la solicitud.");
      }
    });
  });
});