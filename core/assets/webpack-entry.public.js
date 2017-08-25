import $ from 'jquery';
window.jQuery = $;
window.$ = $;

import 'semantic-ui-sass/js/api';
//import 'semantic-ui-sass/js/colorize';
import 'semantic-ui-sass/js/form';
import 'semantic-ui-sass/js/state';
import 'semantic-ui-sass/js/visibility';
//import 'semantic-ui-sass/js/visit';
import 'semantic-ui-sass/js/site';
//import 'semantic-ui-sass/js/accordion';
import 'semantic-ui-sass/js/checkbox';
import 'semantic-ui-sass/js/dimmer';
import 'semantic-ui-sass/js/dropdown';
//import 'semantic-ui-sass/js/embed';
//import 'semantic-ui-sass/js/modal';
//import 'semantic-ui-sass/js/nag';
//import 'semantic-ui-sass/js/popup';
//import 'semantic-ui-sass/js/progress';
//import 'semantic-ui-sass/js/rating';
//import 'semantic-ui-sass/js/search';
//import 'semantic-ui-sass/js/shape';
import 'semantic-ui-sass/js/sidebar';
import 'semantic-ui-sass/js/sticky';
//import 'semantic-ui-sass/js/tab';
import 'semantic-ui-sass/js/transition';

import './scss/style.scss';

$(document).ready(function() {
  // fix main menu to page on passing
  $('#main-menu').visibility({
    type: 'fixed'
  });

  // create sidebar and attach to menu open
  $('#mobile-menu').sidebar('attach events', '.menu-toc');

  // show dropdown on hover
  $('#menu-dropdown').dropdown({
    on: 'click'
  });

});

