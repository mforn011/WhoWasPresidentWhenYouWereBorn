var menu = document.getElementById('top-right');
var offset = menu.offsetTop;

window.onscroll = function () {
    if (window.scrollY > offset) {
        menu.classList.add("menu-fixed");
    } else {
        menu.classList.remove("menu-fixed");
    }
}