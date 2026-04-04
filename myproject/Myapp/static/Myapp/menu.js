let navbar = document.getElementById("navBar");
window.addEventListener("scroll",()=>{
    if(window.scrollY>10){
        navbar.classList.add("scrolled");
    }else{
        navbar.classList.remove("scrolled")
    }
})
