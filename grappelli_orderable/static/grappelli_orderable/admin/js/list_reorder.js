(function ($) {
    $(function () {
        const paginated = $(".grp-pagination span.this-page").length > 0;
        if (paginated) {
            return;
        }

        const rows = $('.grp-changelist-results tbody tr');

        populateIdentifiers(rows);
        adjustAppearance(rows);

        $('.grp-changelist-results tbody').sortable({
            axis: 'y',
            items: 'tr',
            cursor: 'move',
            update: orderUpdated
        });

        // Broken table fix. Seems to collide with internal css.
        $('tbody.ui-sortable').removeClass('ui-sortable');
    });


    function orderUpdated(sorted) {
        var cereal = $(this).sortable("serialize");
        cereal += '&csrfmiddlewaretoken=' + $("input[name=csrfmiddlewaretoken]").val();

        // Update row classes
        $(this).find('tr').removeClass('grp-row-even').removeClass('grp-row-odd');
        $(this).find('tr:even').addClass('grp-row-even');
        $(this).find('tr:odd').addClass('grp-row-odd');

        $.post("reorder/", cereal);
    }


    function adjustAppearance(rows) {
        rows.css('cursor', 'move');

        rows.find("> *").each(function () {
            $(this).width($(this).width())
        });
    }

    function populateIdentifiers(rows) {
        const pathPattern = window.location.pathname + "([0-9]+)/$";
        const urlMatcher = RegExp(pathPattern, "");
        rows.each(function () {
            const id = $("a", this).map(function () {
                const matches = urlMatcher.exec(this.href);
                return matches ? matches[1] : null;
            }).first().get();
            this.id = "neworder_" + id;
        });
    }
})(django.jQuery);