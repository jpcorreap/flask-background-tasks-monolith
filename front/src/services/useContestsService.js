import { useCallback, useMemo } from "react";
import useFetchRequest from "../hooks/useFetchRequest";
import { parseStringToVeryShortDate } from "../utils/dateUtils";

export function useContestsService() {
  const { post, get } = useFetchRequest();

  const getContests = useCallback(
    (onSuccess, onFailure) => {
      return get("/contests")
        .then((res) => {
          const parsedResponse = res.map((contest) => ({
            ...contest,
            start_date: parseStringToVeryShortDate(contest.start_date),
            end_date: parseStringToVeryShortDate(contest.end_date),
          }));
          onSuccess(parsedResponse);
        })
        .catch((error) => {
          console.info("Erroor", { error });
          onFailure(error);
        });
    },
    [get]
  );

  return { getContests };
}
