
"use client";

import { Suspense } from "react";
import CallbackContent from "./callback-handler"

export default function Page() {
  return (
    <Suspense fallback={<p>Signing you in...</p>}>
      <CallbackContent />
    </Suspense>
  );
}