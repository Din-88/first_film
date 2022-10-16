const menu_button = document.getElementById("menu_button")
const first_nav_mobile = document.getElementById("first_nav")
let is_open = 0

menu_button.addEventListener("click", (ev) => {
    first_nav_mobile.classList.toggle("first_nav_activ")
    if(!is_open) {
        menu_button.innerText = "✕"
        is_open = 1
    } else {
        menu_button.innerText = "☰"
        is_open = 0
    }
})


var second_nav_httpr = new XMLHttpRequest()
var second_nav_items = document.querySelectorAll(".second_nav_item")

second_nav_items.forEach((second_nav_item) => {
    var url = "/second_nav/" + second_nav_item.id;

    second_nav_httpr.open("get", url, false)
    try {
        second_nav_httpr.send()
    
        if (second_nav_httpr.status != 200) {
            alert(`Ошибка ${second_nav_httpr.status}: ${second_nav_httpr.statusText}`);
        } else {
            response = second_nav_httpr.responseText
            second_nav_item.insertAdjacentHTML("beforeend", response)
        }
    } catch(err) {
        alert("Запрос не удался");
    }

    var sub = second_nav_item.children[0]

    second_nav_item.addEventListener("click", (ev) => {
        sub.classList.toggle("second_nav_activ")
    })

    second_nav_item.addEventListener("mouseenter", (ev) => {
        if (!ev.sourceCapabilities.firesTouchEvents){                
            sub.classList.toggle("second_nav_activ")
        }
    })

    second_nav_item.addEventListener("mouseleave", (ev) => {
        sub.classList.remove("second_nav_activ")
    })
})