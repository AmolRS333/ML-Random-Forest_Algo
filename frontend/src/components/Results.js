import React from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const Results = ({ data }) => {
  const formatMetricValue = (value) => {
    return value.toFixed(4);
  };

  const renderMetrics = () => {
    return (
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {Object.entries(data.metrics).map(([key, value]) => (
          <div key={key} className="bg-white p-4 rounded-lg shadow">
            <h3 className="text-sm font-medium text-gray-500 uppercase">
              {key}
            </h3>
            <p className="mt-1 text-2xl font-semibold text-gray-900">
              {formatMetricValue(value)}
            </p>
          </div>
        ))}
      </div>
    );
  };

  const renderFeatureImportance = () => {
    const chartData = {
      labels: Object.keys(data.feature_importances),
      datasets: [
        {
          label: "Feature Importance",
          data: Object.values(data.feature_importances),
          backgroundColor: "rgba(59, 130, 246, 0.5)",
          borderColor: "rgb(59, 130, 246)",
          borderWidth: 1,
        },
      ],
    };

    const options = {
      responsive: true,
      plugins: {
        legend: {
          display: false,
        },
        title: {
          display: true,
          text: "Feature Importance",
        },
      },
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    };

    return (
      <div className="bg-white p-4 rounded-lg shadow">
        <Bar data={chartData} options={options} />
      </div>
    );
  };

  const renderPlots = () => {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {Object.entries(data.plots).map(([key, value]) => (
          <div key={key} className="bg-white p-4 rounded-lg shadow">
            <h3 className="text-lg font-medium text-gray-900 mb-4 capitalize">
              {key.replace("_", " ")}
            </h3>
            <img
              src={`data:image/png;base64,${value}`}
              alt={key}
              className="w-full h-auto"
            />
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="space-y-8">
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Analysis Results
        </h2>
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div>
            <h3 className="text-sm font-medium text-gray-500">Problem Type</h3>
            <p className="mt-1 text-lg font-semibold text-gray-900 capitalize">
              {data.problem_type}
            </p>
          </div>
          <div>
            <h3 className="text-sm font-medium text-gray-500">Domain</h3>
            <p className="mt-1 text-lg font-semibold text-gray-900 capitalize">
              {data.domain}
            </p>
          </div>
        </div>
        {renderMetrics()}
      </div>

      {renderFeatureImportance()}
      {renderPlots()}
    </div>
  );
};

export default Results;
