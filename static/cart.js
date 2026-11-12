const cart = new Map();

const linesEl = document.getElementById("cart-lines");
const totalEl = document.getElementById("cart-total");
const placeOrderEl = document.getElementById("place-order");
const confirmationEl = document.getElementById("confirmation");

function euros(cents) {
  return `€${(cents / 100).toFixed(2)}`;
}

function cartTotal() {
  let total = 0;
  for (const item of cart.values()) {
    total += item.price_cents;
  }
  return total;
}

function render() {
  linesEl.innerHTML = "";
  if (cart.size === 0) {
    linesEl.innerHTML = '<li class="empty">Your order is empty.</li>';
  }
  for (const item of cart.values()) {
    const li = document.createElement("li");
    li.innerHTML = `
      <span>${item.name}</span>
      <span class="qty">
        <button type="button" data-action="dec" data-id="${item.id}">−</button>
        ${item.quantity}
        <button type="button" data-action="inc" data-id="${item.id}">+</button>
      </span>`;
    linesEl.appendChild(li);
  }
  totalEl.textContent = euros(cartTotal());
  placeOrderEl.disabled = cart.size === 0;
}

document.querySelectorAll(".product button").forEach((button) => {
  button.addEventListener("click", () => {
    const { id, name, price } = button.dataset;
    const item = cart.get(id) || { id, name, price_cents: Number(price), quantity: 0 };
    item.quantity += 1;
    cart.set(id, item);
    confirmationEl.hidden = true;
    render();
  });
});

linesEl.addEventListener("click", (event) => {
  const { action, id } = event.target.dataset;
  const item = cart.get(id);
  if (!item) return;
  item.quantity += action === "inc" ? 1 : -1;
  if (item.quantity < 1) cart.delete(id);
  render();
});

placeOrderEl.addEventListener("click", async () => {
  placeOrderEl.disabled = true;
  const items = [...cart.values()].map(({ id, quantity }) => ({ id, quantity }));
  try {
    const response = await fetch("/api/orders", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ items }),
    });
    if (!response.ok) throw new Error(`Order failed (${response.status})`);
    const order = await response.json();
    confirmationEl.textContent = `Order ${order.id} placed. ${euros(order.total_cents)} charged to the ward budget.`;
    cart.clear();
  } catch (error) {
    confirmationEl.textContent = "Something went wrong. Please try again.";
  }
  confirmationEl.hidden = false;
  render();
});
