import { createContext, useEffect, useState } from "react";
import useFetchRequest from "../hooks/useFetchRequest";
import { parseJwt } from "../utils/jwtUtils";

export const AuthContext = createContext({
  user: undefined,
  signin: (user, callback) => {},
  signout: (callback) => {},
});

export function AuthProvider({ children }) {
  let [email, setEmail] = useState(null);
  let [jwt, setJwt] = useState(null);
  const { post } = useFetchRequest();

  let isTokenValid = (jwtToCheck) =>
    !!jwtToCheck &&
    Boolean(parseJwt(jwtToCheck).exp * 1000 > new Date().getTime());

  useEffect(() => {
    const storedJwt = sessionStorage.getItem("access_token");
    if (isTokenValid(storedJwt)) {
      setJwt(storedJwt);
      console.info("Hello there", storedJwt);
    } else {
      sessionStorage.removeItem("access_token");
    }
  }, []);

  let signup = (data, callback) => {
    post("/signup", data).then((res) => {
      sessionStorage.setItem("access_token", res.access_token);
      setJwt(res.access_token);
      console.info(" Setted: ", res.access_token);
    });
    callback();
  };

  let signin = (newUser, callback) => {
    return () => {
      setEmail(newUser);
      callback();
    };
  };

  let signout = (callback) => {
    return () => {
      setEmail(null);
      callback();
    };
  };

  let value = { jwt, setJwt, email, signup, signin, signout, isTokenValid };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
