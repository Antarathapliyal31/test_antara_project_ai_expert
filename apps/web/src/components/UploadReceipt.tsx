import { useState } from "react";

import { apiUpload } from "../api/client";

export default function UploadReceipt() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<string>("");

  const onSubmit = async () => {
    if (!file) return;
    setStatus("uploading…");
    try {
      await apiUpload("/receipts", file);
      setStatus("uploaded");
    } catch (err) {
      setStatus(`failed: ${(err as Error).message}`);
    }
  };

  return (
    <div>
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files?.[0] ?? null)}
      />
      <button onClick={onSubmit} disabled={!file}>
        Upload
      </button>
      <span>{status}</span>
    </div>
  );
}
