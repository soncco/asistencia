(function($) {
  $form = $('#the-form');
  $categoria = $('#categoria');
  $fecha = $('#fecha');
  $wrapper = $('.wrapper');

  $tplTabla = $('#tpl-tabla');
  $tplCaption = $('#tpl-caption');

  $print = $('.print');

  $form.submit(function(e) {
    e.preventDefault();
    $wrapper.find('.report').remove();
    $print.show('slow');
    $('.btn-primary').button('loading');

    $.when(
      $.get('/categoria/cursos/' + $categoria.val() + '/')
    ).then(function(cursos) {
      for(curso in cursos) {
        var theCurso = cursos[curso];
        $.when(
          $.ajax({
            type: 'GET',
            url: '/alumnos/categoria/' + theCurso.id + '/',
            async: false
          })
        ).then(function(data){
          data.curso = theCurso;
          tabla = Mustache.render($tplTabla.clone().html(), data);
          $wrapper.append(tabla);
          $wrapper.find('.report').addClass('animated pulse');          
        }); 
      }
    });

    $('.btn-primary').button('reset');
  });

  $print.click(function() {
    frameSrc = '/reporte/categoria/print/?' + $form.serialize();
    $('iframe').attr("src", frameSrc);
    $('#printModal').modal({show: true});
  });

})(jQuery)
