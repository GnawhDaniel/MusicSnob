import { type DeltaInterface } from "../api/api";
import { formatDate } from "~/utils/utils";

type DeltaComponentProps = {
  delta: DeltaInterface;
};

function textColorConditional(metric: number) {
  return metric >= 0 ? (metric === 0 ? "zero" : "positive") : "negative";
}

export default function Delta({ delta }: DeltaComponentProps) {
  return (
    <div className="delta-container">
      <div className="delta-card">
        <h3>{delta.artist_name}</h3>
        <hr />
        <p>since {formatDate(delta.subscription_date)}</p>
        <p>Initial Views: {delta.min_view_count.toLocaleString("en-US")}</p>
        <p className={textColorConditional(delta.views_delta)}>
          {delta.views_delta > 0 ? "+" : ""}
          {((delta.views_delta / delta.min_view_count) * 100).toFixed(2)}%
        </p>
        <p className={textColorConditional(delta.views_delta)}>
          {delta.views_delta >= 0 ? "+" : ""}
          {delta.views_delta.toLocaleString("en-US")} views
        </p>

        <p>Initial Subs: {delta.earliest_sub_count.toLocaleString("en-US")}</p>
        <p className={textColorConditional(delta.subs_delta)}>
          {delta.subs_delta >= 0 ? "+" : ""}
          {delta.subs_delta.toLocaleString("en-US")} subscribers
        </p>
        <p className={textColorConditional(delta.subs_delta)}>
          {delta.subs_delta > 0 ? "+" : ""}
          {((delta.subs_delta / delta.earliest_sub_count) * 100).toFixed(2)}%{" "}
        </p>
      </div>
    </div>
  );
}
