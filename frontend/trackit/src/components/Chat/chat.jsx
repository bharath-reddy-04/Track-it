import React from "react";
import Navbar from "../Navbar/navbar";
import "./chat.css";

/**
 * Chat
 * ----
 * Placeholder page for the "Chat" nav link. Intended to eventually host
 * a chat-based movie recommendation assistant.
 *
 * Replace the placeholder content below once that feature is built —
 * the Navbar link and route are already wired up.
 */
function Chat() {
  return (
    <div className="chat-page">
      <Navbar />
      <main className="chat-page__content page-content">
        <h1 className="chat-page__heading">Chat</h1>
        <p className="chat-page__text">
          Chat-based recommendations are coming soon.
        </p>
      </main>
    </div>
  );
}

export default Chat;