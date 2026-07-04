import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL ?? "http://localhost:8000";
const API_PREFIX = "/api/v1";

// Runtime: node (default) so we can stream multipart, use headers, etc.
export const dynamic = "force-dynamic";

async function proxy(req: NextRequest, params: { path: string[] }) {
  const subPath = params.path.join("/");
  const search = req.nextUrl.search;
  const target = `${BACKEND_URL}${API_PREFIX}/${subPath}${search}`;

  // Forward headers, but strip hop-by-hop ones + host.
  const headers = new Headers(req.headers);
  headers.delete("host");
  headers.delete("connection");
  headers.delete("content-length");

  const init: RequestInit = {
    method: req.method,
    headers,
    // Only include body for methods that can have one.
    body: ["GET", "HEAD"].includes(req.method) ? undefined : req.body,
    // Required in Node when streaming a request body.
    // @ts-expect-error duplex is a valid fetch option in Node 18+.
    duplex: "half",
    cache: "no-store",
    redirect: "manual",
  };

  try {
    const upstream = await fetch(target, init);

    // Pass through response, dropping content-encoding so the runtime can re-encode.
    const resHeaders = new Headers(upstream.headers);
    resHeaders.delete("content-encoding");
    resHeaders.delete("transfer-encoding");

    return new NextResponse(upstream.body, {
      status: upstream.status,
      statusText: upstream.statusText,
      headers: resHeaders,
    });
  } catch (err) {
    return NextResponse.json(
      {
        detail: "Backend unreachable",
        error: err instanceof Error ? err.message : String(err),
      },
      { status: 502 }
    );
  }
}

export async function GET(req: NextRequest, ctx: { params: { path: string[] } }) {
  return proxy(req, ctx.params);
}
export async function POST(req: NextRequest, ctx: { params: { path: string[] } }) {
  return proxy(req, ctx.params);
}
export async function PATCH(req: NextRequest, ctx: { params: { path: string[] } }) {
  return proxy(req, ctx.params);
}
export async function PUT(req: NextRequest, ctx: { params: { path: string[] } }) {
  return proxy(req, ctx.params);
}
export async function DELETE(req: NextRequest, ctx: { params: { path: string[] } }) {
  return proxy(req, ctx.params);
}
