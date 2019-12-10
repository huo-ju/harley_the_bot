//(function($){
//  $(function(){
//
//    $('.sidenav').sidenav();
//
//  }); // end of document ready
//})(jQuery); // end of jQuery name space


  document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, {edge:'left'});

    var elems = document.querySelectorAll('.dropdown-trigger');
    var instances = M.Dropdown.init(elems, {edge:'left'});
  });

