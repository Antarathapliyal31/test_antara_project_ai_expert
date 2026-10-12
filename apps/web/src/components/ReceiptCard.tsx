type Props = {
  merchant: string;
  total: number;
  purchase_date: string;
  category: string | null;
  is_anomaly: boolean;
};

export default function ReceiptCard({ merchant, total, purchase_date, category, is_anomaly }: Props) {
  return (
    <div>
      <strong>{merchant}</strong> — ${total.toFixed(2)} on {purchase_date}{" "}
      ({category ?? "uncategorized"}){is_anomaly ? " ⚠️ unusual" : ""}
    </div>
  );
}
