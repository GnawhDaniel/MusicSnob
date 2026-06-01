import Delta from "../components/delta";
import SearchBar from "~/components/search";
import { type DeltaInterface } from "../api/api";
import "../css/delta.css";

type HomePageProps = {
  deltas: DeltaInterface[];
};

export default function HomePage({ deltas }: HomePageProps) {
  return (
    <>
      <h1>Welcome to the Home Page</h1>
      <SearchBar />
      <ul className="deltas-list">
        {deltas.map((artist) => {
          return (
            <li key={artist.youtube_channel_id}>
              <Delta delta={artist} />
            </li>
          );
        })}
      </ul>
    </>
  );
}
