import 'svgxuse';
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

var $body = $(document.body);
var $doc = $(document);
var $window = $(window);
var $mainMenu = $('#main-menu');
var isHome = $body.hasClass('page--home');
var scrollTop = $window.scrollTop();
var latestKnownScrollY = 0;
var ticking = false;

if (!isHome) {
  $mainMenu.visibility({
    type: 'fixed'
  });
}

if (isHome && scrollTop === 0) {
  $mainMenu.removeClass('menu--solid').addClass('menu--transparent');
}

if (isHome && scrollTop !== 0) {
  $mainMenu.removeClass('menu--transparent').addClass('menu--solid');
}

if (isHome) {
  $doc.scroll(function() {
    latestKnownScrollY = $window.scrollTop();
    requestTick();
  });
}

function updateMenu() {
  ticking = false;
  var currentScrollY = latestKnownScrollY;

  if (currentScrollY === 0 && $mainMenu.hasClass('menu--transparent') === false) {
    $mainMenu.removeClass('menu--solid').addClass('menu--transparent');
    return;
  }

  if (currentScrollY > 0 && $mainMenu.hasClass('menu--solid') === false) {
    $mainMenu.removeClass('menu--transparent').addClass('menu--solid');
  }
}

function requestTick() {
  if(!ticking) {
    requestAnimationFrame(updateMenu);
  }
  ticking = true;
}

// create sidebar and attach to menu open
$('#mobile-menu').sidebar('attach events', '.menu-toc');


$('.dropdown').dropdown({
  on: 'click'
});

$('#sticky-settings').sticky({context: '#invoice_app'});

