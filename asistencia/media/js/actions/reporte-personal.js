(function($) {
  $form = $('#the-form');
  $fecha = $('#fecha');
  $wrapper = $('.wrapper');

  $tplTabla = $('#tpl-tabla');
  $tplCaption = $('#tpl-caption');

  $form.submit(function(e) {
    e.preventDefault();
    $.post(theURL, $form.serialize())
      .done(function(data) {
        $wrapper.find('.report').remove();
        var tabla = Mustache.render($tplTabla.html(), data);
        $wrapper.append(tabla);
        $wrapper.find('.report').addClass('animated flipInY');
        $table = $wrapper.find('.table')
        $table.find('td:contains("Falta")').addClass('danger')

        caption = Mustache.render($tplCaption.html(), {
          'fecha': moment($fecha.val(), 'YYYY-MM-DD').format('DD, MMM YYYY')
        });

        $table.append(caption);
      })

  });
  
})(jQuery)
