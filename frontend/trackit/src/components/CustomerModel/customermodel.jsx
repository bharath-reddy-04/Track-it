import { useState, useMemo } from "react";
import { createCustomer } from "../../api/customerapi";
import { useCustomer } from "../../context/customercontext";
import "./customermodel.css";

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export default function CustomerModal() {
  const { isRegistered, isLoading, registerCustomer } = useCustomer();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const isValid = useMemo(
    () => name.trim().length > 0 && EMAIL_REGEX.test(email.trim()),
    [name, email]
  );

  // Don't render until we know whether a session already exists,
  // and never render again once the customer is registered.
  if (isLoading || isRegistered) {
    return null;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!isValid || submitting) return;

    setSubmitting(true);
    setError("");
    try {
      const customer = await createCustomer({ name: name.trim(), email: email.trim() });
      registerCustomer(customer);
    } catch (err) {
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="customer-modal-overlay">
      <div className="customer-modal" role="dialog" aria-modal="true">
        <h2>Welcome!</h2>
        <p>Tell us a bit about yourself to get personalized recommendations.</p>

        <form onSubmit={handleSubmit}>
          <label htmlFor="customer-name">Name</label>
          <input
            id="customer-name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="John Doe"
            autoComplete="name"
          />

          <label htmlFor="customer-email">Email</label>
          <input
            id="customer-email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="john@example.com"
            autoComplete="email"
          />

          {error && <p className="customer-modal-error">{error}</p>}

          <button type="submit" disabled={!isValid || submitting}>
            {submitting ? "Submitting..." : "Submit"}
          </button>
        </form>
      </div>
    </div>
  );
}