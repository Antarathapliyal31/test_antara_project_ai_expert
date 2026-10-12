import { Line, LineChart, Tooltip, XAxis, YAxis } from "recharts";

type Point = { month: string; total: number };

export default function MonthlyTrend({ data }: { data: Point[] }) {
  return (
    <LineChart width={600} height={300} data={data}>
      <XAxis dataKey="month" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="total" />
    </LineChart>
  );
}
