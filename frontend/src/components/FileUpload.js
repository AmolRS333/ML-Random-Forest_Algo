import React, { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";

const FileUpload = ({ onAnalysisComplete, onError }) => {
  const [isUploading, setIsUploading] = useState(false);

  const onDrop = useCallback(
    async (acceptedFiles) => {
      const file = acceptedFiles[0];
      if (!file) return;

      if (!file.name.endsWith(".csv")) {
        onError("Please upload a CSV file");
        return;
      }

      const formData = new FormData();
      formData.append("file", file);

      setIsUploading(true);

      try {
        const response = await axios.post(
          "http://127.0.0.1:8001/api/analyze",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        onAnalysisComplete(response.data);
      } catch (error) {
        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          onError(
            error.response.data.detail ||
              "Error analyzing file. Please try again."
          );
        } else if (error.request) {
          // The request was made but no response was received
          onError(
            "No response from server. Please check if the backend is running."
          );
        } else {
          // Something happened in setting up the request that triggered an Error
          onError("Error analyzing file. Please try again.");
        }
        console.error("Upload error:", error);
      } finally {
        setIsUploading(false);
      }
    },
    [onAnalysisComplete, onError]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "text/csv": [".csv"],
    },
    multiple: false,
  });

  return (
    <div className="w-full max-w-xl mx-auto">
      <div
        {...getRootProps()}
        className={`p-8 border-2 border-dashed rounded-lg text-center cursor-pointer transition-colors
          ${
            isDragActive
              ? "border-blue-500 bg-blue-50"
              : "border-gray-300 hover:border-blue-400"
          }`}
      >
        <input {...getInputProps()} />
        <div className="space-y-4">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            stroke="currentColor"
            fill="none"
            viewBox="0 0 48 48"
            aria-hidden="true"
          >
            <path
              d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
              strokeWidth={2}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <div className="text-gray-600">
            {isUploading ? (
              <p>Analyzing file...</p>
            ) : isDragActive ? (
              <p>Drop the CSV file here...</p>
            ) : (
              <p>Drag and drop a CSV file here, or click to select one</p>
            )}
          </div>
          <p className="text-sm text-gray-500">Only CSV files are supported</p>
        </div>
      </div>
    </div>
  );
};

export default FileUpload;
