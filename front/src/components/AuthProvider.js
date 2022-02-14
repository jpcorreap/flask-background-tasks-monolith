import { createContext, useState } from "react";
import { authProvider } from "../helpers/auth";

export const AuthContext = createContext({
  user: undefined,
  signin: (user, callback) => {},
  signout: (callback) => {},
});

export function AuthProvider({ children }) {
  let [user, setUser] = useState(null);

  let signin = (newUser, callback) => {
    return authProvider.signin(() => {
      setUser(newUser);
      callback();
    });
  };

  let signout = (callback) => {
    return authProvider.signout(() => {
      setUser(null);
      callback();
    });
  };

  let value = { user, signin, signout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
