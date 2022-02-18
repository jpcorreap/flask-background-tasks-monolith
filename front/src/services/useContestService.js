import { useCallback } from "react";
import useFetchRequest from "../hooks/useFetchRequest";

export function useContestService() {
  const { get, getMedia } = useFetchRequest();

  const getContestDetail = useCallback(
    (contestUrl, onSuccess, onFailure) => {
      return get("/contests/" + contestUrl)
        .then((res) => {
          console.info(res);
          onSuccess(res);
        })
        .catch((error) => {
          console.info("AQUÍÍ", { error });
          onFailure(error);
        });
    },
    [get]
  );

  const getBanner = useCallback(
    (contestUrl, onSuccess, onFailure) => {
      return getMedia("/contests/banner/" + contestUrl)
        .then((res) => {
          console.info(res);
          onSuccess(res);
        })
        .catch((error) => {
          console.info("AQUÍÍ 2", { error });
          onFailure(error);
        });
    },
    [get]
  );

  return { getContestDetail, getBanner };
}
