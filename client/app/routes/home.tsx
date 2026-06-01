import type { Route } from "./+types/home";
import HomePage from "../pages/home";
import { getDeltas, type DeltaInterface } from "../api/api";
import { useLoaderData, type ActionFunctionArgs } from "react-router";
import { addArtist } from "../api/api";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Music Snob" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}


export async function action({ request }: ActionFunctionArgs ) {
  const formData = await request.formData();
  const youtube_channel_id = formData.get("youtube_channel_id") as string;
  console.log(youtube_channel_id)
  return addArtist(youtube_channel_id); // server-side
}


export async function loader() {
  try {
    const deltas = await getDeltas();
    return deltas;
  } catch (error) {
    console.log(error)
  }
  return null;
}

export default function Home() {
  const deltas: DeltaInterface[] | null = useLoaderData(); 
  if (deltas) {
    return <HomePage deltas={deltas} />;
  }
  return (
    <div>
      <h1>Uh oh... Can't access API server. Try relaunching docker container.</h1>
    </div>
  );
}
