// Semantic UI Components
import 'semantic-ui-sass/js/modal';
import 'semantic-ui-sass/js/dimmer';
import 'semantic-ui-sass/js/transition';

import '../../invoices/assets/js/app.js';

$('#delete-invoice').on('click', function() {
  $('#delete-invoice-modal').modal({duration: 150}).modal('show');
});

$('.change-company')
  .on('click', function() {
    alert("Company Change");
  });
