// Using event listener to scrape continuously

const SELECTOR = "a[href^='/marketplace/item/']";
let seen = new Set();


function logNew() {
    document.querySelectorAll(SELECTOR).forEach(a => {
        if (seen.has(a)) return;

        seen.add(a);
        console.log("--------");
        console.log(a.innerText)
    }
    )
}

//Run once for initial scraping
setTimeout(logNew, 2000);

window.addEventListener("scroll", () => {
    logNew();
})

//Idea for optimization: using Mutation Observer