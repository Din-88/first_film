
let posters_preview = document.querySelectorAll(".poster_preview");
let main = document.getElementsByTagName("main")[0];
let shade = document.getElementsByClassName("overlay")[0];

let note = document.createElement('div');
note.className = "note";
note.position = "relative";
note.style.left = "0";
note.style.right = "0";
shade.appendChild(note);

function remove_img_scale_class(poster_img) {
    poster_img.classList.remove("img_scale");
    poster_img.style.cssText = "top: 0px;";
    document.body.style.overflow = "";
}

function change_size(poster_img, ev) {
    let client_width  = document.documentElement.clientWidth;
    let client_height = document.documentElement.clientHeight;
    let main_rect = main.getBoundingClientRect();
    let poster_rect = poster_img.getBoundingClientRect();

    if (poster_img.classList.contains("img_scale")) {
        remove_img_scale_class(poster_img);
        shade.classList.remove("shade_activ");
    } else {
        posters_preview.forEach((poster) => {
            remove_img_scale_class(poster.children[0]);
        });

        poster_img.classList.add("img_scale");

        // if (Math.min(client_width, client_height) < 685) {
        if (ev.sourceCapabilities.firesTouchEvents && client_width <= 1079) {
            document.body.style.overflow = "hidden";
            client_height = frames.outerHeight;

            shade.classList.add("shade_activ");
            let new_width = 0;
            let new_height = 0;
            let new_top = 0;

            if (client_width * 1.5 <= client_height) {
                new_width  = client_width;
                new_height = client_width * 1.5;
                new_top = -poster_rect.top + (client_height / 2) - (client_width * 1.5 / 2);
            } else {
                new_width  =  (client_height / 1.5);
                new_height =  client_height;                
                new_top = -poster_rect.top;
            }

            x = poster_rect.left + new_width;

            if ((poster_rect.left + new_width ) > main_rect.width) {
                var new_right = poster_rect.left + new_width - main_rect.width;
                poster_img.style.right = new_right + "px"
            }

            poster_img.style.width  = new_width + "px";
            poster_img.style.height = new_height + "px";
            poster_img.style.top    = new_top + "px"
        } else {
            if ( ((poster_rect.bottom + 150) > client_height) || 
                 ((poster_rect.bottom + 150) > main_rect.bottom))
            {
                poster_img.style.cssText = "top: -150px";
            }
        }
    }
}

posters_preview.forEach((poster) => {
    var poster_img = poster.children[0];

    poster_img.addEventListener("click", (ev) => {
        change_size(poster_img, ev);
    });

    poster_img.addEventListener("mouseenter", (ev) => {
        if (!ev.sourceCapabilities.firesTouchEvents) {
            change_size(poster_img, ev);
        }
    });

    poster_img.addEventListener("mouseleave", (ev) => {
        if (!ev.sourceCapabilities.firesTouchEvents) {
            remove_img_scale_class(poster_img);
        }
    });
});