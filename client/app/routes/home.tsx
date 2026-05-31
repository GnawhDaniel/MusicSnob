import type { Route } from "./+types/home";
import HomePage from "../pages/home";
import { getDeltas, type DeltaInterface } from "../api/api";
import { useLoaderData } from "react-router";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "New React Router App" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export async function loader() {
  const deltas = await getDeltas();
  return deltas;
}

export default function Home() {
  const deltas: DeltaInterface[] = useLoaderData(); 
  return <HomePage deltas={deltas} />;
}
