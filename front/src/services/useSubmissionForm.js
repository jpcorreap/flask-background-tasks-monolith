import { useCallback } from "react";
import useFetchRequest from "../hooks/useFetchRequest";

export function useSubmissionForm() {
  const { postMedia } = useFetchRequest();

  const createSubmission = useCallback(
    (contestUrl, formData, onSuccess, onFailure) => {
      return postMedia(`/contests/${contestUrl}/submissions`, formData)
        .then((res) => {
          console.info(res);
          onSuccess(res);
        })
        .catch((error) => {
          console.info("AQUÍÍ 2", { error });
          onFailure(error);
        });
    },
    [postMedia]
  );

  return { createSubmission };
}
