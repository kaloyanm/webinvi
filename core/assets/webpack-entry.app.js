// Semantic UI Components
import $ from 'jquery';
window.jQuery = $;
window.$ = $;

import 'semantic-ui-sass/js/dimmer';
import 'semantic-ui-sass/js/transition';
import 'semantic-ui-sass/js/api';
import 'semantic-ui-sass/js/search';
import 'semantic-ui-sass/js/state';
import '../../invoices/assets/js/app.js';


/* Custom API endpoints */
$.fn.api.settings.api = {
  'autocomplete' : '/invoices/autocomplete/?f={field}&k={query}',
  'autocomplete-client' : '/invoices/autocomplete/client/?k={query}'
};

function makeItSearchable(element, field) {
    $(element).search({
        minCharacters : 0,
        apiSettings: {
            action: 'autocomplete',
            method: 'GET',
            urlData: {
                field: field
            }
        }
    });
}

function input2search(obj) {
    obj.addClass('prompt');
    obj.parent().addClass('ui').addClass('search');
    obj.parent().append('<div class="results"></div>');
    return obj;
}

$('.searchable-invoice').each(function() {
    var el = input2search($(this));
    makeItSearchable(el.parent(), el.attr("name"));
});


$('.searchable-client').each(function () {
    var clickMap = {};
    var el = input2search($(this));
        el.on('input', function () {
            var sourceData = clickMap[$(this).val()] || false;
            if (sourceData)
                $('.searchable-client-fill').each(function () {
                    var field_name = $(this).attr('name');
                    $(this).val(sourceData[field_name]);
                })
        });

    $(el.parent()).search({
        minCharacters : 0,
        apiSettings: {
            action: 'autocomplete-client',
            method: 'GET',
            onResponse: function (serverResponse) {
                var
                    response = {
                        results : []
                    };

                $.each(serverResponse.results, function (index, item) {
                    response.results.push({title: item.title});
                    clickMap[item.title] = item;
                });
                return response;
            }
        },
        onSelect: function (event) {
            setTimeout(function () {
                el.trigger('input');
            }, 100);
        }
    });

});
