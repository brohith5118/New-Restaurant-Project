// 🔹 CSRF helper
function getCSRF() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}

// =====================
// ✅ ADD BUTTON
// =====================
document.querySelectorAll(".addButton").forEach(btn => {
    btn.addEventListener("click", function () {
        let itemId = this.dataset.id;

        fetch(`/fetch_add_cart_item/${itemId}/`, {
            method: "POST",
            headers: { "X-CSRFToken": getCSRF() }
        })
        .then(res => res.json())
        .then(data => {
            updateAll(itemId, data.quantity, data.price, data.name);
        });
    });
});

// =====================
// ✅ ITEM SECTION (+ / -)
// =====================
document.querySelectorAll(".increaseButton, .reduceButton").forEach(btn => {
    btn.addEventListener("click", function () {
        let itemId = this.dataset.id;
        let url = this.classList.contains("increaseButton")
            ? `/fetch_add_cart_item/${itemId}/`
            : `/fetch_reduce_cart_item/${itemId}/`;

        fetch(url, {
            method: "POST",
            headers: { "X-CSRFToken": getCSRF() }
        })
        .then(res => res.json())
        .then(data => {
            if (data.quantity === 0) {
                removeItem(itemId);
            } else {
                updateAll(itemId, data.quantity, data.price, data.name);
            }
        });
    });
});

// =====================
// ✅ CART SECTION (EVENT DELEGATION)
// =====================
document.getElementById("cartHolder").addEventListener("click", function (e) {

    let btn = e.target;
    let itemId = btn.dataset.id;

    if (!itemId) return;

    let url = btn.classList.contains("cartIncreaseButton")
        ? `/fetch_add_cart_item/${itemId}/`
        : btn.classList.contains("cartReduceButton")
        ? `/fetch_reduce_cart_item/${itemId}/`
        : null;

    if (!url) return;

    fetch(url, {
        method: "POST",
        headers: { "X-CSRFToken": getCSRF() }
    })
    .then(res => res.json())
    .then(data => {
        if (data.quantity === 0) {
            removeItem(itemId);
        } else {
            updateAll(itemId, data.quantity, data.price, data.name);
        }
    });
});

// =====================
// 🔥 MASTER UPDATE FUNCTION
// =====================
function updateAll(itemId, quantity, price, name) {
    updateItemSection(itemId, quantity);
    updateCartUI(itemId, quantity, price, name);
    updateTotal();
}

// =====================
// 🔹 ITEM SECTION UPDATE
// =====================
function updateItemSection(itemId, quantity) {
    let count = document.querySelector(`.itemCount[data-id="${itemId}"]`);
    let addBtn = document.querySelector(`.addButton[data-id="${itemId}"]`);
    let qtyBox = count?.parentElement;

    if (!count || !addBtn || !qtyBox) return;

    if (quantity > 0) {
        count.textContent = quantity;
        addBtn.classList.add("hidden");
        qtyBox.classList.remove("hidden");
    }
}

// =====================
// 🔹 REMOVE ITEM (WHEN 0)
// =====================
function removeItem(itemId) {
    let count = document.querySelector(`.itemCount[data-id="${itemId}"]`);
    let addBtn = document.querySelector(`.addButton[data-id="${itemId}"]`);
    let qtyBox = count?.parentElement;

    if (count) count.textContent = 0;
    if (qtyBox) qtyBox.classList.add("hidden");
    if (addBtn) addBtn.classList.remove("hidden");

    let cartItem = document.getElementById(`cartItem${itemId}`);
    if (cartItem) cartItem.remove();

    updateTotal();
}

// =====================
// 🔹 CART UI UPDATE
// =====================
function updateCartUI(itemId, quantity, price, name) {
    let cartItem = document.getElementById(`cartItem${itemId}`);

    // ✅ If item NOT in cart → create it
    if (!cartItem) {
        let container = document.getElementById("cartHolder");

        container.insertAdjacentHTML("beforeend", `
        <div id="cartItem${itemId}" class="cart-item">
            <div>
                <p class="cartItemName">${name}</p>
                <p class="cartItemPrice">₹${price}</p>
            </div>
            <div class="cart-qty-controller">
                <button class="cartReduceButton cart-qty-btn" data-id="${itemId}">-</button>
                <p data-price="${price}" id="cartItemQuantity${itemId}" class="cart-qty-count">${quantity}</p>
                <button class="cartIncreaseButton cart-qty-btn" data-id="${itemId}">+</button>
            </div>
        </div>
        `);

    } else {
        // ✅ If exists → just update
        let qtyEl = document.getElementById(`cartItemQuantity${itemId}`);
        if (qtyEl) qtyEl.textContent = quantity;
    }
}

// =====================
// 🔹 TOTAL CALCULATION
// =====================
function updateTotal() {
    let total = 0;
    let count = 0;

    document.querySelectorAll(".cart-qty-count").forEach(el => {
        let q = parseInt(el.textContent);
        let p = parseFloat(el.dataset.price);

        total += q * p;
        count++;
    });

    document.getElementById("countItems").textContent = `(${count} items)`;
    document.getElementById("totalPrice").textContent = total;
}

// =====================
updateTotal();