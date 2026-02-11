
document.addEventListener("DOMContentLoaded", function () {
    const filterBtns = document.querySelectorAll(".filter-btn");
    const projectItems = document.querySelectorAll(".grid-item, .card-item");
    const grid = document.querySelector(".grid");

    filterBtns.forEach((btn) => {
        btn.addEventListener("click", () => {
            // Remove active class from all buttons
            filterBtns.forEach((b) => b.classList.remove("active"));
            // Add active class to clicked button
            btn.classList.add("active");

            const category = btn.getAttribute("data-filter").trim();

            projectItems.forEach((item) => {
                const itemCategories = item.getAttribute("data-category");
                let itemCategoryList = [];

                try {
                    const parsed = JSON.parse(itemCategories);
                    // Handle both single string and array of strings
                    if (Array.isArray(parsed)) {
                        itemCategoryList = parsed;
                    } else {
                        itemCategoryList = [parsed];
                    }
                } catch (e) {
                    console.log("JSON parse error for:", itemCategories, e);
                    // Fallback for single-quoted arrays or raw strings
                    if (itemCategories) {
                        try {
                            const repaired = itemCategories.replace(/'/g, '"');
                            const parsedRepaired = JSON.parse(repaired);
                            if (Array.isArray(parsedRepaired)) {
                                itemCategoryList = parsedRepaired;
                            } else {
                                itemCategoryList = [parsedRepaired];
                            }
                        } catch (e2) {
                            let cleanCat = itemCategories.trim();
                            if (cleanCat.startsWith('"') && cleanCat.endsWith('"')) cleanCat = cleanCat.slice(1, -1);
                            itemCategoryList = [cleanCat];
                        }
                    }
                }

                // Ensure strings are trimmed
                itemCategoryList = itemCategoryList.map(c => String(c).trim());

                if (category === "all" || itemCategoryList.includes(category)) {
                    item.style.display = null;
                } else {
                    item.style.display = "none";
                }
            });

            // Re-layout Masonry if it exists and we are in grid mode
            if (grid && window.Masonry) {
                // We need to wait a tiny bit for the display changes to apply? 
                // Or just call layout. 
                // Often Masonry needs to be notified of item removal/addition, 
                // but here we are just hiding valid items. 
                // 'layout' method lays out all item elements.

                // Check if masonry instance exists on the grid element
                // accepted way to get masonry instance if initialized via data attributes or jQuery
                var msnry = Masonry.data(grid);
                if (msnry) {
                    msnry.layout();
                }
            }
        });
    });
});
