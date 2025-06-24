console.log("🔥 FlipSensei script injected 🔥");


// Since Facebook has multiple nested divs and dynamic class names, must find another way to scrape:
setTimeout(() => {
    const items = document.querySelectorAll("a[href^='/marketplace/item/']"); //Scrapes all the items with the a tag and corresponding href
    console.log("Found ${items.length} items!") //prints amount of items scraped
    items.forEach(el => {
        console.log("--------");
        console.log(el.innerText);
    })}, 3000);

console.log("FlipSensei Script Loaded!");