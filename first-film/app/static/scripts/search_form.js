const search_div = document.getElementById("search");
const search_form = document.getElementById("search_form");
const search = document.getElementById("search_text");
const result = document.getElementById("search_result");

const xhr = new XMLHttpRequest();

search_form.addEventListener("input", () => {
    f = new FormData(search_form);
    xhr.open("post", "/search");
    xhr.send(f);
}, false);


search_form.addEventListener("submit", (ev) => {
    if (result.innerHTML === "") {
        ev.preventDefault();
    } else {
        length = parseInt(result.firstChild.value);
        console.log("asd");
        if (length === NaN || length < 1) {
            ev.preventDefault();
        }
    }
}, false);


xhr.onload = function() {
    if (xhr.status != 200) {
        console.log("rx Ошибка " + xhr.status + " " + xhr.statusText);
    } else {
        answer = xhr.responseText;

        if (answer.length < 1) {
            result.style.visibility = "hidden";
        } 
        else {            
            result.innerHTML = answer;
        }

        console.log("rx " + answer);
    }
}