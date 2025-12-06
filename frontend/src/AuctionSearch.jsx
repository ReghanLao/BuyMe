import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL;

export default function ItemSearch() {
  const [filters, setFilters] = useState({
    item_type: "",        // shoes | shirts | pants
    min_price: "",
    max_price: "",
    gender: "",           // shoes-only
    size: "",
    color: "",
    brand: "",
    status: "running",    // show currently bidding by default
    sort_by: "end_time",  // end_time | current_price | name
    sort_dir: "asc",      // asc | desc
    keyword: "",          // search in name/description/etc.
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
      const params = new URLSearchParams();

      // only send non-empty filters
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== "" && value !== null && value !== undefined) {
          params.append(key, value);
        }
      });

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
      <h2>Search Items</h2>

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
        {/* Item/category filters */}
        <select name="item_type" value={filters.item_type} onChange={handleChange}>
          <option value="">Any Type</option>
          <option value="shoes">Shoes</option>
          <option value="shirts">Shirts</option>
          <option value="pants">Pants</option>
        </select>

        <input
          name="keyword"
          placeholder="Keyword (name/desc/brand)"
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

        {/* Shoe-specific filters; backend can just ignore when item_type != shoes */}
        <select name="gender" value={filters.gender} onChange={handleChange}>
          <option value="">Any Gender</option>
          <option value="mens">Mens</option>
          <option value="womens">Womens</option>
          <option value="unisex">Unisex</option>
        </select>

        <input
          name="size"
          placeholder="Size"
          value={filters.size}
          onChange={handleChange}
        />

        <input
          name="color"
          placeholder="Color"
          value={filters.color}
          onChange={handleChange}
        />

        <input
          name="brand"
          placeholder="Brand"
          value={filters.brand}
          onChange={handleChange}
        />

        {/* Show status of current bidding */}
        <select name="status" value={filters.status} onChange={handleChange}>
          <option value="">Any Status</option>
          <option value="running">Running</option>
          <option value="scheduled">Scheduled</option>
          <option value="closed">Closed</option>
        </select>

        {/* Sorting */}
        <select name="sort_by" value={filters.sort_by} onChange={handleChange}>
          <option value="end_time">Sort by End Time</option>
          <option value="current_price">Sort by Current Price</option>
          <option value="name">Sort by Name</option>
        </select>

        <select name="sort_dir" value={filters.sort_dir} onChange={handleChange}>
          <option value="asc">Asc</option>
          <option value="desc">Desc</option>
        </select>

        <button type="submit" disabled={loading}>
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      {message && <p>{message}</p>}

      {/* Results list: show items + current auction status/price */}
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
            {it.brand && <p>Brand: {it.brand}</p>}
            {it.color && <p>Color: {it.color}</p>}
            {it.size && <p>Size: {it.size}</p>}

            {/* current bidding info from joined auction */}
            {it.status && <p>Status: {it.status}</p>}
            {it.current_price != null && (
              <p>Current Price: ${Number(it.current_price).toFixed(2)}</p>
            )}
            {it.end_time && (
              <p>Ends: {new Date(it.end_time).toLocaleString()}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
