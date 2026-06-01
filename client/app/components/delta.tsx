import { type DeltaInterface } from "../api/api";

type DeltaComponentProps = {
  delta: DeltaInterface;
};

function textColorConditional(metric: number) {
  return metric >= 0 ? (metric === 0 ? "zero" : "positive") : "negative";
}

export default function Delta({ delta }: DeltaComponentProps) {
  return (
    <>
      <h1>{delta.artist_name}</h1>

      <div>
        <p>Initial View: {delta.min_view_count}</p>
        <p className={textColorConditional(delta.views_delta)}>
          {delta.views_delta > 0 ? "+" : ""}
          {((delta.views_delta / delta.min_view_count) * 100).toFixed(2)}%
        </p>
        <p className={textColorConditional(delta.views_delta)}>
          {delta.views_delta >= 0 ? "+" : ""}
          {delta.views_delta} views
        </p>
      </div>

      <div>
        <p>Initial Subs: {delta.earliest_sub_count}</p>
        <p className={textColorConditional(delta.subs_delta)}>
          {delta.subs_delta >= 0 ? "+" : ""}
          {delta.subs_delta} subscribers
        </p>
        <p className={textColorConditional(delta.subs_delta)}>
          {delta.subs_delta > 0 ? "+" : ""}
          {((delta.subs_delta / delta.min_view_count) * 100).toFixed(2)}%        </p>
      </div>

      <div></div>
    </>
  );
}
