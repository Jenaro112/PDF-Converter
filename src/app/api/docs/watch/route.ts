import { NextRequest } from 'next/server';
import fs from 'fs';
import path from 'path';

export const dynamic = 'force-dynamic';

export async function GET(req: NextRequest) {
  const docsDir = path.join(process.cwd(), 'docs');
  
  if (!fs.existsSync(docsDir)) {
    fs.mkdirSync(docsDir, { recursive: true });
  }

  const stream = new ReadableStream({
    start(controller) {
      const encoder = new TextEncoder();
      
      const sendEvent = (event: string, data: any) => {
        try {
          controller.enqueue(encoder.encode(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`));
        } catch (e) {
          // controller might be closed
        }
      };
      
      sendEvent('connected', { message: 'watching docs' });
      
      let debounceTimer: NodeJS.Timeout | null = null;
      
      const watcher = fs.watch(docsDir, (eventType, filename) => {
        if (filename && filename.endsWith('.md')) {
          // debounce events to avoid multiple triggers for a single save
          if (debounceTimer) clearTimeout(debounceTimer);
          debounceTimer = setTimeout(() => {
            sendEvent('change', { eventType, filename });
          }, 300);
        }
      });
      
      req.signal.addEventListener('abort', () => {
        watcher.close();
      });
    }
  });
  
  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
