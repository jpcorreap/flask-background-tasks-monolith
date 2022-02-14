import { useParams } from "react-router-dom";

export default function Contest() {
  let params = useParams();
  return <h2>Contest: {params.contestId}</h2>;
}