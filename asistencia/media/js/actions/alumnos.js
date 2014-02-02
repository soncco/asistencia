(function($) {
  $form = $('#the-form');
  $wrapper = $('.wrapper');
  $msg = $('.msg');
  $dni = $('#dni');
  $curso $('#curso');

  $tplPersonal = $('#tpl-personal');
  $tpl404 = $('#tpl-404');
  $tpl403 = $('#tpl-403');

  $form.submit(function(e) {
    e.preventDefault();
    $.post(theURL, $form.serialize())
      .done(function(data) {
        var client = Mustache.render($tplPersonal.html(), data);
        limpiar();   
        $wrapper.append(client);
        $wrapper.find('.img-circle').addClass('animated bounceIn');
        $wrapper.find('.text-info').addClass('animated bounceInUp');
        setTimeout(limpiar, 30000);
      })
      .error(function(xhr) {
        if(xhr.status == 404) {
          var msg = Mustache.render($tpl404.html(), {});
          handleAlerts($msg, msg);
        }
        if(xhr.status == 403) {
          var msg = Mustache.render($tpl403.html(), {});
          handleAlerts($msg, msg);
        }
      });
      $dni.val('');
      $curso.val('');
  });
  
})(jQuery)
