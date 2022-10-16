let butt_more_reviews = document.getElementById("more_reviews");
let xhr_reviews = new XMLHttpRequest()
let review_page = 1

let reviews_block = document.getElementById("reviews_block");


function more_reviews(film_id) {
    url = `/more_reviews/${film_id}/${review_page}`
    xhr_reviews.open("get", url, true)
    xhr_reviews.send()
}

xhr_reviews.onload = function() {
    if (xhr_reviews.status != 200) {
        console.log("rx Ошибка " + xhr_reviews.status + " " + xhr_reviews.statusText);
    } 
    else {
        responseText = xhr_reviews.responseText;
        reviews_block.lastElementChild.insertAdjacentHTML('beforebegin', responseText);
        review_page += 1;
    }
}