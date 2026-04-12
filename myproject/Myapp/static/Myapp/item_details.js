document.addEventListener("DOMContentLoaded", () => {
    setupButtons();
    loadCart();
});

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

/* SETUP BUTTON */
function setupButtons() {
    document.querySelectorAll('.cart-controls').forEach(control => {

        control.onclick = (e) => {
            if (e.target.classList.contains('add-button')) {
                let itemId = control.dataset.id;
                addToCart(itemId, control);
            }
        };

    });
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
        loadCart();
    });
}

/* RENDER UI */
function renderQty(control, itemId, qty) {
    control.innerHTML = `
        <div class="qty-controller">
            <button class="minus">-</button>
            <span>${qty}</span>
            <button class="plus">+</button>
        </div>
    `;

    control.querySelector('.plus').onclick = () => updateCart(itemId, "increase", control);
    control.querySelector('.minus').onclick = () => updateCart(itemId, "decrease", control);
}

/* UPDATE */
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
        } else {
            control.querySelector('span').textContent = data.quantity;
        }

        loadCart();
    });
}

/* LOAD CART */
function loadCart() {

    fetch('/get-cart/')
    .then(res => res.json())
    .then(data => {

        let cartBox = document.getElementById("cartHolder");
        cartBox.innerHTML = "";

        let total = 0;

        if (data.items.length === 0) {
            cartBox.innerHTML = "🛒 Empty Cart";
            return;
        }

        data.items.forEach(item => {
            total += item.price * item.quantity;

            cartBox.innerHTML += `
                <p>${item.name} × ${item.quantity}</p>
            `;

            // 🔥 sync button
            let control = document.querySelector(`.cart-controls[data-id="${item.id}"]`);
            if (control) renderQty(control, item.id, item.quantity);
        });

        cartBox.innerHTML += `<hr>Total: ₹${total}`;
    });
}