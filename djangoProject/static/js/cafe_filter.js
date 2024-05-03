function filterItems() {
    const filterValue = document.getElementById("type-filter").value;


    const cards = document.querySelectorAll(".cafecard");
    cards.forEach(card => {
        const type = card.getAttribute("data-type");
        if (filterValue === "all" || filterValue === type) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    });
}