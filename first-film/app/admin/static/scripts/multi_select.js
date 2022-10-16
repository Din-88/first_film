let text_areas = document.querySelectorAll(".textarea");

text_areas.forEach(text_area => {
    let ul = text_area.nextElementSibling;
    let li = text_area.nextElementSibling.childNodes; //.firstChild
    
    let text_area_value = ""
    li.forEach(l => {
        let check_box = l.children[0]
        let lable = l.children[1]

        if (check_box.checked)
        {
            text_area_value += lable.innerText + "\n";
        }
        
        check_box.addEventListener("change", (ev) => {
            if (check_box.checked) {
                text_area.value = text_area.value + "\n" + lable.innerText;
            } else {
                let index = text_area.value.indexOf(lable.innerText);
                if (index > -1) {
                    text_area.value = text_area.value.replace(lable.innerText, '');
                }
            }
            // text_area.value = text_area.value.replace(/\s+/g,' ').trim()
            text_area.value = text_area.value.replace(/\n{2,}/g, "\n").trim()
            // text_area.value = text_area.value.trim()
            console.log(text_area.value);
        });
    })
    text_area.value = text_area_value;    
    text_area.defaultValue = text_area_value

    text_area.style.height = "auto";
    text_area.style.height = (text_area.scrollHeight) + "px";
});