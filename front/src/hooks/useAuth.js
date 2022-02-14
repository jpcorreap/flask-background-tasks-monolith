import { createContext, useContext } from "react";

export const AuthContext = createContext({
  user: undefined,
  signin: (user, callback) => {},
  signout: (callback) => {},
});

export function useAuth() {
  return useContext(AuthContext);
}
