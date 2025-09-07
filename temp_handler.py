
def handle_portal_data(handler, UPLOAD_ROOT, safe_join):
    """
    Handle GET and POST for PortalData.json located in hidden folder 'useful-info'.
    This exposes ONLY this specific file securely.
    """
    # Assuming 'useful-info' matches the config.json hidden folder name
    PORTAL_DATA_PATH = os.path.join(UPLOAD_ROOT, "useful-info", "PortalData.json")
    
    if handler.command == "GET":
        if os.path.exists(PORTAL_DATA_PATH):
            handler.send_response(200)
            handler.send_header("Content-Type", "application/json")
            handler.end_headers()
            with open(PORTAL_DATA_PATH, "rb") as f:
                shutil.copyfileobj(f, handler.wfile)
        else:
            # Return empty structure if not exists
            handler.send_response(200)
            handler.send_header("Content-Type", "application/json")
            handler.end_headers()
            handler.wfile.write(b'{"links":[]}')
            
    elif handler.command == "POST":
        try:
            length = int(handler.headers.get("Content-Length", 0))
            data = json.loads(handler.rfile.read(length))
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(PORTAL_DATA_PATH), exist_ok=True)
            
            with open(PORTAL_DATA_PATH, "w", encoding="utf-8") as f:
                # Expecting data to be the full JSON content object (e.g. {links: [...]})
                # If the client sends { content: {links...} } we might need to adjust, 
                # but Portal.html saveResource currently sends: 
                # { filename: 'Dashboard.json', content: { links } } to save_json.
                # Use compatible format: expect { content: {...} } or direct object?
                # Let's standardize on receiving the FULL object or Wrapped.
                # Portal.html previously sent: { filename:..., content: {links: ...} }
                # We will accept { links: ... } directly for cleaner API, or support the wrapped one.
                
                content_to_save = data
                if "content" in data and "filename" not in data.get("content", {}):
                     content_to_save = data["content"]
                
                json.dump(content_to_save, f, indent=4)
                
            handler.send_response(200)
            handler.end_headers()
            handler.wfile.write(b'{"status":"ok"}')
        except Exception as e:
            handler.send_error(500, f"Error saving portal data: {str(e)}")
