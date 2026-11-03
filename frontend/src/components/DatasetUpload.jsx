import { useState } from "react";
import {
  Upload,
  FileSpreadsheet,
  CheckCircle2,
  AlertCircle,
} from "lucide-react";
import { uploadDataset } from "../services/api";

function DatasetUpload() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a CSV or Excel file first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await uploadDataset(file);
      setResult(data);
    } catch (err) {
      const detail = err.response?.data?.detail;
      setError(
        typeof detail === "string"
          ? detail
          : Array.isArray(detail)
            ? detail.map((item) => item.msg || JSON.stringify(item)).join("; ")
            : "Upload failed. Check the selected file and backend logs.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="view-layout">
      <div className="view-heading">
        <div>
          <span className="section-kicker">DATA MANAGEMENT</span>
          <h2>Upload Dataset</h2>
          <p>Upload a dataset for profiling and data quality analysis.</p>
        </div>
      </div>

      <div className="dataset-upload-card">
        <div className="dataset-upload-icon">
          <Upload size={28} />
        </div>

        <h3>Import your dataset</h3>
        <p>Select a supported CSV file to begin analysis.</p>

        <label className="dataset-file-picker">
          <FileSpreadsheet size={20} />
          <span>{file ? file.name : "Choose a CSV file"}</span>
          <input
            type="file"
            accept=".csv"
            onChange={(event) => {
              setFile(event.target.files?.[0] || null);
              setResult(null);
              setError("");
            }}
          />
        </label>

        {file && (
          <p className="dataset-file-size">
            {(file.size / 1024).toFixed(1)} KB
          </p>
        )}

        <button
          className="refresh-button dataset-upload-button"
          onClick={handleUpload}
          disabled={!file || loading}
        >
          <Upload size={16} />
          {loading ? "Uploading and profiling..." : "Upload and Analyze"}
        </button>

        {error && (
          <div className="dataset-message dataset-error">
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        {result && (
          <div className="dataset-result">
            <div className="dataset-message dataset-success">
              <CheckCircle2 size={18} />
              <strong>Dataset uploaded successfully</strong>
            </div>

            <div className="dataset-result-grid">
              <div>
                <span>Dataset ID</span>
                <strong>{result.dataset_id}</strong>
              </div>
              <div>
                <span>Rows</span>
                <strong>{result.profile?.rows?.toLocaleString() ?? "—"}</strong>
              </div>
              <div>
                <span>Columns</span>
                <strong>{result.profile?.columns ?? "—"}</strong>
              </div>
              <div>
                <span>Duplicate Rows</span>
                <strong>
                  {result.profile?.duplicate_rows?.toLocaleString() ?? "—"}
                </strong>
              </div>
              <div>
                <span>Missing Values</span>
                <strong>
                  {result.profile?.total_missing_values?.toLocaleString() ??
                    "—"}
                </strong>
              </div>
              <div>
                <span>Completeness</span>
                <strong>
                  {result.profile?.completeness_percentage ?? "—"}%
                </strong>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default DatasetUpload;
