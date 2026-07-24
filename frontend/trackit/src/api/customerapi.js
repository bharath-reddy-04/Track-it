const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

async function handleResponse(response) {
  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    throw new Error(errorBody.detail || `Request failed with status ${response.status}`);
  }
  return response.json();
}

export async function createCustomer({ name, email }) {
  const response = await fetch(`${API_BASE_URL}/api/customer/create`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email }),
  });
  return handleResponse(response);
}

export async function trackMovieClick({ customerId, movie }) {
  const response = await fetch(`${API_BASE_URL}/api/customer/movie`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ customer_id: customerId, movie }),
  });
  return handleResponse(response);
}

export async function getCustomer(customerId) {
  const response = await fetch(`${API_BASE_URL}/api/customer/${customerId}`);
  return handleResponse(response);
}