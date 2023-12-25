navbar = document.getElementById('navbar');

btns = document.getElementById('nav-btn')

function changeClass(){
    navbar.classList.toggle('active');
}


btns.addEventListener("click", changeClass)