import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL;

export default function AuctionForm() {
  const [form, setForm] = useState({
    seller_id: "",
    name: "",
    item_type: "",
    item_details: "",
    initial_price: "",
    min_sell_price: "",
    bid_increment: "",
    start_time: "",
    end_time: "",
  });

  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`${API_URL}/api/auctions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const data = await response.json();

      if (!response.ok) {
        setMessage("Error creating auction");
      } else {
        setMessage(data.message);
      }
    } catch (err) {
        console.error("AuctionForm error:", err);
      setMessage("Error! Could not reach backend ");
    }

  };
  
  return (
    <div style={{ padding: "20px" }}>
      <h2>Create Auction</h2>

      <form
        onSubmit={handleSubmit}
        style={{ display: "flex", flexDirection: "column", gap: "10px", maxWidth: "300px" }}
      >
        <input
          name="seller_id"
          placeholder="Seller ID"
          value={form.seller_id}
          onChange={handleChange}
          required
        />

        <input
          name="name"
          placeholder="Item Name"
          value={form.name}
          onChange={handleChange}
          required
        />

        <input
          name="item_type"
          placeholder="Item Type"
          value={form.item_type}
          onChange={handleChange}
          required
        />

        <textarea
          name="item_details"
          placeholder="Item Details"
          value={form.item_details}
          onChange={handleChange}
          required
        />

        <input
          type="number"
          name="initial_price"
          placeholder="Initial Price"
          value={form.initial_price}
          onChange={handleChange}
          required
        />

        <input
          type="number"
          name="min_sell_price"
          placeholder="Minimum Sell Price"
          value={form.min_sell_price}
          onChange={handleChange}
          required
        />

        <input
          type="number"
          name="bid_increment"
          placeholder="Bid Increment"
          value={form.bid_increment}
          onChange={handleChange}
          required
        />

        <input
          type="date"
          name="start_time"
          value={form.start_time}
          onChange={handleChange}
          required
        />

        <input
          type="date"
          name="end_time"
          value={form.end_time}
          onChange={handleChange}
          required
        />

        <button type="submit">Create Auction</button>
      </form>

      {message && <p>{message}</p>}
    </div>
  );
}
