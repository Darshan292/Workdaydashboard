/*
==========================================================
Enterprise Animation Engine
==========================================================
*/

(function () {

    "use strict";

    // =====================================================
    // Fade Sections
    // =====================================================

    function revealSections() {

        const sections = document.querySelectorAll(

            ".dashboard-section"

        );

        const observer = new IntersectionObserver(

            function(entries){

                entries.forEach(

                    function(entry){

                        if(entry.isIntersecting){

                            entry.target.classList.add(

                                "fade-in"

                            );

                        }

                    }

                );

            },

            {

                threshold:0.15

            }

        );

        sections.forEach(

            function(section){

                observer.observe(

                    section

                );

            }

        );

    }

    // =====================================================
    // KPI Counter Animation
    // =====================================================

    function animateCounter(

        element,

        endValue,

        duration

    ){

        let start = 0;

        const increment =

            endValue /

            (duration / 16);

        function update(){

            start += increment;

            if(start >= endValue){

                element.innerText =

                    endValue.toLocaleString();

                return;

            }

            element.innerText =

                Math.floor(

                    start

                ).toLocaleString();

            requestAnimationFrame(

                update

            );

        }

        update();

    }

    function animateKPIs(){

        document.querySelectorAll(

            ".kpi-value"

        ).forEach(

            function(kpi){

                const value = parseFloat(

                    kpi.dataset.value

                );

                if(

                    !isNaN(value)

                ){

                    animateCounter(

                        kpi,

                        value,

                        900

                    );

                }

            }

        );

    }

    // =====================================================
    // Hover Lift
    // =====================================================

    function attachHover(){

        document.querySelectorAll(

            ".dashboard-card"

        ).forEach(

            function(card){

                card.addEventListener(

                    "mouseenter",

                    function(){

                        card.classList.add(

                            "hover-lift"

                        );

                    }

                );

                card.addEventListener(

                    "mouseleave",

                    function(){

                        card.classList.remove(

                            "hover-lift"

                        );

                    }

                );

            }

        );

    }

    // =====================================================
    // Refresh Pulse
    // =====================================================

    function pulseRefresh(){

        const button =

            document.getElementById(

                "refresh-button"

            );

        if(!button) return;

        button.addEventListener(

            "click",

            function(){

                button.classList.add(

                    "pulse"

                );

                setTimeout(

                    function(){

                        button.classList.remove(

                            "pulse"

                        );

                    },

                    1200

                );

            }

        );

    }

    // =====================================================
    // Staggered Animation
    // =====================================================

    function staggerCharts(){

        document.querySelectorAll(

            ".dashboard-card"

        ).forEach(

            function(card,index){

                card.style.animationDelay =

                    (index*0.05)+"s";

            }

        );

    }

    // =====================================================
    // Mutation Observer
    // =====================================================

    const observer =

        new MutationObserver(

            function(){

                revealSections();

                animateKPIs();

                attachHover();

                pulseRefresh();

                staggerCharts();

            }

        );

    observer.observe(

        document.body,

        {

            childList:true,

            subtree:true

        }

    );

    // =====================================================
    // Initial
    // =====================================================

    window.addEventListener(

        "load",

        function(){

            revealSections();

            animateKPIs();

            attachHover();

            pulseRefresh();

            staggerCharts();

        }

    );

})();