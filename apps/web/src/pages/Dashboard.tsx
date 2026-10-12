import { useEffect, useState } from "react";

import { apiGet } from "../api/client";
import MonthlyTrend from "../components/charts/MonthlyTrend";

type TrendPoint = { month: string; total: number };

export default function Dashboard() {
  const [trends, setTrends] = useState<TrendPoint[]>([]);

  useEffect(() => {
    apiGet<TrendPoint[]>("/dashboard/trends")
      .then(setTrends)
      .catch(() => setTrends([]));
  }, []);

  return (
    <>
      <h1>Dashboard</h1>
      <MonthlyTrend data={trends} />
    </>
  );
}
