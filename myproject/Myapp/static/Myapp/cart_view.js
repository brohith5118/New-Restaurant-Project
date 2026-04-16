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
            updateItemTotal();
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
            updateItemTotal();
        });
    })
});

function updateItemTotal() {
    document.querySelectorAll(".qty-count").forEach(span => {
        let quantity = parseInt(span.textContent);
        let price = parseFloat(span.getAttribute("data-price"));
        let itemId = span.getAttribute("data-id");
        let itemTotal = quantity * price;
        document.getElementById(`itemTotal${itemId}`).textContent = `₹${itemTotal}`;
    });
}

function updateTotal() {
    let total = 0;
    let totalItems = 0;

    document.querySelectorAll(".qty-count").forEach(span => {
        let quantity = parseInt(span.textContent);
        let price = parseFloat(span.getAttribute("data-price"));

        total += quantity * price;
        totalItems += quantity; // ✅ FIXED
    });

    document.getElementById("countItems").textContent = `(${totalItems} items)`;
    document.getElementById("summaryItems").textContent = totalItems;
    document.getElementById("totalPrice").textContent = total;
}

updateTotal();
updateItemTotal();