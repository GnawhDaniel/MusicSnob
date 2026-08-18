import SearchBar from "@/components/search";
import { getDeltas } from "@/app/actions";
import Delta from "@/components/delta";
import "@/app/app.css";

export default async function Home() {
  const deltas = await getDeltas();
  let deltas_sorted = deltas.sort(
    (a, b) => b.view_delta / b.min_view_count - a.view_delta / a.min_view_count,
  );
  return (
    <>
      <header>
        <h1>Music Snob</h1>
        <SearchBar />
      </header>
      <div className="deltas-list">
        {deltas_sorted.map((artist) => {
          return <Delta key={artist.youtube_channel_id} delta={artist} />;
        })}
      </div>
    </>
  );
}
