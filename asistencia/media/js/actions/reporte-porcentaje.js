(function($) {
  $form = $('#the-form');
  $curso = $('#curso');
  $wrapper = $('.wrapper');

  $tplTabla = $('#tpl-tabla');
  $tplCaption = $('#tpl-caption');

  $form.submit(function(e) {
    e.preventDefault();
    $('.btn-primary').button('loading');
    $.post(theURL, $form.serialize())
      .done(function(data) {
        $wrapper.find('.report').remove();
        var tabla = Mustache.render($tplTabla.html(), data);
        $wrapper.append(tabla);
        $wrapper.find('.report').addClass('animated flipInY');
        $table = $wrapper.find('.table')
        $('.percent').each(function(i) {
          text = $(this).text().trim();
          console.log(text);
          if(text > 51) $(this).addClass('success');
          if(text <= 50 && text > 21) $(this).addClass('warning');
          if(text <= 20) $(this).addClass('danger');
        });

        $option = $curso.find(':selected');
        caption = Mustache.render($tplCaption.html(), {
          'nombre': $option.text(),
          'hora_inicio': $option.data('horainicio'),
          'hora_fin': $option.data('horafin'),
          'fecha_inicio': $option.data('fechainicio'),
          'fecha_fin': $option.data('fechafin'),
        });

        $wrapper.find('.print').click(function() {
          frameSrc = '/reporte/curso/porcentaje/print/?' + $form.serialize();
          $('iframe').attr("src", frameSrc);
          $('#printModal').modal({show: true});
        });

        $table.append(caption);
      })
    $('.btn-primary').button('reset');
  });
  
})(jQuery)
