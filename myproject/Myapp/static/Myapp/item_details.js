window.onload = function () {
    loadCart();
};
document.querySelectorAll('.cart-controls').forEach(control => {

    let addBtn = control.querySelector('.add-button');

    if (addBtn) {
        addBtn.addEventListener('click', () => {
            let itemId = control.dataset.id;
            addToCart(itemId, control);
        });
    }

});

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

/* ADD ITEM */
function addToCart(itemId, control) {

    fetch('/add-to-cart/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `item_id=${itemId}`
    })
    .then(res => res.json())
    .then(data => {
        renderQty(control, itemId, data.quantity);
        loadCart(); // refresh cart UI
    });
}

/* RENDER +/- UI */
function renderQty(control, itemId, quantity) {
    control.innerHTML = `
        <div class="qty-controller">
            <button class="qty-btn minus">-</button>
            <span class="qty-count">${quantity}</span>
            <button class="qty-btn plus">+</button>
        </div>
    `;

    control.querySelector('.plus').onclick = () => updateCart(itemId, "increase", control);
    control.querySelector('.minus').onclick = () => updateCart(itemId, "decrease", control);
}

/* UPDATE CART */
function updateCart(itemId, action, control) {

    fetch('/update-cart/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `item_id=${itemId}&action=${action}`
    })
    .then(res => res.json())
    .then(data => {

        if (data.status === "removed") {
            control.innerHTML = `<button class="add-button">Add To Cart</button>`;
            attachAddEvent(control);
        } else {
            control.querySelector('.qty-count').textContent = data.quantity;
        }

        loadCart(); // refresh cart UI
    });
}

function loadCart() {
    fetch('/get-cart/')
    .then(res => res.json())
    .then(data => {

        let cartContainer = document.getElementById("cartHolder");
        cartContainer.innerHTML = "";

        let total = 0;

        if (data.items.length === 0) {
            cartContainer.innerHTML = "<p>🛒 Your Cart is Currently Empty</p>";
            return;
        }

        data.items.forEach(item => {
            total += item.price * item.quantity;

            cartContainer.innerHTML += `
                <p>${item.name} × ${item.quantity} - ₹${item.price * item.quantity}</p>
            `;
        });

        cartContainer.innerHTML += `<hr><h4>Total: ₹${total}</h4>`;
    });
}

/* REATTACH ADD BUTTON */
function attachAddEvent(control) {
    control.querySelector('.add-button').onclick = () => {
        let itemId = control.dataset.id;
        addToCart(itemId, control);
    };
}