document.addEventListener('DOMContentLoaded', function () {

  const forms = document.querySelectorAll(".order_form");
  for (i = 0; i < forms.length; i++) {
    forms[i].addEventListener('submit', () => order())
  }
  document.getElementById('submit_order_button').addEventListener('click', () => submitorder())

  check_cart();
});

function cancel_buttons() {

}
var order_list = {}
var total = 0

function order() {
  const item_id = event.target.item.value;
  const item_name = event.target.itemName.value;
  const item_quantity = event.target.quantity.value;
  const item_price = event.target.itemPrice.value;

  if (item_name in order_list) {

    order_list[item_name]['quantity'] += parseInt(item_quantity)
  } else {
    order_list[item_name] = {}
    order_list[item_name]['id'] = parseInt(item_id)
    order_list[item_name]['quantity'] = parseInt(item_quantity)
    order_list[item_name]['price'] = parseFloat(item_price)
  }
  console.log(order_list);
  check_cart();
  event.preventDefault();
}

function check_cart() {
  if (order_list.len == 0) {
    document.getElementById('cart_test').innerHTML = "Your cart is empty";
  } else {
    document.getElementById('cart_test').innerHTML = "";
    let cart_items = document.createElement('ul');
    let items_content = ""
    total = 0
    for (i in order_list) {
      total += order_list[i]['price'] * order_list[i]['quantity'];
      items_content += `<li><form onsubmit="return cancel(event)" class="cancel_item">                
        ${i} ${order_list[i]['quantity']} ---- ${order_list[i]['price']}$
        <input type="submit" class="btn btn-danger btn-sm" value="X" style="font-size: 60%; padding: 5px;">
        <input name="item" value="${i}" hidden>
        </form></li>`
    }
    cart_items.innerHTML = items_content;
    document.getElementById('cart_test').append(cart_items);
    document.getElementById('order_total').innerHTML = total;
    document.getElementById('submit_order').style.display = 'block';
  }

}

function cancel() {
  const item = event.target.item.value;
  console.log(item)
  if (item in order_list) {
    delete order_list[item]
    for (i in order_list) {
      total += order_list[i]['price'] * order_list[i]['quantity'];
    }
    document.getElementById('order_total').innerHTML = total;
  }
  check_cart();
  event.preventDefault();
}

function submitorder() {
  let ready_order = {}
  for (i in order_list){
    ready_order[i] = order_list[i]['quantity']
  }
  fetch(`/submit_order`, {
      method: 'POST',
      headers: {
        "content-type": "application/json"
      },
      body: JSON.stringify(ready_order)
    })
    .then(response => response.json())
    .then(res => {
      document.getElementById('cart_test').innerHTML = "order placed successfully";
      order_list = {}
      document.getElementById('order_total').innerHTML = 0;
      console.log(res);
    })
  event.preventDefault();
}