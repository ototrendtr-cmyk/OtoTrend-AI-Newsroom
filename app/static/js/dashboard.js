// ============================================
// OtoTrend AI CMS
// Dashboard JS
// ============================================

document.addEventListener("DOMContentLoaded", () => {

    console.log("✅ Dashboard yüklendi.");

    initTooltips();

    initRefreshButton();

    initCharts();

});


// ============================================
// Bootstrap Tooltips
// ============================================

function initTooltips() {

    const tooltipTriggerList = document.querySelectorAll(
        '[data-bs-toggle="tooltip"]'
    );

    [...tooltipTriggerList].map(

        tooltip => new bootstrap.Tooltip(tooltip)

    );

}


// ============================================
// Haberleri Yenile
// ============================================

function initRefreshButton() {

    const button = document.querySelector("#refreshNews");

    if (!button) return;

    button.addEventListener("click", () => {

        button.disabled = true;

        button.innerHTML = `
            <span class="spinner-border spinner-border-sm"></span>
            Güncelleniyor...
        `;

        location.reload();

    });

}


// ============================================
// Chart
// ============================================

function initCharts() {

    const canvas = document.getElementById("newsChart");

    if (!canvas) return;

    if (typeof Chart === "undefined") {

        console.log("Chart.js henüz eklenmedi.");

        return;

    }

    new Chart(canvas, {

        type: "line",

        data: {

            labels: [

                "Pzt",
                "Sal",
                "Çar",
                "Per",
                "Cum",
                "Cmt",
                "Paz"

            ],

            datasets: [

                {

                    label: "Haber",

                    data: [12, 18, 9, 20, 15, 24, 13],

                    borderWidth: 3,

                    tension: .4,

                    fill: false

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false

                }

            }

        }

    });

}