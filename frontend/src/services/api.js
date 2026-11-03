import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export const getKPIs = async () => {
  const response = await API.get("/api/kpis");
  return response.data;
};

export const getMonthlySales = async () => {
  const response = await API.get("/api/monthly-sales");
  return response.data;
};



export const getCategories = async () => {
  const response = await API.get("/api/categories");
  return response.data;
};

export const getDelivery = async () => {
  const response = await API.get("/api/delivery");
  return response.data;
};

export const getShippingModes = async () => {
  const response = await API.get("/api/shipping-modes");
  return response.data;
};

export const getWarehouses = async () => {
  const response = await API.get("/api/warehouses");
  return response.data;
};


export const uploadDataset = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

 const response = await API.post(
  "/api/datasets/upload",
  formData,
  {
    headers: {
      "Content-Type": undefined,
    },
  }
);

  return response.data;
};

export const getDatasets = async () => {
  const response = await API.get("/api/datasets");
  return response.data;
};


export const getDatasetDetails = async (datasetId) => {
  const response = await API.get(
    `/api/datasets/${encodeURIComponent(datasetId)}`
  );
  return response.data;
};
