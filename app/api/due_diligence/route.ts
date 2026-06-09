import { NextResponse } from "next/server"

// Forward the multipart form-data request to the FastAPI backend.
// Local dev defaults to the uvicorn server; production should set NEXT_PUBLIC_BACKEND_URL
// (or BACKEND_URL) to the deployed FastAPI endpoint.
const BACKEND_URL =
  process.env.BACKEND_URL ||
  process.env.NEXT_PUBLIC_BACKEND_URL ||
  "http://localhost:8000"

export const maxDuration = 300

export async function POST(request: Request) {
  try {
    const formData = await request.formData()

    const target = `${BACKEND_URL.replace(/\/$/, "")}/run_due_diligence`

    const backendResponse = await fetch(target, {
      method: "POST",
      body: formData,
    })

    const contentType = backendResponse.headers.get("content-type") || ""

    if (!backendResponse.ok) {
      let detail = `Backend responded with status ${backendResponse.status}`
      try {
        if (contentType.includes("application/json")) {
          const errJson = await backendResponse.json()
          detail = errJson.detail || JSON.stringify(errJson)
        } else {
          detail = (await backendResponse.text()) || detail
        }
      } catch {
        // keep default detail
      }
      return NextResponse.json({ error: detail }, { status: backendResponse.status })
    }

    const data = await backendResponse.json()
    return NextResponse.json(data)
  } catch (err) {
    const message =
      err instanceof Error ? err.message : "Unexpected error contacting the analysis backend."
    return NextResponse.json(
      {
        error: `Could not reach the due diligence backend at ${BACKEND_URL}. ${message}`,
      },
      { status: 502 },
    )
  }
}
