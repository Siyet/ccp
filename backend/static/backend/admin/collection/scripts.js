(function ($) {
    $(document).ready(function () {
        const contrastDetailsCheck = $("#id_contrast_details");
        if (!contrastDetailsCheck.length) {
            return
        }
        toggleWhiteFabric(!contrastDetailsCheck.prop('checked'));
        contrastDetailsCheck.change(function () {
            toggleWhiteFabric(!this.checked);
        });
    });

    function toggleWhiteFabric(show) {
        $("div.white_fabric").toggle(show);
    }
})('django' in window && django.jQuery ? django.jQuery : jQuery);