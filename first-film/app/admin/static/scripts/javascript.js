let div_content = document.getElementById("content");

let httpr = new XMLHttpRequest();
httpr.timeout = 10000;

function get_models(name, page) {
    url = `/admin/view?name=${name}&page=${page}`;
    httpr.open("get", url);
    httpr.send();
}

httpr.onload = function() {
    if (httpr.status != 200)
    {
        console.log("rx Ошибка " + httpr.status + " " + httpr.statusText);
    } 
    else {
        answer = httpr.responseText;
        div_content.children[0].innerHTML = answer;
        console.log("rx " + answer);
    }
}
