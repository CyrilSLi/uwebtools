import base64, os, pathlib, subprocess, zlib
abs_path = lambda path: os.path.join(os.path.dirname(__file__), pathlib.Path(path))

orig_size = os.path.getsize(abs_path("index.html"))

subprocess.run(["npx", "html-minifier-next", "-v", "-i", abs_path("index.html"), "-o", abs_path("index.min.html"), "-c", abs_path("html-minifier-next.config.json")])

with open(abs_path("index.min.html"), "rb") as f:
    data = base64.b64encode(zlib.compress(f.read(), 9)).decode("utf-8")

with open(abs_path("index.txt"), "w") as f:
    f.write(f'data:text/html,<script>a=Uint8Array,r=Response,new r(new r(a.from(atob("{data}"),c=>c.charCodeAt())).body.pipeThrough(new DecompressionStream("deflate"))).text().then((t,d=document)=>(d.open(),d.write(t),d.close()))</script>')

min_size = os.path.getsize(abs_path("index.txt"))

print(f"\nTotal: {orig_size} -> {min_size} bytes ({min_size - orig_size}, {min_size/orig_size:.2%})")