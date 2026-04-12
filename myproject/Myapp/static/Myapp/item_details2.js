let increaseButton = document.getElementById("increaseButton");

increaseButton.addEventListener("click", function() {
    let itemId = this.getAttribute("data-id");
    let csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;

    fetch(`/fetch_add_cart_item/${itemId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrf
        }
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("itemCount").textContent = data.quantity;
    });
});

let reduceButton = document.getElementById("reduceButton");

reduceButton.addEventListener("click", function() {
    let itemId = this.getAttribute("data-id");
    let csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;

    fetch(`/fetch_reduce_cart_item/${itemId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrf
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.quantity === 0) {
            let qtyController = document.getElementById("qtyController");
            qtyController.style.display = "none";
            document.getElementById("addButton").classList.remove("hidden");
        }
        document.getElementById("itemCount").textContent = data.quantity;
    });
});