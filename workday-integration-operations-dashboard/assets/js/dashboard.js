/*
==========================================================
Enterprise Dashboard Controller
==========================================================
*/

(function () {

    "use strict";

    // ======================================================
    // Resize Plotly Charts
    // ======================================================

    function resizeCharts() {

        const charts =

            document.querySelectorAll(

                ".js-plotly-plot"

            );

        charts.forEach(

            function (chart) {

                if (

                    window.Plotly

                ) {

                    Plotly.Plots.resize(

                        chart

                    );

                }

            }

        );

    }

    // ======================================================
    // Window Resize
    // ======================================================

    window.addEventListener(

        "resize",

        function () {

            resizeCharts();

        }

    );

    // ======================================================
    // Sidebar
    // ======================================================

    function toggleSidebar() {

        const sidebar =

            document.getElementById(

                "sidebar"

            );

        if (!sidebar)

            return;

        sidebar.classList.toggle(

            "collapsed"

        );

        setTimeout(

            resizeCharts,

            350

        );

    }

    // ======================================================
    // Smooth Scroll
    // ======================================================

    document.querySelectorAll(

        "a[href^='#']"

    ).forEach(

        function (anchor) {

            anchor.addEventListener(

                "click",

                function (e) {

                    e.preventDefault();

                    const target =

                        document.querySelector(

                            this.getAttribute(

                                "href"

                            )

                        );

                    if (

                        target

                    ) {

                        target.scrollIntoView(

                            {

                                behavior:"smooth",

                                block:"start"

                            }

                        );

                    }

                }

            );

        }

    );

    // ======================================================
    // Auto Refresh Indicator
    // ======================================================

    function refreshAnimation() {

        const icon =

            document.getElementById(

                "refresh-icon"

            );

        if (

            !icon

        ) return;

        icon.classList.add(

            "spin"

        );

        setTimeout(

            function(){

                icon.classList.remove(

                    "spin"

                );

            },

            900

        );

    }

    // ======================================================
    // Fullscreen Charts
    // ======================================================

    function registerFullscreen() {

        document.querySelectorAll(

            ".fullscreen-btn"

        ).forEach(

            function(btn){

                btn.onclick=function(){

                    const card=

                        btn.closest(

                            ".dashboard-card"

                        );

                    if(

                        !document.fullscreenElement

                    ){

                        card.requestFullscreen();

                    }

                    else{

                        document.exitFullscreen();

                    }

                    resizeCharts();

                };

            }

        );

    }

    // ======================================================
    // Toast Auto Close
    // ======================================================

    function dismissToasts(){

        const toasts=

            document.querySelectorAll(

                ".toast"

            );

        toasts.forEach(

            function(t){

                setTimeout(

                    function(){

                        t.classList.remove(

                            "show"

                        );

                    },

                    5000

                );

            }

        );

    }

    // ======================================================
    // Keyboard Shortcuts
    // ======================================================

    document.addEventListener(

        "keydown",

        function(e){

            if(

                e.key==="r"

                &&

                e.ctrlKey

            ){

                e.preventDefault();

                refreshAnimation();

            }

            if(

                e.key==="b"

                &&

                e.ctrlKey

            ){

                e.preventDefault();

                toggleSidebar();

            }

        }

    );

    // ======================================================
    // Mutation Observer
    // ======================================================

    const observer=

        new MutationObserver(

            function(){

                resizeCharts();

                registerFullscreen();

                dismissToasts();

            }

        );

    observer.observe(

        document.body,

        {

            childList:true,

            subtree:true

        }

    );

    // ======================================================
    // Initial
    // ======================================================

    window.addEventListener(

        "load",

        function(){

            resizeCharts();

            registerFullscreen();

            dismissToasts();

        }

    );

})();