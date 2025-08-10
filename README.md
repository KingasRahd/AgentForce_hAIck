

# PlanNexus — AI Planner

This is a Flask-based web application that displays a chatbot interface and 
renders dynamic step-by-step data (from a Python list) with checkboxes.

---

## 1. Prerequisites

- Python 3.9+ installed
- Anaconda or Miniconda installed
- Basic understanding of Flask/Jinja2 templating
- Use your own api key and store it in .env file as API_KEY=<your api key>

---

## 2. Setting Up the Environment (Anaconda)

1. Create a new conda environment:
   conda create -n plannexus python=3.9

2. Activate the environment:
   conda activate plannexus

3. Install required dependencies:
   pip install -r requirements.txt

4. (Optional) If you plan to use extra libraries:
   pip install requests numpy pandas

---

## 4. Running the Application

1. Activate your conda environment:
   conda activate plannexus

2. Start the Flask app:
   python main.py

3. Open your browser and go to:
   http://127.0.0.1:5000/

---

## 5. Notes

- `l` is the Python list passed to Jinja template.
- `{{ l|length }}` gives the total number of steps.
- `onclick="sam(lgt)"` passes the length to JavaScript function.
- Make sure each checkbox has a unique ID to avoid conflicts.

---

## 7. Stopping the Server

Press `CTRL + C` in the terminal running Flask.

---

## 8. Auto-start Flask App on Laptop Boot (Anaconda Environment)

### Windows (Task Scheduler)
1. Open **Task Scheduler**.
2. Click **Create Task**.
3. In the **General** tab:
   - Name: `PlanNexus AutoStart`
4. In the **Triggers** tab:
   - Add → Begin the task: **At log on**
5. In the **Actions** tab:
   - Add → Action: **Start a Program**
   - Program/script:  
     ```
     C:\Users\<YourUsername>\anaconda3\Scripts\activate.bat
     ```
   - Add arguments:  
     ```
     plannexus && python C:\path\to\PlanNexus\main.py
     ```
6. Save and restart your PC — the Flask app should start automatically.

---

### macOS (LaunchAgent)
1. Create a `.plist` file in `~/Library/LaunchAgents/`:
```

nano \~/Library/LaunchAgents/com.plannexus.startup.plist

```
2. Add:
```

   <?xml version="1.0" encoding="UTF-8"?>

   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
   "http://www.apple.com/DTDs/PropertyList-1.0.dtd">

   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.plannexus.startup</string>
       <key>ProgramArguments</key>
       <array>
           <string>/Users/<YourUsername>/opt/anaconda3/bin/conda</string>
           <string>run</string>
           <string>-n</string>
           <string>plannexus</string>
           <string>python</string>
           <string>/path/to/PlanNexus/main.py</string>
       </array>
       <key>RunAtLoad</key>
       <true/>
   </dict>
   </plist>
   ```
3. Load it:
   ```
   launchctl load ~/Library/LaunchAgents/com.plannexus.startup.plist
   ```

---

### Linux (systemd)

1. Create a service file:

   ```
   sudo nano /etc/systemd/system/plannexus.service
   ```
2. Add:

   ```
   [Unit]
   Description=PlanNexus Flask App
   After=network.target

   [Service]
   Type=simple
   ExecStart=/home/<youruser>/anaconda3/bin/conda run -n plannexus python /path/to/PlanNexus/app.py
   WorkingDirectory=/path/to/PlanNexus
   Restart=always
   User=<youruser>

   [Install]
   WantedBy=multi-user.target
   ```
3. Enable & start:

   ```
   sudo systemctl enable plannexus
   sudo systemctl start plannexus
   ```

---

