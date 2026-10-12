import { Bar, BarChart, Tooltip, XAxis, YAxis } from "recharts";

type Slice = { category: string; total: number };

export default function CategoryBreakdown({ data }: { data: Slice[] }) {
  return (
    <BarChart width={600} height={300} data={data}>
      <XAxis dataKey="category" />
      <YAxis />
      <Tooltip />
      <Bar dataKey="total" />
    </BarChart>
  );
}
