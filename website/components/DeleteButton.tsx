// app/artist/[channelID]/DeleteButton.tsx
"use client";

import { deleteArtist } from "@/app/actions";

export default function DeleteButton({ channelID }: { channelID: string }) {
  return (
    <button onClick={() => deleteArtist(channelID)}>
      Delete
    </button>
  );
}