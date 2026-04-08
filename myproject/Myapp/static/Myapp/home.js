let navbar = document.getElementById("navBar");
let navOption = document.querySelectorAll('.nav-option')
window.addEventListener("scroll",()=>{
    if(window.scrollY>10){
        navbar.classList.add("scrolled");
        navOption.forEach(el => el.classList.add('scrolled'));
    }else{
        navbar.classList.remove("scrolled")
        navOption.forEach(el => el.classList.remove('scrolled'));
    }
})
