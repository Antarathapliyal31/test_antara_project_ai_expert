import { useEffect, useState } from "react";

import { apiGet } from "../api/client";

export type Receipt = {
  id: number;
  merchant: string;
  purchase_date: string;
  total: number;
  category: string | null;
  is_anomaly: boolean;
};

export function useReceipts(): Receipt[] {
  const [receipts, setReceipts] = useState<Receipt[]>([]);
  useEffect(() => {
    apiGet<Receipt[]>("/expenses")
      .then(setReceipts)
      .catch(() => setReceipts([]));
  }, []);
  return receipts;
}
