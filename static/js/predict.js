// This file runs on the symptom-selection (predict) page.
// It does two simple things:
//   1. Turns the plain <select> into a searchable dropdown (Select2).
//   2. Keeps the "X symptoms selected" counter text up to date.

$(document).ready(function () {

    // 1. Set up the searchable symptom dropdown
    $('#symptoms').select2({
        placeholder: 'Type to search symptoms...',
        allowClear: true,
        width: '100%'
    });

    // 2. Update the counter text whenever the selection changes
    const counterBox = document.getElementById('selected-count');

    function updateCounter() {
        const selected = $('#symptoms').val() || []; // array of selected values
        const count = selected.length;

        if (count === 0) {
            counterBox.textContent = '0 symptoms selected';
        } else if (count === 1) {
            counterBox.textContent = '1 symptom selected';
        } else {
            counterBox.textContent = count + ' symptoms selected';
        }
    }

    // Run once on page load, then every time the dropdown changes
    updateCounter();
    $('#symptoms').on('change', updateCounter);

});
