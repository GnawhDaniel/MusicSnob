import type { Route } from "./+types/sign-in";
import { useState } from "react";
import { signIn } from "../api/api";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Music Snob" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export default function SignInElement() {
  const [username, setUsername] = useState("");
  const [passwd, setPasswd] = useState("");

  return (
    <div>
      <div className="sign-in">
        <label htmlFor="uname">Username</label>
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          type="text"
          placeholder="Enter Username"
          name="uname"
          required
        />

        <label htmlFor="passwd">Password</label>
        <input
          value={passwd}
          onChange={(e) => setPasswd(e.target.value)}
          type="password"
          name="passwd"
          required
        />

        <button type="submit" onClick={() => signIn(username, passwd)}>
          Login
        </button>
      </div>
    </div>
  );
}
