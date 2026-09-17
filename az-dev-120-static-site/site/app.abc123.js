const products = [
    { name: 'Kayak 10ft', price: 649 },
    { name: '2-Person Tent', price: 249 },
    { name: '45L Backpack', price: 189 },
    { name: 'Trail Boots', price: 145 },
    { name: 'Weekend Stove', price: 79 },
    { name: 'Rain Jacket', price: 129 },
];
const el = document.getElementById('products');
el.innerHTML = products.map(p => `
  <div class="card">
    <h3>${p.name}</h3>
    <div class="price">$${p.price}</div>
  </div>
`).join('');
