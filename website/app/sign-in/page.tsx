"use server"
import { signIn } from "@/app/actions";

export default async function sign_in() {

  return (
    <div className="search">
      <form className="sign-in" action={signIn}>
        <label htmlFor="uname">Username</label>
        <input
          type="text"
          placeholder="Enter Username"
          name="uname"
          required
        />

        <label htmlFor="passwd">Password</label>
        <input
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
