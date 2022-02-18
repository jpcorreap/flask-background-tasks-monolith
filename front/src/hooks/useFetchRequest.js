import { useCallback, useMemo } from "react";
import { useAuth } from "./useAuth";

const fetch_url =
  process.env.NODE_ENV === "production" ? "" : process.env.REACT_APP_FETCH_URL;

export default function useFetchRequest() {
  const { jwt } = useAuth();

  const _getHeaders = useCallback(async () => {
    const headers = new Headers();
    headers.append("Content-Type", "application/json");
    if (jwt) headers.append("Authorization", `Bearer ${jwt}`);
    return headers;
  }, [jwt]);

  return useMemo(
    () => ({
      async get(path) {
        const headers = await _getHeaders();
        return fetch(fetch_url + path, { headers, method: "GET" }).then(
          (res) => {
            console.info({ res });
            return res.json();
          }
        );
      },

      async getMedia(path) {
        const headers = await _getHeaders();
        return fetch(fetch_url + path, { headers, method: "GET" }).then((res) =>
          res.blob()
        );
      },

      async patch(path, body) {
        const headers = await _getHeaders();
        return fetch(fetch_url + path, {
          headers,
          method: "PATCH",
          body: JSON.stringify(body),
        }).then((res) => {
          console.info({ Response: res });
          return res.json();
        });
      },

      async post(path, body) {
        const headers = await _getHeaders();
        return fetch(fetch_url + path, {
          headers,
          method: "POST",
          body: JSON.stringify(body),
        }).then((res) => {
          console.info({ Response: res });
          console.info({ Response: res.status });
          return res.json();
        });
      },

      async put(path, body) {
        const headers = await _getHeaders();
        return fetch(fetch_url + path, {
          headers,
          method: "PUT",
          body: JSON.stringify(body),
        }).then((res) => {
          console.info({ res });
          return res.json();
        });
      },

      async delete(path, body) {
        const headers = await _getHeaders();
        return fetch(fetch_url + path, {
          headers,
          method: "DELETE",
          body: JSON.stringify(body),
        }).then((res) => {
          console.info({ res });
          return res.json();
        });
      },
    }),
    [_getHeaders]
  );
}
