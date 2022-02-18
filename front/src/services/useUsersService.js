import { useCallback } from "react";
import useFetchRequest from "../hooks/useFetchRequest";

export function useUsersService() {
  const { get } = useFetchRequest();

  const getUserInfo = useCallback(
    (userId, onSuccess, onFailure) => {
      return get("/users/" + userId)
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

  return { getUserInfo };
}
