Video Demonstration: https://streamable.com/r9cuzv
# Request Form
This should be just about ready to deploy for MVP
- Request Form Submission -> Admin Panel -> Approve/Reject
   - If Approved -> Move to front-end/images
   - If Rejected -> Delete

Directory setup should look something like:
```
Project
├── touchless-kiosk-server/
│   ├── backend/
│   │   ├── All the backend code (API, database, etc)
│   │   ├── uploads
│   │   │   ├── img_requests
│   │   │   │   ├── {email (before@)}_request_{request #}
│   │   │   │   │   ├── Image Files
├── touchless-kiosk-front-end/
│   ├── images/
│   │   ├── slideshow pulls images from here
│   ├── src/
│   │   ├── home-interface
│   │   │   ├──image_slideshow_function.py
│   │   ├── request-form
```

# Steps to Run:
(I used Anaconda to run local)
1) Navigate to `touchless-kiosk-server/`

2) If you don't have the dependencies:
   ```bash
   pip install "fastapi[standard]"
   pip install --upgrade -r requirements.txt
   ```

3) Launch App from project root: 
   ```
   uvicorn backend.main:app --reload
   ```

4) Navigate to `touchless-kiosk-front-end/src/request-form` and open it with a web browser, submit a form

5) Then, Navigate to `touchless-kiosk-server/backend/docs/index.html` and open it with a browser. You should see a request in there. 
   - http://localhost:8000/imgrequestform/imgrequests

6) Approve that request then navigate to:
   ```bash
   touchless-kiosk-front-end/src/home-interface/
   ```
   ```bash
   install pygame: `pip install pygame`
   ```
   and run 
   ```bash
   py image_slideshow_function.py
   ```

Note: It's not perfect, but it's a proof of concept.

## Limitations/Future Plans
- In its current form, on approval/reject, EVERY image in the request is either removed or added. In the future, this should be reworked to be more modular.
- The admin page was thrown together for testing purposes and a proof of concept. Some time should be spent making this look nice
- Not sure if this'll be implemented tomorrow (2024/12/10) or not, but a login screen is vital for both the request form and admin panel.
- Restrict file size/type.
   - The use-case for multiple images was to post images from events. Maybe a restriction of `n` amount of photos per request should be added in order to limit the load.
- When login screen is implemented, name and email fields for the request form may no longer be needed and can be autofilled. 
