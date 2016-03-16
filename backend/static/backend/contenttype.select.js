/**
 * Created by strange on 16.03.16.
 */

(function($){
    $.fn.contentTypeSelect = function(){
        return this.each(function(i) {
            buildSelector($(this));
        });
    };

    buildSelector = function(element){
        element.on('change', function() {
            console.log($(this).val());
            element.prop('disabled', 'disabled');
            var data = {
                pk: element.val()
            };
            $.getJSON(element.data('url'), data, function(obj) {
                var select = $('#'+element.data('field'));
                select.html('<option value=""></option>');
                for (var i=0; i<obj.length; i++) {
                    select.append('<option value="'+obj[i][0]+'">'+obj[i][1]+'</option>');
                }
                element.prop('disabled', false);
            });
        });
    };

})('django' in window && django.jQuery ? django.jQuery : jQuery);
