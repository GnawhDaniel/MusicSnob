"use server"
import { signIn } from "@/app/actions";

export default async function sign_in() {

  return (
    <div>
      <form className="sign-in" action={signIn}>
        <label htmlFor="uname">Username</label>
        <input
        //   value={username}
        //   onChange={(e) => setUsername(e.target.value)}
          type="text"
          placeholder="Enter Username"
          name="uname"
          required
        />

        <label htmlFor="passwd">Password</label>
        <input
        //   value={passwd}
        //   onChange={(e) => setPasswd(e.target.value)}
          type="password"
          name="passwd"
          required
        />

        <button type="submit">
          Login
        </button>
      </form>
    </div>
  );
}
