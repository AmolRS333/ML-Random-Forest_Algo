import React, { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";

const FileUpload = ({ onAnalysisComplete, onError }) => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [fileName, setFileName] = useState("");

  const onDrop = useCallback(
    async (acceptedFiles) => {
      const file = acceptedFiles[0];
      if (!file) return;

      if (!file.name.endsWith(".csv")) {
        onError("Please upload a CSV file");
        return;
      }

      setFileName(file.name);
      const formData = new FormData();
      formData.append("file", file);

      setIsUploading(true);
      setUploadProgress(0);

      try {
        const response = await axios.post(
          "http://127.0.0.1:8001/api/analyze",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
            onUploadProgress: (progressEvent) => {
              const progress = Math.round(
                (progressEvent.loaded * 100) / progressEvent.total
              );
              setUploadProgress(progress);
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
        setUploadProgress(0);
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
        className={`relative p-8 border-2 border-dashed rounded-lg text-center cursor-pointer transition-all duration-300 ease-in-out
          ${
            isDragActive
              ? "border-blue-500 bg-blue-50 scale-105"
              : "border-gray-300 hover:border-blue-400 hover:bg-gray-50"
          }
          ${isUploading ? "opacity-75 cursor-not-allowed" : ""}`}
      >
        <input {...getInputProps()} disabled={isUploading} />

        <div className="space-y-4">
          {isUploading ? (
            <>
              <div className="relative w-16 h-16 mx-auto">
                <div className="absolute inset-0 border-4 border-blue-200 rounded-full"></div>
                <div
                  className="absolute inset-0 border-4 border-blue-500 rounded-full"
                  style={{
                    clipPath: `polygon(0 0, ${uploadProgress}% 0, ${uploadProgress}% 100%, 0 100%)`,
                  }}
                ></div>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-sm font-medium text-blue-500">
                    {uploadProgress}%
                  </span>
                </div>
              </div>
              <p className="text-gray-600 font-medium">
                Analyzing {fileName}...
              </p>
            </>
          ) : (
            <>
              <div className="relative">
                <svg
                  className={`mx-auto h-12 w-12 transition-colors duration-300 ${
                    isDragActive ? "text-blue-500" : "text-gray-400"
                  }`}
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
                {isDragActive && (
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="bg-blue-500 text-white px-4 py-2 rounded-full text-sm font-medium animate-pulse">
                      Drop to upload
                    </div>
                  </div>
                )}
              </div>
              <div className="space-y-2">
                <p className="text-gray-600 font-medium">
                  {isDragActive
                    ? "Drop your CSV file here"
                    : "Drag and drop your CSV file here"}
                </p>
                <p className="text-sm text-gray-500">
                  or click to browse files
                </p>
              </div>
            </>
          )}
        </div>

        {fileName && !isUploading && (
          <div className="mt-4 text-sm text-gray-500">
            Last uploaded: {fileName}
          </div>
        )}
      </div>

      <div className="mt-4 text-center">
        <p className="text-sm text-gray-500">Supported file type: CSV</p>
      </div>
    </div>
  );
};

export default FileUpload;
