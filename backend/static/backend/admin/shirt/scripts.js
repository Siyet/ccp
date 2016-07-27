(function ($) {
    $(document).ready(function () {
        const sleeveSelect = $("#id_sleeve");
        toggleCuffs(sleeveSelect.val());
        sleeveSelect.change(function () {
            toggleCuffs(this.value)
        });
    });

    function toggleCuffs(sleeveId) {
        $.get('show_cuffs/' + sleeveId + '/', function (useCuffs) {
            const group = $("#cuff-group");
            group.toggle(JSON.parse(useCuffs));
        });
    }
})('django' in window && django.jQuery ? django.jQuery : jQuery);