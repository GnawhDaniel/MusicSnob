import { getDeltas } from "@/app/actions";
import SearchBar from "@/components/search";
import DeltaList from "@/components/delta-list";
import "@/app/app.css";

export default async function Home() {
  const deltas = await getDeltas();

  return (
    <>
      <header>
        <h1>Music Snob</h1>
        <SearchBar />
      </header>
      <DeltaList deltas={deltas} />
    </>
  );
}