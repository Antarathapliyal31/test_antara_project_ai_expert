import ReceiptCard from "../components/ReceiptCard";
import UploadReceipt from "../components/UploadReceipt";
import { useReceipts } from "../hooks/useReceipts";

export default function Receipts() {
  const receipts = useReceipts();

  return (
    <>
      <h1>Receipts</h1>
      <UploadReceipt />
      {receipts.map((r) => (
        <ReceiptCard
          key={r.id}
          merchant={r.merchant}
          total={r.total}
          purchase_date={r.purchase_date}
          category={r.category}
          is_anomaly={r.is_anomaly}
        />
      ))}
    </>
  );
}
