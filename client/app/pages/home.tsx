import Delta from "../components/delta";
import { type DeltaInterface } from "../api/api";

type HomePageProps = {
  deltas: DeltaInterface[];
};

export default function HomePage({ deltas }: HomePageProps) {
  console.log(deltas);
  return (
    <>
      <h1>Welcome to the Home Page</h1>
      {deltas.map((artist) => {
        return (
          <>
            <div key={artist.youtube_channel_id}>
              <h1>{artist.artist_name}</h1>
              {/* <p>+{artist.subscriber_delta}</p> */}
              
              <div>
                <h2>View Delta</h2>
                <p>+{artist.view_delta}</p>
              </div>
              <p>
                {((artist.view_delta / artist.min_view_count) * 100).toFixed(2)}
                %
              </p>
            </div>
            <hr />
          </>
        );
      })}
    </>
  );
}
