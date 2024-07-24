pipeline {
    agent any

    stages {
        stage('Clone repository') {
            steps {
                // Clone your repository
                git 'https://github.com/jawahar1098/thunderbolt.git'
            }
        }

        stage('Backend Deployment on Slave') {
            agent {
                label 'slavenode1' // Replace with your slave node label
            }
            steps {
                // Install Python and Git
                script {
                    // Install Python
                    sh 'apt-get update && apt-get install -y python'

                    // Install Git
                    sh 'apt-get install -y git'
                }

                // Backend deployment steps
                dir('backend') {
                    // Activate the virtual environment (assuming it's named 'env')
                    sh '. env/bin/activate'

                    // Start the Python backend application
                    sh 'python wsgi.py &'
                }
            }
        }

        stage('Frontend Deployment on Slave') {
            agent {
                label 'slavenode1' // Replace with your slave node label
            }
            steps {
                // Install Node.js and npm (if not already installed)
                script {
                    sh 'apt-get update && apt-get install -y nodejs npm'
                }

                // Frontend deployment steps
                dir('front_app') {
                    // Install npm dependencies
                    sh 'npm install'

                    // Start frontend development server
                    sh 'npm run dev &'
                }
            }
        }
    }
}
