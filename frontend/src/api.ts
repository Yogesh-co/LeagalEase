const base = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8001';
async function post<T>(path: string, body: unknown): Promise<T> {
  let response: Response;
  try { response = await fetch(`${base}${path}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }); }
  catch { throw new Error('Unable to reach the LegalEase service. Make sure the backend is running.'); }
  if (!response.ok) { const data = await response.json().catch(() => ({})); throw new Error(data.detail || `Request failed (${response.status})`); }
  return response.json();
}
export const generate = (data: { document_type: string; party_one: string; party_two: string; effective_date: string; key_terms: string }) => post<{document: string; document_type: string}>('/api/documents/generate', data);
export const ask = (kind: 'summary' | 'explain', text: string) => post<{result:string}>(`/api/ai/${kind}`, {text});
export async function download(format: 'pdf'|'docx'|'txt', text: string) {
  const response = await fetch(`${base}/api/exports/${format}`, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text})});
  if (!response.ok) { const data = await response.json().catch(()=>({})); throw new Error(data.detail || `Export failed (${response.status})`); }
  const blob = await response.blob(); const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = `legalease-document.${format}`; a.click(); URL.revokeObjectURL(url);
}
