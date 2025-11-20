import React from "react";

interface WeatherChartTableProps {
  data: any[];
  todayISO: string;
}

const WeatherChartTable: React.FC<WeatherChartTableProps> = ({ data, todayISO }) => (
  <div className="mt-6">
    <h2 className="text-lg font-semibold mb-4">Weather Data Table</h2>
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white border border-gray-200 rounded-lg">
        <thead>
          <tr className="bg-gray-100 text-gray-700 uppercase text-sm leading-normal">
            <th className="py-3 px-5 text-left">Date</th>
            <th className="py-3 px-5 text-left">Max Temp (°C)</th>
            <th className="py-3 px-5 text-left">Min Temp (°C)</th>
            <th className="py-3 px-5 text-left">Precipitation (mm)</th>
            <th className="py-3 px-5 text-left">Pressure (hPa)</th>
            <th className="py-3 px-5 text-left">Wind Speed (km/h)</th>
            <th className="py-3 px-5 text-left">Humidity (%)</th>
          </tr>
        </thead>
        <tbody className="text-gray-600 text-sm leading-relaxed">
          {data.map((rec: any) => (
            <tr
              key={rec.xKey}
              className={rec.date === todayISO ? "bg-yellow-100 font-bold" : "hover:bg-gray-50 transition-colors"}
            >
              <td className="py-3 px-5 border-b">{rec.date}</td>
              <td className="py-3 px-5 border-b">{rec.temperature_2m_max}</td>
              <td className="py-3 px-5 border-b">{rec.temperature_2m_min}</td>
              <td className="py-3 px-5 border-b">{rec.precipitation_sum}</td>
              <td className="py-3 px-5 border-b">{rec.pressure_msl_mean}</td>
              <td className="py-3 px-5 border-b">{rec.wind_speed_10m_max}</td>
              <td className="py-3 px-5 border-b">{rec.relative_humidity_2m_max}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);

export default WeatherChartTable;
