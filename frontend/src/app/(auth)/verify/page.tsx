"use client";

import { useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import api from "@/lib/api";

export default function VerifyPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const token = searchParams.get("token");

  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (token) {
      verifyToken(token);
    }
  }, [token]);

  const verifyToken = async (t: string) => {
    setStatus("loading");
    try {
      const res = await api.get(`/accounts/verify/${t}`);
      setMessage(res.data.message);
      setStatus("success");
      setTimeout(() => router.push("/login"), 3000);
    } catch (err: any) {
      setMessage(err.response?.data?.detail || "Verification failed");
      setStatus("error");
    }
  };

  // no token in URL — show "check your email" notice
  if (!token) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-md text-center">
          <div className="text-5xl mb-4">📧</div>
          <h1 className="text-2xl font-bold text-gray-800 mb-2">Check your email</h1>
          <p className="text-gray-500 text-sm">
            We sent a verification link to your email address. Click the link to activate your account.
          </p>
          <p className="text-gray-400 text-xs mt-4">
            Didn't get it? Check your spam folder.
          </p>
        </div>
      </div>
    );
  }

  // token in URL — show verification result
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-md text-center">
        {status === "loading" && (
          <>
            <div className="text-5xl mb-4">⏳</div>
            <h1 className="text-2xl font-bold text-gray-800">Verifying...</h1>
          </>
        )}

        {status === "success" && (
          <>
            <div className="text-5xl mb-4">✅</div>
            <h1 className="text-2xl font-bold text-gray-800 mb-2">Email verified!</h1>
            <p className="text-gray-500 text-sm">{message}</p>
            <p className="text-gray-400 text-xs mt-4">Redirecting to login...</p>
          </>
        )}

        {status === "error" && (
          <>
            <div className="text-5xl mb-4">❌</div>
            <h1 className="text-2xl font-bold text-gray-800 mb-2">Verification failed</h1>
            <p className="text-red-500 text-sm">{message}</p>
            <a href="/login" className="text-blue-600 text-sm hover:underline mt-4 block">
              Back to login
            </a>
          </>
        )}
      </div>
    </div>
  );
}