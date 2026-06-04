# Logo Poll Web App

A clean, minimal, mobile-friendly logo voting web application. It displays logo designs one by one, allows users to rate them as Love or Hate, compiles a summary of the selections, and posts the results to a Google Sheet.

## Structure

```text
/logos         <- Folder to drop image files
index.html     <- Frontend application interface
logos.json     <- Generated file mapping available images
generate.py    <- Python script to compile image index
README.md      <- Setup and configuration manual
```

## Setup Instructions

### 1. Load Images
Drop all your logo images into the `logos/` folder. The application supports standard formats: PNG, JPG, JPEG, WEBP, and SVG.

### 2. Generate the Image Catalog
Run the Python script in the project root to scan your images and create the registry file `logos.json`:

```bash
python3 generate.py
```

This will scan the files, build the sorted array, write it to `logos.json`, and print a confirmation message.

### 3. Google Apps Script Configuration
To store poll submissions in a Google Sheet, follow these steps to deploy a custom database handler:

1. Create a new Google Sheet.
2. In the menu, go to **Extensions** -> **Apps Script**.
3. Clear the default template code in the editor and paste the following Google Apps Script:

```javascript
function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var payload = JSON.parse(e.postData.contents);
    var votes = payload.votes;
    var logos = payload.logos;
    
    // Check if row 1 is empty (check cell A1)
    var headerRange = sheet.getRange(1, 1);
    if (headerRange.isBlank() || headerRange.getValue() === "") {
      // Write headers: Timestamp followed by all logo filenames
      var headers = ["Timestamp"];
      for (var i = 0; i < logos.length; i++) {
        headers.push(logos[i]);
      }
      sheet.appendRow(headers);
    }
    
    // Read the headers in row 1 to match columns correctly
    var lastColumn = sheet.getLastColumn();
    var headerRow = sheet.getRange(1, 1, 1, lastColumn).getValues()[0];
    
    // Build the new row based on the header columns
    var row = [new Date()];
    // Start from index 1 (the logo columns)
    for (var j = 1; j < headerRow.length; j++) {
      var logoName = headerRow[j];
      var vote = votes[logoName] || "";
      row.push(vote);
    }
    
    sheet.appendRow(row);
    return ContentService.createTextOutput("ok");
  } catch(err) {
    return ContentService.createTextOutput("error: " + err.toString());
  }
}
```

4. Click the **Save** (floppy disk) icon to save the script.

### 4. Deploy the Apps Script Web App
1. Click the **Deploy** button at the top right of the Apps Script workspace, and select **New deployment**.
2. Click the gear icon next to **Select type** and choose **Web app**.
3. Provide a description (for example: Logo Poll Backend).
4. Under **Execute as**, select **Me (your email)**.
5. Under **Who has access**, select **Anyone**. This is required so the frontend application can submit anonymous votes.
6. Click **Deploy**.
7. Copy the generated **Web app URL** from the dialog box.

### 5. Link Frontend to Backend
1. Open the file `index.html` in a text editor.
2. Locate the configuration variable `SHEET_URL` at the top of the script tag (around line 348):
   ```javascript
   const SHEET_URL = "";
   ```
3. Paste your Web app URL inside the quotation marks:
   ```javascript
   const SHEET_URL = "https://script.google.com/macros/s/YOUR_DEPLOYED_SCRIPT_ID/exec";
   ```
4. Save the file. If `SHEET_URL` is kept empty, the application runs in offline/test mode where you can view the summary and complete submissions without saving to Google Sheets.

### 6. Host on GitHub Pages
To publish the voting application online:
1. Create a new repository on GitHub.
2. Commit and push the codebase (including `/logos`, `generate.py`, `logos.json`, `index.html`, and `README.md`) to your repository.
3. In your GitHub repository, navigate to **Settings** -> **Pages**.
4. Under **Build and deployment**, select **Deploy from a branch** as the source.
5. Select the main branch and `/ (root)` folder, then click **Save**.
6. GitHub will generate a public URL for your web app.
