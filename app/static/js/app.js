document.addEventListener("DOMContentLoaded", () => {
    console.log("🚗 OtoTrend AI CMS yüklendi.");

    const refreshButton = document.getElementById("refreshNews");

    if (refreshButton) {
        refreshButton.addEventListener("click", () => {
            location.reload();
        });
    }
});