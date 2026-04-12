let plusBtn = document.querySelectorAll(".plusBtn");

plusBtn.forEach(btn=>{
    btn.addEventListener("click",function(){
        let itemId = this.getAttribute('data-id');
        let csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;

        fetch(`/fetch_add_cart_item/${itemId}/`,{
            method: 'POST',
            headers:{
                "X-CSRFToken":csrf
            }
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById(`count${itemId}`).textContent = data.quantity;
            updateTotal();
        })
    })
})

let minusBtn = document.querySelectorAll(".minusBtn");

minusBtn.forEach(btn=>{
    btn.addEventListener("click",function(){
        let itemId = this.getAttribute('data-id');
        let csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;

        fetch(`/fetch_reduce_cart_item/${itemId}/`,{
            method: 'POST',
            headers:{
                "X-CSRFToken":csrf
            }
        })
        .then(res=>res.json())
        .then(data=>{
            document.getElementById(`count${itemId}`).textContent = data.quantity;
            if(data.quantity === 0){
                document.getElementById(`cartItem${itemId}`).remove();
            }
            updateTotal();
        });
    })
});


function updateTotal() {
    let total = 0;
    let countItems = 0;
    document.querySelectorAll(".qty-count").forEach(span => {
        let quantity = parseInt(span.textContent);

        let price = parseFloat(span.getAttribute("data-price"));

        total += quantity * price;
        countItems += 1;
    });
    document.getElementById("countItems").textContent = `(${countItems} items)`;
    document.getElementById("totalPrice").textContent = total;
}

updateTotal();