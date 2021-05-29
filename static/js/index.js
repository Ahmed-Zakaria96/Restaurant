document.addEventListener('DOMContentLoaded', function () {

  load_restaurants();
  document.querySelector("#apiloginform").addEventListener('click', () => {
    document.getElementById('login_form').style.display = 'block';
    document.getElementById('menu_section').style.display = 'none';
    document.getElementById('branches_section').style.display = 'none';

    
  });
  document.querySelector("#login_form").addEventListener('submit', () => login());
});

function load_restaurants() {
  document.getElementById('login_form').style.display = 'none';
  document.getElementById('menu_section').style.display = 'none';
  document.getElementById('branches_section').style.display = 'block';
  fetch('/restaurants')
    .then(response => response.json())
    .then(data => {
      data.forEach(r => {
        const container = document.createElement('div');
        let restaurant_data = `<div class="tm-popular-item">
            <div class="tm-popular-item-description">
              <h3 class="tm-handwriting-font tm-popular-item-title"><span class='tm-handwriting-font bigger-first-letter'>${r.title}</span></h3><hr class="tm-popular-item-hr">
              <p>Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque. sed ipsum.</p>

              <div class="order-now-container">
                <button onclick='restaurant_details(${r.id})' class="order-now-link tm-handwriting-font rest_button">View Details</a>
              </div>
            </div>              
            </div>`
        container.innerHTML = restaurant_data;
        let content_section = document.getElementById('content');
        content_section.appendChild(container);
      })
    })
}

function restaurant_details(id) {
  document.getElementById('menu_section').style.display = 'block';
  document.getElementById('branches_section').style.display = 'none';

  fetch(`/restaurants/${id}`)
    .then(response => response.json())
    .then(data => {
      data.forEach(m => {
        const container = document.createElement('div');
        let menu_data = `<div class="tm-product">
            <div class="tm-product-text">
              <h3 class="tm-product-title">${m.name}</h3>
              <p class="tm-product-description">Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque. Red ipsum.</p>
            </div>
            <div class="tm-product-price">
              <a href="#" class="tm-product-price-link tm-handwriting-font"><span class="tm-product-price-currency">$</span>${m.price}</a>
            </div>
          </div>`
        container.innerHTML = menu_data;
        container.setAttribute('class', 'container');
        let menu_section = document.getElementById('menu_content');
        menu_section.appendChild(container);
      })


    })
}

function login() {
  const user = document.getElementById('apiusername').value;
  const password = document.getElementById('apipassword').value;
  fetch(`/apilogin`, {
      method: 'POST',
      headers: {
        "content-type": "application/json"
      },
      body: JSON.stringify({
        username: user,
        password: password
      })
    })
    .then(response => {
      if (response.status === 201) {
        return response.json();
      }
    })
    .then(rep => {
      console.log(rep)
    })
    .catch(function (error) {
      console.log("Fetch error: " + error);
    });
}