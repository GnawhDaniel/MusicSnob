import { type DeltaInterface } from "@/app/interfaces";
import { formatDate } from "@/utils/utils";

type DeltaComponentProps = {
  delta: DeltaInterface;
};

function textColorConditional(metric: number) {
  return metric >= 0 ? (metric === 0 ? "zero" : "positive") : "negative";
}

export default function Delta({ delta }: DeltaComponentProps) {
  console.log(delta);
  return (
    <div className="delta-container" id={delta.youtube_channel_id}>
      <div className="delta-card">
        <h3>{delta.artist_name}</h3>
        <hr />
        <p>since {formatDate(delta.sub_date)}</p>
        <p>Initial Views: {delta.min_view_count.toLocaleString("en-US")}</p>
        <p className={textColorConditional(delta.view_delta)}>
          {delta.view_delta > 0 ? "+" : ""}
          {((delta.view_delta / delta.min_view_count) * 100).toFixed(2)}%
        </p>
        <p className={textColorConditional(delta.view_delta)}>
          {delta.view_delta >= 0 ? "+" : ""}
          {delta.view_delta.toLocaleString("en-US")} views
        </p>

        <p>Initial Subs: {delta.earliest_subscriber_count.toLocaleString("en-US")}</p>
        <p className={textColorConditional(delta.subscriber_delta)}>
          {delta.subscriber_delta >= 0 ? "+" : ""}
          {delta.subscriber_delta.toLocaleString("en-US")} subscribers
        </p>
        <p className={textColorConditional(delta.subscriber_delta)}>
          {delta.subscriber_delta > 0 ? "+" : ""}
          {((delta.subscriber_delta / delta.earliest_subscriber_count) * 100).toFixed(2)}%{" "}
        </p>
      </div>
    </div>
  );
}
