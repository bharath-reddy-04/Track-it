import { createContext, useContext, useEffect, useState, useCallback } from "react";
import { getCustomer } from "../api/customerapi";

const CustomerContext = createContext(undefined);

const STORAGE_KEY = "customer_id";

export function CustomerProvider({ children }) {
  const [customerId, setCustomerId] = useState(null);
  const [name, setName] = useState(null);
  const [email, setEmail] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // On mount, try to restore the customer session from localStorage.
  useEffect(() => {
    const storedId = localStorage.getItem(STORAGE_KEY);
    if (!storedId) {
      setIsLoading(false);
      return;
    }

    getCustomer(storedId)
      .then((customer) => {
        setCustomerId(customer.id);
        setName(customer.name);
        setEmail(customer.email);
      })
      .catch(() => {
        // Stored id is stale/invalid — clear it so the modal reappears.
        localStorage.removeItem(STORAGE_KEY);
      })
      .finally(() => setIsLoading(false));
  }, []);

  const registerCustomer = useCallback((customer) => {
    setCustomerId(customer.id);
    setName(customer.name);
    setEmail(customer.email);
    localStorage.setItem(STORAGE_KEY, customer.id);
  }, []);

  const clearCustomer = useCallback(() => {
    setCustomerId(null);
    setName(null);
    setEmail(null);
    localStorage.removeItem(STORAGE_KEY);
  }, []);

  const value = {
    customerId,
    name,
    email,
    isLoading,
    isRegistered: Boolean(customerId),
    registerCustomer,
    clearCustomer,
  };

  return (
    <CustomerContext.Provider value={value}>{children}</CustomerContext.Provider>
  );
}

export function useCustomer() {
  const context = useContext(CustomerContext);
  if (context === undefined) {
    throw new Error("useCustomer must be used within a CustomerProvider");
  }
  return context;
}