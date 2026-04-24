import axios from "axios";

export const api = axios.create({
  baseURL: "https://sudama-interiors.onrender.com/api",
});