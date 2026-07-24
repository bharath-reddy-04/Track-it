import { useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Navbar from "../Navbar/navbar";
import { createCustomer } from "../../api/customerapi";
import { useCustomer } from "../../context/customercontext";
import "./register.css";

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export default function Register() {
  const navigate = useNavigate();
  const { isLoading, isRegistered, name: registeredName, registerCustomer } = useCustomer();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const isValid = useMemo(() => name.trim().length > 0 && EMAIL_REGEX.test(email.trim()), [name, email]);

  async function handleSubmit(event) {
    event.preventDefault();
    if (!isValid || submitting) return;
    setSubmitting(true);
    setError("");
    try {
      const customer = await createCustomer({ name: name.trim(), email: email.trim() });
      registerCustomer(customer);
      navigate("/");
    } catch (err) {
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  return <div className="register-page"><Navbar /><main className="register-page__content page-content"><section className="register-card" aria-labelledby="register-title">{isLoading ? <p>Checking your registration…</p> : isRegistered ? <><h1 id="register-title">You’re registered</h1><p>Welcome back, {registeredName}.</p><Link className="register-card__button" to="/">Browse movies</Link></> : <><h1 id="register-title">Create your profile</h1><p>Register to personalize your movie recommendations.</p><form onSubmit={handleSubmit}><label htmlFor="customer-name">Name</label><input id="customer-name" type="text" value={name} onChange={(event) => setName(event.target.value)} placeholder="John Doe" autoComplete="name" /><label htmlFor="customer-email">Email</label><input id="customer-email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="john@example.com" autoComplete="email" />{error && <p className="register-card__error">{error}</p>}<button type="submit" disabled={!isValid || submitting}>{submitting ? "Registering…" : "Register"}</button></form></>}</section></main></div>;
}
