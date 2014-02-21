(function($) {
  
  function stripTrailingSlash(str) {
    if(str.substr(-1) == '/') {
      return str.substr(0, str.length - 1);
    }
    return str;
  }

  var url = window.location.pathname;  
  var activePage = stripTrailingSlash(url);

  $('.nav li a').each(function(){  
    var currentPage = stripTrailingSlash($(this).attr('href'));

    if (activePage == currentPage) {
      $(this).parent().addClass('active'); 
    } 
  });

  $('.datepicker').datepicker({
    changeMonth: true,
    changeYear: true,
    dateFormat: 'yy-mm-dd',
    maxDate: new Date()
  });

  limpiar = function() {
    $wrapper.find('.client').remove();
  };

  handleAlerts = function(el, msg) {
    $msg.find('.alert').remove(); 
    $msg.append(msg);
    $msg.find('.alert').alert();
    $msg.find('.alert').addClass('animated fadeIn');
    $('.alert').bind('closed.bs.alert', function () {
      $dni.focus();
    });
  };

})(jQuery)