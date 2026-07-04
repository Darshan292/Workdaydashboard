/*
==========================================================
Enterprise Theme Manager
==========================================================
*/

(function () {

    "use strict";

    // ======================================================
    // Theme Storage
    // ======================================================

    const STORAGE_KEY = "workday-dashboard-theme";

    // ======================================================
    // Get Theme
    // ======================================================

    function getTheme() {

        return localStorage.getItem(STORAGE_KEY) || "dark";

    }

    // ======================================================
    // Save Theme
    // ======================================================

    function saveTheme(theme) {

        localStorage.setItem(

            STORAGE_KEY,

            theme

        );

    }

    // ======================================================
    // Apply Theme
    // ======================================================

    function applyTheme(theme) {

        const root = document.body;

        root.classList.remove(

            "dark-theme",

            "light-theme"

        );

        root.classList.add(

            theme + "-theme"

        );

        saveTheme(theme);

    }

    // ======================================================
    // Toggle
    // ======================================================

    function toggleTheme() {

        const current = getTheme();

        const next =

            current === "dark"

                ? "light"

                : "dark";

        applyTheme(next);

        updateToggleButton(next);

    }

    // ======================================================
    // Button
    // ======================================================

    function updateToggleButton(theme) {

        const button = document.getElementById(

            "theme-toggle"

        );

        if (!button)

            return;

        if (theme === "dark") {

            button.innerHTML =

                '<i class="fa-solid fa-moon"></i> Dark';

        }

        else {

            button.innerHTML =

                '<i class="fa-solid fa-sun"></i> Light';

        }

    }

    // ======================================================
    // Plotly Theme
    // ======================================================

    function refreshCharts() {

        const graphs =

            document.querySelectorAll(

                ".js-plotly-plot"

            );

        graphs.forEach(

            function (graph) {

                window.dispatchEvent(

                    new Event(

                        "resize"

                    )

                );

            }

        );

    }

    // ======================================================
    // Initial
    // ======================================================

    document.addEventListener(

        "DOMContentLoaded",

        function () {

            const theme = getTheme();

            applyTheme(theme);

            updateToggleButton(theme);

            refreshCharts();

        }

    );

    // ======================================================
    // Toggle Button
    // ======================================================

    document.addEventListener(

        "click",

        function (event) {

            if (

                event.target.id === "theme-toggle"

            ) {

                toggleTheme();

                refreshCharts();

            }

        }

    );

    // ======================================================
    // Listen Storage
    // ======================================================

    window.addEventListener(

        "storage",

        function (event) {

            if (

                event.key === STORAGE_KEY

            ) {

                applyTheme(

                    event.newValue

                );

                refreshCharts();

            }

        }

    );

})();