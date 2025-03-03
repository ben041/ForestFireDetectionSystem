# Fire Detection and Monitoring System

## Overview
The Fire Detection and Monitoring System is a Django-based web application that integrates fire detection capabilities with weather monitoring to provide real-time updates and alerts. It utilizes a pre-trained cascade classifier for fire detection, weather APIs for local weather data, and email notifications for critical alerts.

## Features
- **Fire Detection**: Uses OpenCV and a Haar Cascade classifier to detect fire in real-time from video feeds.
- **Real-time Alerts**: Plays an alarm sound and sends an email notification upon detecting fire.
- **Weather Monitoring**: Fetches and displays weather data for specific areas using OpenWeatherMap API.
- **Area Management**: Admins can manage and display geographic areas with latitude and longitude information.
- **User Authentication**: Includes sign-up, sign-in, and logout functionalities for users.
- **Video Recording**: Captures and stores video clips when fire is detected.

## Technologies Used
- **Backend**: Django Framework
- **Frontend**: HTML, CSS, and Django templates
- **Fire Detection**: OpenCV
- **Weather API**: OpenWeatherMap
- **Email Notifications**: SMTP
- **Database**: SQLite (default for Django)

## Prerequisites
- Python 3.8+
- Django 3.2+
- OpenCV 4.0+
- An SMTP-enabled email account (e.g., Gmail)

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/ben041/ForestFireDetectionSystem.git
    cd fire-detection-system
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply database migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Start the development server:
    ```bash
    python manage.py runserver
    ```

6. Access the application at `http://127.0.0.1:8000/`.

## Configuration
- **Fire Detection Cascade**: Ensure the `fire_detection_cascade_model.xml` file is in the project directory.
- **Email Notifications**: Update the email credentials in the `send_mail_function` method of `views.py`.
- **API Key**: Replace the placeholder API key in `monitor` view with your OpenWeatherMap API key.

## Project Structure
```
fire-detection-system/
|-- core/
|   |-- migrations/
|   |-- templates/
|   |   |-- index.html
|   |   |-- location.html
|   |   |-- map.html
|   |   |-- monitor.html
|   |   |-- signin.html
|   |   |-- signup.html
|   |-- static/
|   |-- views.py
|   |-- models.py
|   |-- urls.py
|-- media/
|-- recordings/
|-- fire_detection_cascade_model.xml
|-- manage.py
|-- requirements.txt
```

## Usage
### Adding Areas
1. Log in as an admin.
2. Navigate to the admin panel (`/admin`).
3. Add areas with their district, latitude, and longitude information.

### Monitoring Fire
1. Access the "Monitor" page for a specific area.
2. Upload a video feed to check for fire detection.
3. Upon detection, receive real-time alerts and view recorded videos.

### Viewing Weather Data
1. Select an area from the "Location" page.
2. View detailed weather data, including temperature, humidity, wind speed, and forecasts.

## Known Issues
- Ensure video files are in supported formats for proper fire detection.
- Accurate weather data depends on the availability of latitude and longitude for the area.

## Future Enhancements
- Real-time video feed integration via webcam.
- User roles with restricted access based on permissions.
- Mobile app integration for notifications and monitoring.

## Contributors
- **ben041** - [GitHub Profile](https://github.com/ben041)

## License
This project is licensed under the MIT License. See the LICENSE file for details.

