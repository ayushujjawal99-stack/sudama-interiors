export default function Home() {
  return (
    <div className="p-10">

      <h1 className="text-3xl font-bold mb-8 text-gray-900">
        CRM Dashboard
      </h1>

      <div className="grid grid-cols-3 gap-6">

        <div className="crm-card">
          <p className="text-gray-500">Total Leads</p>
          <h2 className="text-3xl font-bold mt-2">124</h2>
        </div>

        <div className="crm-card">
          <p className="text-gray-500">Hot Leads</p>
          <h2 className="text-3xl font-bold mt-2">32</h2>
        </div>

        <div className="crm-card">
          <p className="text-gray-500">Closed Deals</p>
          <h2 className="text-3xl font-bold mt-2">18</h2>
        </div>

      </div>

    </div>
  );
}