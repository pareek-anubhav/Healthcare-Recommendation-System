// This file runs on the result page.
// It swaps which prediction's detail panel is visible when the
// user clicks one of the 3 rank tabs (🥇 🥈 🥉) at the top.

document.addEventListener('DOMContentLoaded', function () {

    const tabs = document.querySelectorAll('.rank-tab');
    const panels = document.querySelectorAll('.detail-panel');

    tabs.forEach(function (tab) {

        tab.addEventListener('click', function () {

            const targetId = tab.getAttribute('data-target');

            // Step 1: turn every tab "off" and every panel "hidden"
            tabs.forEach(function (t) {
                t.classList.remove('rank-tab--active');
            });

            panels.forEach(function (p) {
                p.classList.remove('detail-panel--active');
            });

            // Step 2: turn "on" only the clicked tab and its matching panel
            tab.classList.add('rank-tab--active');
            document.getElementById(targetId).classList.add('detail-panel--active');

        });

    });

});
