import Delta from "../components/delta";
import SearchBar from "~/components/search";
import { type DeltaInterface } from "../api/api";
import "../css/delta.css";

type HomePageProps = {
  deltas: DeltaInterface[];
};

export default function HomePage({ deltas }: HomePageProps) {

  // Sort based on view percentage
  let deltas_sorted = deltas.sort((a, b) => 
    (b.views_delta / b.min_view_count) - (a.views_delta / a.min_view_count))

  return (
    <>
      <h1>Music Snob</h1>
      <SearchBar />
      <div className="deltas-list">
        {deltas_sorted.map((artist) => {
          return (
            <Delta delta={artist} />
          );
        })}
      </div>
    </>
  );
}
