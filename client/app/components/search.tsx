import { useState } from "react";
import { useFetcher } from "react-router";

export default function SearchBar() {
  const [query, setQuery] = useState("");

  const fetcher = useFetcher();
  // Example ChannelID:
  // UCGjD8QSbPrqHC6sqxsLiB0g

  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Youtube Channel ID"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button
        onClick={() =>
          fetcher.submit({ youtube_channel_id: query }, { method: "post" })
        }
      >
        Submit
      </button>
    </div>
  );
}
