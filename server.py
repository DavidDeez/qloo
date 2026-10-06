import http.server
import socketserver
import json
import urllib.request
import urllib.parse
from urllib.error import URLError

PORT = 8501
API_URL = "https://hackathon.api.qloo.com"
API_KEY = "hack_73913cf282adf18cb8c9efd647b5aa88d0138b97"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ClientVibe | B2B Intelligence</title>
    <style>
        :root { --bg: #0f172a; --panel: #1e293b; --text: #f8fafc; --muted: #94a3b8; --accent: #3b82f6; --accent-hover: #2563eb; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 2rem; }
        .container { max-width: 1200px; margin: 0 auto; }
        header { border-bottom: 1px solid #334155; padding-bottom: 1.5rem; margin-bottom: 2rem; }
        h1 { margin: 0 0 0.5rem; font-size: 1.8rem; font-weight: 600; }
        p.subtitle { color: var(--muted); margin: 0; }
        
        .grid { display: grid; grid-template-columns: 1fr 2fr; gap: 2rem; }
        .card { background: var(--panel); border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid #334155; }
        .card h3 { margin-top: 0; font-size: 1.1rem; color: #e2e8f0; border-bottom: 1px solid #334155; padding-bottom: 0.5rem; margin-bottom: 1rem; }
        
        label { display: block; margin-bottom: 0.5rem; font-size: 0.9rem; color: var(--muted); }
        input { width: 100%; box-sizing: border-box; background: #0f172a; border: 1px solid #334155; color: white; padding: 0.75rem; border-radius: 6px; margin-bottom: 1.5rem; font-size: 1rem; }
        input:focus { outline: none; border-color: var(--accent); }
        
        button { width: 100%; background: var(--accent); color: white; border: none; padding: 0.875rem; border-radius: 6px; font-weight: 600; cursor: pointer; transition: background 0.2s; }
        button:hover { background: var(--accent-hover); }
        button:disabled { background: #334155; cursor: not-allowed; }
        
        #results { display: none; }
        .tags-container { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1.5rem; }
        .tag { background: #334155; padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.85rem; font-weight: 500; color: #cbd5e1; }
        
        .recommendation-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem; }
        .rec-box { background: #0f172a; border: 1px solid #334155; padding: 1rem; border-radius: 8px; }
        .rec-box h4 { margin: 0 0 0.5rem; font-size: 1rem; }
        .rec-box ul { margin: 0; padding-left: 1.25rem; color: #cbd5e1; font-size: 0.95rem; }
        
        .email-draft { background: #000; border: 1px solid #334155; padding: 1.5rem; border-radius: 8px; font-family: monospace; white-space: pre-wrap; font-size: 0.9rem; color: #a3e635; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏆 ClientVibe Intelligence</h1>
            <p class="subtitle">Turn offhand conversational clues into hyper-personalized B2B relationships using Qloo Taste Data.</p>
        </header>
        
        <div class="grid">
            <!-- Sidebar: Input Form -->
            <div class="card">
                <h3>Client Profile Setup</h3>
                <label>Client Name & Role</label>
                <input type="text" id="name" value="Alex (VP of Sales)">
                
                <label>Cultural Seed Entities (Music, Brands, Places)</label>
                <input type="text" id="query" value="The National, Patagonia, Tulum">
                
                <button id="analyzeBtn" onclick="analyze()">Generate Qloo Insight Report</button>
            </div>
            
            <!-- Main Content: Results -->
            <div class="card" id="results">
                <h3>Analysis Dashboard</h3>
                <div id="content"></div>
            </div>
        </div>
    </div>

    <script>
        async function analyze() {
            const query = document.getElementById('query').value;
            const name = document.getElementById('name').value;
            const btn = document.getElementById('analyzeBtn');
            const results = document.getElementById('results');
            const content = document.getElementById('content');
            
            btn.disabled = true;
            btn.innerText = 'Analyzing Taste Graph...';
            results.style.display = 'block';
            content.innerHTML = '<p style="color:var(--muted)">Querying Qloo API endpoints...</p>';
            
            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    body: JSON.stringify({query: query, name: name})
                });
                const data = await response.json();
                
                // Build Tags
                let tagsHtml = `<div class="tags-container">`;
                if (data.correlations.tags && data.correlations.tags.length > 0) {
                    data.correlations.tags.forEach(t => tagsHtml += `<span class="tag">${t}</span>`);
                } else {
                    tagsHtml += `<span class="tag">No specific tags found</span>`;
                }
                tagsHtml += `</div>`;
                
                // Build Recommendations
                let recHtml = `<div class="recommendation-grid">
                    <div class="rec-box">
                        <h4>🍽️ Dining Vibe</h4>
                        <ul>`;
                data.correlations.dining.forEach(d => recHtml += `<li>${d}</li>`);
                recHtml += `</ul></div>
                    <div class="rec-box">
                        <h4>🎁 Gifting Profile</h4>
                        <ul>`;
                data.correlations.gifts.forEach(d => recHtml += `<li>${d}</li>`);
                recHtml += `</ul></div></div>`;
                
                // Build Email
                const topVibe = data.correlations.tags[0] || 'unique';
                const emailHtml = `<h4>📝 Auto-Drafted Outreach Email</h4>
<div class="email-draft">Hi ${name.split(' ')[0]},

Great catching up today! I remembered you mentioning you were a fan of ${query.split(',')[0]} and had a great time in ${query.split(',').pop().trim()}. 

If you're free next week, I'd love to grab dinner. Given your tastes, I know a great spot with a really ${topVibe} vibe that I think you'd appreciate.

Best,
Your Name
</div>`;
                
                content.innerHTML = `
                    <label>Real-time Qloo Demographic Footprint</label>
                    ${tagsHtml}
                    ${recHtml}
                    ${emailHtml}
                `;
            } catch (err) {
                content.innerHTML = `<p style="color:#ef4444;">Error connecting to server.</p>`;
            }
            
            btn.disabled = false;
            btn.innerText = 'Generate Qloo Insight Report';
        }
    </script>
</body>
</html>
"""

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML.encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/analyze':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            body = json.loads(post_data.decode('utf-8'))
            query_string = body.get('query', '')
            
            # Split the user input into individual entities
            entities = [e.strip() for e in query_string.split(',') if e.strip()]
            
            collected_tags = []
            
            # Call real Qloo API to extract cultural tags
            for entity in entities:
                try:
                    url = f"{API_URL}/search?query=" + urllib.parse.quote(entity)
                    req = urllib.request.Request(url, headers={'x-api-key': API_KEY})
                    with urllib.request.urlopen(req, timeout=3) as response:
                        data = json.loads(response.read().decode())
                        if data.get('results') and len(data['results']) > 0:
                            # Get the best match
                            best_match = data['results'][0]
                            tags = [t['name'] for t in best_match.get('tags', [])][:10]
                            collected_tags.extend(tags)
                except Exception as e:
                    print(f"Error fetching {entity}: {e}")
                    pass
            
            # Deduplicate tags
            unique_tags = list(set(collected_tags))
            
            # Simulated Agentic Logic: An LLM would take `unique_tags` and generate this dynamically.
            # We will generate dynamic text based on the real Qloo tags we found!
            if unique_tags:
                tag_preview = ", ".join(unique_tags[:5])
                dining = [f"Restaurants matching: {unique_tags[0]}", f"Vibe: {unique_tags[1]} dining"] if len(unique_tags) > 1 else ["Upscale Dining"]
                gifts = [f"A gift related to: {unique_tags[2] if len(unique_tags) > 2 else 'Art'}", f"Experiences feeling {unique_tags[3] if len(unique_tags) > 3 else 'Premium'}"]
            else:
                tag_preview = "No clear cultural footprint found."
                dining = ["High-end Steakhouse"]
                gifts = ["Premium Wine"]
                
            res = {
                "correlations": {
                    "dining": dining,
                    "gifts": gifts,
                    "tags": unique_tags[:10]
                }
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(res).encode('utf-8'))

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
