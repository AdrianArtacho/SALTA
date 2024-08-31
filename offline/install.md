# SALTA App | Installation

---

# Install

1. Install `node.js` ([LTS](https://nodejs.org/)) 

2. Verify Installation
   
   ```shell
   node -v
   npm -v
   ```

3. Install http-server or live-server:
   
   ```shell
   npm install -g http-server
   # sudo npm install -g http-server

   npm install -g live-server
   # sudo npm install -g live-server
   ```

4. Navigate to your project’s root directory and Start the server:

   ```shell
   # Go to root directory
   cd path/to/your/repo

   # Start server
   http-server
   ```

5. This will serve your files locally, similarly to how GitHub Pages would. Now go to

> [http://localhost:8080](http://localhost:8080)
> 
> or ([http://127.0.0.1:8080](http://127.0.0.1:8080))

---

### Error: `An error occurred while processing the file.` (main.js)

The error you're encountering when running your website locally is likely due to CORS (Cross-Origin Resource Sharing) issues. This happens because your JavaScript code is trying to make a request from your local environment (http://localhost:8080) to a different domain (https://flask-api-efnqmcjjla-ew.a.run.app), which is not allowed by default due to security restrictions.

#### Temporarily Bypass CORS for Local Development

The [Moesif CORS extension](https://chromewebstore.google.com/detail/moesif-origincors-changer/digfbfaphojjndkpccljibejjbppifbc?pli=1) for Chrome allows you to turn off CORS restrictions temporarily.

1. Install the extension

2. Enable CORS

3. Run normally:

```shell
htttp-server
```

---
