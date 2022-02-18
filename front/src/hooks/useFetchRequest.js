import { useCallback, useMemo } from "react";
import { useAuth } from "./useAuth";

export const fetch_url = "http://172.24.41.21/api";

export default function useFetchRequest() {
  const { jwt } = useAuth();

  const _getHeaders = useCallback(async () => {
    const headers = new Headers();
    headers.append("Content-Type", "application/json");
    if (jwt) headers.append("Authorization", `Bearer ${jwt}`);
    return headers;
  }, [jwt]);

  const _getHeadersMedia = useCallback(async () => {
    const headers = new Headers();
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

      async postMedia(path, formData) {
        const headers = await _getHeadersMedia();
        return fetch(fetch_url + path, {
          headers,
          method: "POST",
          body: formData,
        }).then((res) => {
          console.info({ Response: res });
          console.info({ Response: res.status });
          return res.json();
        });
      },

      async putMedia(path, formData) {
        const headers = await _getHeadersMedia();
        return fetch(fetch_url + path, {
          headers,
          method: "PUT",
          body: formData,
        }).then((res) => {
          console.info({ res });
          return res.json();
        });
      },

      async httpDelete(path, body) {
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
