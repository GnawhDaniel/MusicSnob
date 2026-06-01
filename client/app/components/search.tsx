import { useState } from "react";
import { addArtist } from "~/api/api";

export default async function SearchBar() {
  const [query, setQuery] = useState("");

  async function submitHandler() {
    const res = await addArtist(query);
    console.log(res);
  }
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
      <button onClick={submitHandler}>Submit</button>
    </div>
  );
}
