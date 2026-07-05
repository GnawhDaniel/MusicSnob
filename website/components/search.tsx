"use server";
import { addArtist } from "@/app/actions";

export default async function SearchBar() {
  // Example ChannelID:
  // UCGjD8QSbPrqHC6sqxsLiB0g

  return (
    <form className="search-bar" action={addArtist}>
      <input
        type="text"
        placeholder="Youtube Channel ID"
        name="youtube_channel_id"
      />
      <button type="submit">Submit</button>
    </form>
  );
}
