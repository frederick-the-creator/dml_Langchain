# User Stories for Theme Extraction Application

## Theme Analysis Feature

### US-4.1: Export Themes
**As a** user  
**I want to** 
- Be able to export the themes to a csv file and download it to my local machine

**Acceptance Criteria**
- Clickable button to download a csv file of the aggregated_df that is created in src/app.py


### US-4.2: Import Themes
**As a** user  
**I want to** 
- Upload and edited version of the csv downloaded in US-4.1

**Acceptance Criteria**
- Clickable button to upload a csv file with the themes
- The application should be able to read the csv and convert it to a dataframe. 
- This dataframe is shown in the UI below the previous version of the dataframe
- Replace the text 'Aggregated Results:' with 'Theme Extracted from Raw Data' and make the text bold and a few font sizes bigger
- For the new dataframe, title this as 'Themes Updated by User' in the same style as above. 