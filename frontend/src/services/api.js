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
