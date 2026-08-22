import DeleteButton from "@/components/DeleteButton";
import { getArtistInfo } from "@/app/actions";
import { cookies } from "next/headers";
import { notFound } from "next/navigation";

interface Artist {
  youtube_channel_id: string;
  artist_name: string;
  // add any other fields your API returns
  // move this to interface.ts
}

export default async function Page({
  params,
}: {
  params: Promise<{ channelID: string }>;
}) {
  const { channelID } = await params;

  const artist: Artist | null = await getArtistInfo(channelID);

  if (!artist) {
    notFound();
  }

  const cookieStore = await cookies();
  const token = cookieStore.get("__Host-SessionID");

  return (
    <>
      <div>Channel ID: {channelID}</div>
      <div>Artist: {artist.artist_name}</div>
      {token && <DeleteButton channelID={channelID} />}
    </>
  );
}
