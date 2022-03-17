import { useMemo } from "react";
import { useAuth } from "../hooks/useAuth";
import useFetchRequest from "../hooks/useFetchRequest";

export default function useOtroService() {
  const { post } = useFetchRequest();
  const { token } = useAuth();

  return useMemo(() => ({}), [post]);
}
