export async function loadOrders() {
  const response = await fetch('/orders');
  return response.json();
}
