import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL;

// Browse/search screen for items + current auction status
export default function ItemBrowse() {
  const [filters, setFilters] = useState({
    item_type: "",        // shoes | shirts | pants
    min_price: "",
    max_price: "",
    keyword: "",          // name/brand/description, etc.
    sort_by: "end_time",  // end_time | current_price | name
    sort_dir: "asc",      // asc | desc
  });

  const [items, setItems] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFilters((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      // build query string from filters
      const params = new URLSearchParams();
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== "" && value !== null && value !== undefined) {
          params.append(key, value);
        }
      });

      // NOTE: adjust endpoint + response shape to your backend
      const res = await fetch(`${API_URL}/api/items?${params.toString()}`);
      const data = await res.json();

      if (!res.ok) {
        setItems([]);
        setMessage(data.message || "Error searching items");
      } else {
        const list = data.items || [];
        setItems(list);
        if (list.length === 0) {
          setMessage("No items found for these filters.");
        }
      }
    } catch (err) {
      console.error(err);
      setItems([]);
      setMessage("Error! Could not reach backend");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Browse Items</h2>

      {/* Filter / search form */}
      <form
        onSubmit={handleSearch}
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))",
          gap: "10px",
          maxWidth: "900px",
          marginBottom: "20px",
        }}
      >
        <select
          name="item_type"
          value={filters.item_type}
          onChange={handleChange}
        >
          <option value="">Any Type</option>
          <option value="shoes">Shoes</option>
          <option value="shirts">Shirts</option>
          <option value="pants">Pants</option>
        </select>

        <input
          name="keyword"
          placeholder="Keyword (name/brand)"
          value={filters.keyword}
          onChange={handleChange}
        />

        <input
          type="number"
          name="min_price"
          placeholder="Min Price"
          value={filters.min_price}
          onChange={handleChange}
        />

        <input
          type="number"
          name="max_price"
          placeholder="Max Price"
          value={filters.max_price}
          onChange={handleChange}
        />

        <select
          name="sort_by"
          value={filters.sort_by}
          onChange={handleChange}
        >
          <option value="end_time">Sort by End Time</option>
          <option value="current_price">Sort by Current Price</option>
          <option value="name">Sort by Name</option>
        </select>

        <select
          name="sort_dir"
          value={filters.sort_dir}
          onChange={handleChange}
        >
          <option value="asc">Asc</option>
          <option value="desc">Desc</option>
        </select>

        <button type="submit" disabled={loading}>
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      {message && <p>{message}</p>}

      {/* Results list */}
      <div style={{ display: "grid", gap: "10px" }}>
        {items.map((it) => (
          <div
            key={it.iid}
            style={{
              border: "1px solid #ccc",
              borderRadius: "4px",
              padding: "10px",
            }}
          >
            <h3>{it.name}</h3>
            <p>Type: {it.item_type}</p>

            {/* Optional item details from subtype tables; adjust to match backend */}
            {it.brand && <p>Brand: {it.brand}</p>}
            {it.color && <p>Color: {it.color}</p>}
            {it.size && <p>Size: {it.size}</p>}

            {/* Current bidding status pulled from joined auction */}
            {it.status && <p>Status: {it.status}</p>}
            {it.current_price != null && (
              <p>
                Current Price: $
                {Number(it.current_price).toFixed(2)}
              </p>
            )}
            {it.end_time && (
              <p>Ends: {new Date(it.end_time).toLocaleString()}</p>
            )}

            {/* You can later make this clickable to go to an Auction Detail screen */}
          </div>
        ))}
      </div>
    </div>
  );
}
