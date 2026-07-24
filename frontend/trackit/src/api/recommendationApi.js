const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

export async function getRecommendations(customerId) {
  const response = await fetch(`${API_BASE_URL}/api/recommendations/${customerId}`);
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || "Could not load recommendations.");
  }
  return response.json();
}
