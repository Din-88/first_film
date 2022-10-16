let xhr_register = new XMLHttpRequest();

let elem_email = document.getElementById("email");
let elem_username = document.getElementById("username");

let email_check = document.getElementById("email_check");
let username_check = document.getElementById("username_check");

elem_email.addEventListener("blur", () => {
    if (elem_email.value.length > 5) {
        xhr_register.open("get", `/signup_check?email=${elem_email.value}`);
        xhr_register.send();
    }
}, false)

elem_username.addEventListener("blur", () => {
    if (elem_username.value.length > 3) {
        xhr_register.open("get", `/signup_check?username=${elem_username.value}`);
        xhr_register.send();
    }
}, false)

elem_email.addEventListener("focus", () => {
    email_check.style.visibility = "hidden"
}, false)

elem_username.addEventListener("focus", () => {
    username_check.style.visibility = "hidden"
}, false)


xhr_register.onload = function() {
    if (xhr_register.status != 200) 
    {
        console.log("rx Ошибка " + xhr_register.status + " " + xhr_register.statusText);
    } 
    else {
        let answer = xhr_register.responseText;

        if(answer === "email") {
            email_check.style.visibility = "visible";
        } else if (answer === "username") {
            username_check.style.visibility = "visible";
        }
    }
}