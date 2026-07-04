"use server"

export default async function SearchBar() {

  // Example ChannelID:
  // UCGjD8QSbPrqHC6sqxsLiB0g

  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Youtube Channel ID"
        // value={""}
        // onChange={() => null}
      />
      <button
        // onClick={() =>
        //   fetcher.submit({ youtube_channel_id: query }, { method: "post" })
        // }
      >
        Submit
      </button>
    </div>
  );
}
