import { type DeltaInterface } from "../api/api";

type DeltaComponentProps = {
  delta: DeltaInterface;
};

function textColorConditional(view_delta: number) {
  return view_delta >= 0
    ? view_delta === 0
      ? "zero"
      : "positive"
    : "negative";
}

export default function Delta({ delta }: DeltaComponentProps) {
  return (
    <>
      <h1>{delta.artist_name}</h1>

      <div>
        <p>Initial View: {delta.min_view_count}</p>
        <p>Initial Subs: {delta.min_subscriber_count}</p>
      </div>

      <div>
        <p className={textColorConditional(delta.view_delta)}>
          {delta.view_delta >= 0 ? "+" : ""}{delta.view_delta} views
        </p>
      </div>
      <p className={textColorConditional(delta.view_delta)}>
        {delta.view_delta > 0 ? "+" : ""}
        {((delta.view_delta / delta.min_view_count) * 100).toFixed(2)}%
      </p>
    </>
  );
}
