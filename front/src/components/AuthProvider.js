import { createContext, useEffect, useState } from "react";
import useFetchRequest from "../hooks/useFetchRequest";
import { isTokenValid, parseFullJwt, parseJwt } from "../utils/jwtUtils";

// Context to store all related with auth
// This is a template to understand what is stored on context
export const AuthContext = createContext({
  email: undefined,
  jwt: undefined,
  signup: () => {},
  signin: () => {},
  signout: () => {},
  setJwt: () => {},
  isTokenValid: () => {},
});

export function AuthProvider({ children }) {
  let [email, setEmail] = useState(null);
  let [jwt, setJwt] = useState(null);

  const { post } = useFetchRequest();

  useEffect(() => {
    const storedJwt = localStorage.getItem("access_token");
    if (isTokenValid(storedJwt)) {
      setJwt(storedJwt);
      console.info("Hello there", storedJwt);
      setEmail(parseFullJwt(storedJwt)["email"]);
    } else {
      localStorage.removeItem("access_token");
    }
  }, []);

  let signup = (data, onSuccess, onFailure) => {
    post("/signup", data)
      .then((res) => {
        onSuccess();
        setTimeout(() => {
          localStorage.setItem("access_token", res.access_token);
          setJwt(res.access_token);
          setEmail(data.email);
          console.info(" Setted: ", res.access_token);
          console.info(" Setted: ", data.email);
        }, 5000);
      })
      .catch((error) => {
        onFailure(error);
      });
  };

  let signin = (data, onSuccess, onFailure) => {
    post("/signin", data)
      .then((res) => {
        if (res.access_token) {
          localStorage.setItem("access_token", res.access_token);
          setJwt(res.access_token);
          setEmail(data.email);
          console.info(" Setted: ", res.access_token);
          console.info(" Setted: ", data.email);
          onSuccess();
        } else {
          onFailure();
        }
      })
      .catch((error) => {
        onFailure(error);
      });
  };

  let signout = (callback) => {
    setEmail(null);
    setJwt(null);
    localStorage.removeItem("access_token");
    callback();
  };

  let value = { jwt, setJwt, email, signup, signin, signout, isTokenValid };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
