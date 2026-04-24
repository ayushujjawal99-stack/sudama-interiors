"use client";

import { useEffect, useState } from "react";
import { api } from "@/services/api";

export default function LeadsPage() {
  const [leads, setLeads] = useState([]);

  useEffect(() => {
    api.get("/leads/")
      .then((res) => setLeads(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="p-8">

      <h1 className="text-2xl font-bold mb-6">Leads</h1>

      <div className="bg-white rounded-xl shadow overflow-hidden">

        <table className="w-full text-sm">

          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="p-4 text-left">Name</th>
              <th>Service</th>
              <th>Budget</th>
            </tr>
          </thead>

          <tbody>
            {leads.map((lead: any) => (
              <tr key={lead.id} className="border-b hover:bg-gray-50">
                <td className="p-4">{lead.name}</td>
                <td>{lead.service}</td>
                <td>{lead.budget}</td>
              </tr>
            ))}
          </tbody>

        </table>

      </div>

    </div>
  );
}