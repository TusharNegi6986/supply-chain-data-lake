
import { useCallback, useEffect, useState } from "react";
import {
  Database,
  RefreshCw,
  FileSpreadsheet,
  CheckCircle2,
  AlertCircle,
  ArrowLeft,
  Eye,
  LoaderCircle,
} from "lucide-react";
import { getDatasets, getDatasetDetails } from "../services/api";

function DatasetLibrary() {
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [detailsLoading, setDetailsLoading] = useState(false);
  const [detailsError, setDetailsError] = useState("");

  const loadDatasets = useCallback(async () => {
    setLoading(true);
    setError("");

    try {
      const data = await getDatasets();
      setDatasets(data?.datasets ?? []);
    } catch (err) {
      setError(
        typeof err?.response?.data?.detail === "string"
          ? err.response.data.detail
          : "Unable to load datasets. Check that the backend is running."
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadDatasets();
  }, [loadDatasets]);

  const openDatasetDetails = async (datasetId) => {
    setSelectedDataset(null);
    setDetailsLoading(true);
    setDetailsError("");

    try {
      const data = await getDatasetDetails(datasetId);
      setSelectedDataset(data?.dataset ?? null);

      if (!data?.dataset) {
        setDetailsError("Dataset details were not returned by the server.");
      }
    } catch (err) {
      setDetailsError(
        typeof err?.response?.data?.detail === "string"
          ? err.response.data.detail
          : "Unable to load dataset details."
      );
    } finally {
      setDetailsLoading(false);
    }
  };

  const formatBytes = (bytes = 0) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  const formatDate = (value) => {
    if (!value) return "—";

    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
  };

  const renderDetails = () => {
    if (detailsLoading) {
      return (
        <div className="dataset-library-empty">
          <LoaderCircle size={28} />
          <p>Loading dataset details...</p>
        </div>
      );
    }

    if (detailsError) {
      return (
        <div className="dataset-message dataset-error">
          <AlertCircle size={18} />
          <span>{detailsError}</span>
        </div>
      );
    }

    if (!selectedDataset) return null;

    const dataset = selectedDataset;
    const mappings = Array.isArray(dataset.semantic_mapping)
      ? dataset.semantic_mapping
      : [];

    return (
      <div className="dataset-detail">
        <div className="view-heading">
          <div>
            <span className="section-kicker">DATA MANAGEMENT</span>
            <h2>{dataset.filename}</h2>
            <p>Dataset metadata, data quality, and semantic mappings.</p>
          </div>

          <button
            className="refresh-button"
            onClick={() => setSelectedDataset(null)}
          >
            <ArrowLeft size={16} />
            Back to library
          </button>
        </div>

        <div className="dataset-library-summary">
          <Database size={22} />
          <div>
            <span>Processing Status</span>
            <strong>{dataset.processing_status}</strong>
          </div>
        </div>

        <div className="dataset-detail-grid">
          <div className="dataset-detail-item">
            <span>Rows</span>
            <strong>{dataset.row_count ?? "—"}</strong>
          </div>
          <div className="dataset-detail-item">
            <span>Columns</span>
            <strong>{dataset.column_count ?? "—"}</strong>
          </div>
          <div className="dataset-detail-item">
            <span>Duplicate rows</span>
            <strong>{dataset.duplicate_rows ?? "—"}</strong>
          </div>
          <div className="dataset-detail-item">
            <span>Missing values</span>
            <strong>{dataset.missing_values ?? "—"}</strong>
          </div>
          <div className="dataset-detail-item">
            <span>Completeness</span>
            <strong>
              {dataset.completeness_percentage != null
                ? `${dataset.completeness_percentage}%`
                : "—"}
            </strong>
          </div>
          <div className="dataset-detail-item">
            <span>File size</span>
            <strong>{formatBytes(dataset.file_size_bytes)}</strong>
          </div>
        </div>

        <div className="dataset-detail-section">
          <h3>File information</h3>
          <p><strong>Dataset ID:</strong> {dataset.dataset_id}</p>
          <p><strong>File type:</strong> {dataset.file_type?.toUpperCase()}</p>
          <p><strong>SHA-256:</strong></p>
          <code className="dataset-hash">{dataset.sha256}</code>
          <p><strong>Uploaded:</strong> {formatDate(dataset.uploaded_at)}</p>
        </div>

        <div className="dataset-detail-section">
          <h3>Semantic mappings ({mappings.length})</h3>

          {mappings.length === 0 ? (
            <p>No semantic mappings are stored for this dataset.</p>
          ) : (
            <div className="dataset-mapping-table-wrap">
              <table className="dataset-mapping-table">
                <thead>
                  <tr>
                    <th>Column</th>
                    <th>Normalized name</th>
                    <th>Semantic type</th>
                    <th>Data type</th>
                    <th>Unique values</th>
                    <th>Confidence</th>
                  </tr>
                </thead>
                <tbody>
                  {mappings.map((mapping, index) => (
                    <tr
                      key={`${mapping.column_name}-${index}`}
                    >
                      <td>{mapping.column_name}</td>
                      <td>{mapping.normalized_name}</td>
                      <td>{mapping.semantic_type}</td>
                      <td>{mapping.data_type}</td>
                      <td>{mapping.unique_count ?? "—"}</td>
                      <td>{mapping.confidence ?? "—"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    );
  };

  if (selectedDataset || detailsLoading || detailsError) {
    return (
      <div className="view-layout">
        {renderDetails()}
        {!selectedDataset && !detailsLoading && detailsError && (
          <button
            className="refresh-button"
            onClick={() => setDetailsError("")}
          >
            <ArrowLeft size={16} />
            Back to library
          </button>
        )}
      </div>
    );
  }

  return (
    <div className="view-layout">
      <div className="view-heading">
        <div>
          <span className="section-kicker">DATA MANAGEMENT</span>
          <h2>Dataset Library</h2>
          <p>Browse datasets uploaded to your data platform.</p>
        </div>

        <button
          className="refresh-button"
          onClick={loadDatasets}
          disabled={loading}
        >
          <RefreshCw size={16} />
          {loading ? "Loading..." : "Refresh"}
        </button>
      </div>

      <div className="dataset-library-summary">
        <Database size={22} />
        <div>
          <span>Total Datasets</span>
          <strong>{datasets.length}</strong>
        </div>
      </div>

      {error && (
        <div className="dataset-message dataset-error">
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      )}

      {loading ? (
        <p>Loading datasets...</p>
      ) : datasets.length === 0 && !error ? (
        <div className="dataset-library-empty">
          <Database size={32} />
          <h3>No datasets found</h3>
          <p>Upload a CSV or Excel file to get started.</p>
        </div>
      ) : (
        <div className="dataset-library-grid">
          {datasets.map((dataset) => (
            <article
              className="dataset-library-card"
              key={`${dataset.dataset_id}-${dataset.filename}`}
            >
              <div className="dataset-library-card-header">
                <div className="dataset-library-file-icon">
                  <FileSpreadsheet size={22} />
                </div>

                <span
                  className={
                    dataset.processed
                      ? "dataset-status dataset-status-success"
                      : "dataset-status"
                  }
                >
                  {dataset.processed ? (
                    <>
                      <CheckCircle2 size={14} />
                      Processed
                    </>
                  ) : (
                    "Pending"
                  )}
                </span>
              </div>

              <h3 title={dataset.filename}>{dataset.filename}</h3>

              <p className="dataset-library-id">{dataset.dataset_id}</p>

              <div className="dataset-library-meta">
                <span>{dataset.file_type?.toUpperCase()}</span>
                <span>{formatBytes(dataset.file_size_bytes)}</span>
              </div>

              <button
                className="refresh-button"
                onClick={() => openDatasetDetails(dataset.dataset_id)}
              >
                <Eye size={16} />
                View details
              </button>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}

export default DatasetLibrary;
