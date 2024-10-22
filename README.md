# Todo Kivy

## Overview

Todo Kivy is a simple to-do application developed using the **Python Kivy** framework. Designed for Android devices, this application allows users to efficiently manage their tasks with a clean and intuitive interface.

## Features

- **Task Creation**: Easily add new tasks to your list.
- **Task Management**: Mark tasks as complete or delete them as needed.
- **User-Friendly Interface**: A straightforward layout that enhances user experience.
- **Persistent Storage**: Tasks are saved in a JSON file, maintaining data across app sessions.

## Technology Stack

- **Python Kivy**: A framework for developing multitouch applications.
- **Buildozer**: For packaging the application into a binary suitable for Android deployment.
- **GitHub Actions**: For continuous integration and deployment.
- **JSON**: Used for storing task data persistently.

## Development Workflow

1. **Local Development**: Code and test the application locally using Python and Kivy.
2. **Version Control**: Utilize Git for version control to manage changes effectively.
3. **Continuous Integration**: Automated workflows using GitHub Actions ensure validation of every change.
4. **Build Process**: Use Buildozer to compile the application into an Android package (.apk) for distribution.

## Getting Started

To get started with Todo Kivy, follow these steps:

1. **Clone the Repository**:
   ```
git clone https://github.com/deekshith0509/Todo-kivy.git
cd Todo-kivy
```

2. **Install Dependencies**: Make sure you have Kivy and other necessary dependencies installed, which can be specified in the requirements.txt file if applicable.

3. **Run Locally**: To run the application on your local machine, execute:
```
python main.py
```

4. **Build for Android**: To create an Android package, run:
```
    buildozer -v android debug
```
5. **Deploy to Device**: Use Buildozer to install the APK on an Android device for testing.

****Contribution****

Contributions are welcome! Feel free to open issues or submit pull requests. Your input helps improve the application.
