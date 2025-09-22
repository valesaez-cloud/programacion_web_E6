$(".eliminar_usuario").unbind();
$(".eliminar_usuario").click(function()
{ 
  if (confirm("¿Seguro que quieres eliminar este usuario?")) {  
        
    $.ajax({
        url: "/eliminar_usuario",
        type: "POST",
        data: {
            id: $(this).data("id"),
            csrfmiddlewaretoken: "{{ csrf_token }}"
        },
        success: function (response) {
            alert(response.mensaje);
          window.location.href ='/listar_usuarios'
        },
        error: function (xhr) {
            const res = xhr.responseJSON;
            alert(res?.error || "Error al eliminar registro.");
        }
    });
   }
})