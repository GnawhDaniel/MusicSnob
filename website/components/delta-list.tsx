"use client";

import { useState, useMemo } from "react";
import { DeltaInterface } from "@/app/interfaces";
import Delta from "@/components/delta";

type DeltaSortField =
  | keyof DeltaInterface
  | "view_change_percent"
  | "subscriber_change_percent";

function sortDeltas(
  deltas: DeltaInterface[],
  field: DeltaSortField,
  descending = true,
): DeltaInterface[] {
  return [...deltas].sort((a, b) => {
    let aValue: string | number;
    let bValue: string | number;

    switch (field) {
      case "view_change_percent":
        aValue = a.view_delta / a.min_view_count;
        bValue = b.view_delta / b.min_view_count;
        break;

      case "subscriber_change_percent":
        aValue = a.subscriber_delta / a.earliest_subscriber_count;
        bValue = b.subscriber_delta / b.earliest_subscriber_count;
        break;

      case "artist_name":
        aValue = a.artist_name.toLowerCase();
        bValue = b.artist_name.toLowerCase();
        break;

      default:
        aValue = a[field];
        bValue = b[field];
    }

    if (aValue < bValue) return descending ? 1 : -1;
    if (aValue > bValue) return descending ? -1 : 1;
    return 0;
  });
}

export default function DeltaList({ deltas }: { deltas: DeltaInterface[] }) {
  const [sortField, setSortField] = useState<DeltaSortField>(
    "view_change_percent",
  );
  const [descending, setDescending] = useState(true);

  const sorted = useMemo(
    () => sortDeltas(deltas, sortField, descending),
    [deltas, sortField, descending],
  );

  return (
    <>
      <div className="sort-controls">
        <select
          value={sortField}
          onChange={(e) => setSortField(e.target.value as DeltaSortField)}
        >
          <option value="view_change_percent">View change %</option>
          <option value="subscriber_change_percent">Subscriber change %</option>
          <option value="view_delta">View delta</option>
          <option value="subscriber_delta">Subscriber delta</option>
          <option value="artist_name">Artist name</option>
          <option value="sub_date">Date subscribed</option>
        </select>
        <button onClick={() => setDescending((d) => !d)}>
          {descending ? "Descending" : "Ascending"}
        </button>
      </div>
      <div className="deltas-list">
        {sorted.map((artist) => (
          <Delta key={artist.youtube_channel_id} delta={artist} />
        ))}
      </div>
    </>
  );
}
