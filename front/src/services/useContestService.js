import { useCallback } from "react";
import useFetchRequest from "../hooks/useFetchRequest";

export function useContestService() {
  const { get, getMedia, postMedia, httpDelete, putMedia } = useFetchRequest();

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

  const createContest = useCallback(
    (formData, onSuccess, onFailure) => {
      return postMedia("/contests", formData)
        .then((res) => {
          console.info(res);
          onSuccess();
        })
        .catch((error) => {
          console.info("AQUÍÍ 2", { error });
          onFailure(error);
        });
    },
    [postMedia]
  );

  const updateContest = useCallback(
    (prevUrl, formData, onSuccess, onFailure) => {
      return putMedia("/contests/" + prevUrl, formData)
        .then((res) => {
          onSuccess();
        })
        .catch((error) => {
          console.info("AQUÍÍ 2", { error });
          onFailure(error);
        });
    },
    [putMedia]
  );

  const deleteContest = useCallback(
    (contestUrl, onSuccess, onFailure) => {
      return httpDelete("/contests/" + contestUrl)
        .then((res) => {
          console.info("ELIMINAOOOO", { res });
          onSuccess(res);
        })
        .catch((error) => {
          console.info("AQUÍÍ 2 ERROOOR", { error });
          onFailure(error);
        });
    },
    [httpDelete]
  );

  return {
    getContestDetail,
    getBanner,
    createContest,
    deleteContest,
    updateContest,
  };
}
